from intake.source import base
import httpx
import asyncio
from .utilities import get_metadata_from_api
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NWMPSReachesSeries(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "nwmp_api"
    visualization_args = {
        "id": "text",
    }
    visualization_group = "NWMP"
    visualization_label = "NWMP Reaches Time Series"
    visualization_type = "plotly"

    def __init__(self, id, metadata=None):
        self.api_base_url = "https://api.water.noaa.gov/nwps/v1"
        self.id = id
        self.metadata = None
        self.reach_data = {
            "analysis_assimilation": None,
            "short_range": None,
            "medium_range": None,
            "long_range": None,
            "medium_range_blend": None,
        }
        self.matching_forecast = {
            "analysis_assimilation": "analysisAssimilation",
            "short_range": "shortRange",
            "medium_range": "mediumRange",
            "long_range": "longRange",
            "medium_range_blend": "mediumRangeBlend",
        }
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        super(NWMPSReachesSeries, self).__init__(metadata=metadata)

    def read(self):
        self.metadata = get_metadata_from_api(self.api_base_url, self.id, "reaches")
        if self.metadata is not None:
            self.getData()
        traces = self.create_plotly_data()
        layout = self.create_plotly_layout()
        return {"data": traces, "layout": layout}

    def create_plotly_data(self):
        """
        Process the data object to create a list of traces for Plotly.js.
        """
        traces = []
        for product_name, product in self.reach_data.items():
            if product_name == "reach":
                continue

            if product is None or not isinstance(product, dict):
                logger.warning(
                    f"The product '{product_name}' is None or not a dictionary. Skipping."
                )
                continue

            for simulation_name, simulation in product.items():
                if simulation is None or not isinstance(simulation, dict):
                    logger.warning(
                        f"The simulation '{simulation_name}' in product '{product_name}' is None or not a dictionary. Skipping."
                    )
                    continue

                data_points = simulation.get("data", [])
                if not data_points:
                    logger.warning(
                        f"No data points found for simulation '{simulation_name}' in product '{product_name}'. Skipping."
                    )
                    continue

                x = [
                    point.get("validTime")
                    for point in data_points
                    if "validTime" in point
                ]
                y = [point.get("flow") for point in data_points if "flow" in point]

                if not x or not y:
                    logger.warning(
                        f"Missing 'validTime' or 'flow' in data points for simulation '{simulation_name}' in product '{product_name}'. Skipping."
                    )
                    continue

                trace = {
                    "x": x,
                    "y": y,
                    "type": "scatter",
                    "mode": "lines",
                    "name": f"{product_name} {simulation_name}",
                    "line": {"width": 2},
                }
                traces.append(trace)

        return traces

    def create_plotly_layout(self, yaxis_title="Flow"):
        """
        Create a layout dictionary for Plotly.js based on the data object.
        """
        units = None
        for product_name, product in self.reach_data.items():
            if product_name == "reach":
                continue

            if product is None or not isinstance(product, dict):
                continue

            for simulation_name, simulation in product.items():
                units = simulation.get("units")
                if units:
                    break
            if units:
                break

        if units:
            yaxis_title_with_units = f"{yaxis_title} ({units})"
        else:
            yaxis_title_with_units = yaxis_title

        layout = {
            "title": "<b>Reach</b>: {} <br><sub>ID:{} </sub>".format(
                self.metadata.get("name", "Unknown"), self.id
            ),
            "xaxis": {
                "type": "date",
                "tickformat": "%Y-%m-%d\n%H:%M",
            },
            "yaxis": {
                "title": {"text": yaxis_title_with_units},
                "rangemode": "tozero",
            },
            "legend": {
                "orientation": "h",
                "x": 0,
                "y": -0.2,
            },
            "margin": {
                "l": 50,
                "r": 50,
                "t": 80,
                "b": 80,
            },
            "hovermode": "x unified",
        }

        return layout

    async def reach_api_call(self, product):
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.get(
                    url=f"{self.api_base_url}/reaches/{self.id}/streamflow",
                    params={"series": product},
                    timeout=None,
                )
                logger.info(f"Request URL: {product} {response.status_code}")

                if response.status_code != 200:
                    logger.error(f"Error: {response.status_code}")
                    logger.error(response.text)
                    return None
                else:
                    self.reach_data[product] = response.json().get(
                        self.matching_forecast[product], None
                    )
                    return response.json()
        except Exception as e:
            logger.error(e)
            return None

    async def make_reach_api_calls(self, products):
        tasks = []
        for product in products:
            task = self.reach_api_call(product)
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results

    def getData(self):
        try:
            products = self.reach_data.keys()
            results = self.loop.run_until_complete(self.make_reach_api_calls(products))
            return results
        except Exception as e:
            logger.error(e)
            return None
