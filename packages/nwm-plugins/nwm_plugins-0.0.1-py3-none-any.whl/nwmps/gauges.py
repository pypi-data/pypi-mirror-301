from intake.source import base
import httpx
from .utilities import get_metadata_from_api
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# This will be used for the TimeSeries of the NWM data
class NWMPSGaugesSeries(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "nwmp_api"
    visualization_args = {"id": "text"}
    visualization_group = "NWMP"
    visualization_label = "NWMP Gauges Time Series"
    visualization_type = "plotly"

    def __init__(self, id, metadata=None):
        self.api_base_url = "https://api.water.noaa.gov/nwps/v1"
        self.id = id
        self.data = None
        self.metadata = None
        super(NWMPSGaugesSeries, self).__init__(metadata=metadata)

    def read(self):
        self.data = self.get_gauge_data()
        self.metadata = get_metadata_from_api(self.api_base_url, self.id, "gauges")
        traces = self.create_traces()
        flood_data = self.metadata.get("flood", {})
        shapes, annotations = self.create_flood_events(flood_data)
        secondary_range = self.get_secondary_data_range(self.data)
        layout = self.create_layout(shapes, annotations, secondary_range)
        return {"data": traces, "layout": layout}

    def get_gauge_data(self):
        try:
            with httpx.Client(verify=False) as client:
                r = client.get(
                    url=f"{self.api_base_url}/gauges/{self.id}/stageflow",
                    timeout=None,
                )
                if r.status_code != 200:
                    logger.error(f"Error: {r.status_code}")
                    logger.error(r.text)
                    return None
                else:
                    return r.json()
        except httpx.HTTPError as exc:
            logger.error(f"Error while requesting {exc.request.url!r}: {exc}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None

    def create_traces(self):
        traces = []
        datasets = ["observed", "forecast"]

        for dataset_name in datasets:
            if dataset_name in self.data:
                dataset = self.data[dataset_name]
                data_points = dataset.get("data", [])
                times = [d["validTime"] for d in data_points]
                primary_values = [d.get("primary", None) for d in data_points]
                secondary_values = [d.get("secondary", None) for d in data_points]

                hover_text = []
                for t, p, s in zip(times, primary_values, secondary_values):
                    utc_time = datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")
                    formatted_time = utc_time.strftime("%a %B %d %Y %I:%M:%S %p")
                    text = (
                        f"Time: {formatted_time}<br>{dataset.get('primaryUnits')}: {p}"
                    )
                    if s is not None and s >= 0:
                        text += f"<br>{dataset.get('secondaryUnits')}: {s}"
                    hover_text.append(text)

                trace = {
                    "x": times,
                    "y": primary_values,
                    "mode": "lines",
                    "name": dataset_name.capitalize(),
                    "yaxis": "y1",
                    "hoverinfo": "text",
                    "text": hover_text,
                }

                traces.append(trace)
                traceFake = {"x": times[0], "y": [0], "yaxis": "y2", "visible": False}
                traces.append(traceFake)

        return traces

    @staticmethod
    def create_flood_events(flood_data):
        shapes = []
        annotations = []

        if "categories" not in flood_data:
            return shapes, annotations

        categories = flood_data["categories"]
        category_colors = {
            "action": "orange",
            "minor": "yellow",
            "moderate": "red",
            "major": "purple",
        }

        for category, details in categories.items():
            stage = details.get("stage", None)
            if stage is not None:
                shapes.append(
                    {
                        "type": "line",
                        "x0": 0,
                        "x1": 1,
                        "xref": "paper",
                        "y0": stage,
                        "y1": stage,
                        "yref": "y1",
                        "line": {
                            "color": category_colors.get(category.lower(), "black"),
                            "width": 2,
                            "dash": "dash",
                        },
                    }
                )

                annotations.append(
                    {
                        "x": 0,
                        "y": stage,
                        "xref": "paper",
                        "yref": "y1",
                        "text": f"{stage} {flood_data.get('stageUnits', '')} - {category}".strip(),
                        "showarrow": False,
                        "xanchor": "left",
                        "yanchor": "bottom",
                        "font": {"color": "black", "size": 12},
                    }
                )

        return shapes, annotations

    @staticmethod
    def get_secondary_data_range(data):
        secondary_values = []
        datasets = ["observed", "forecast"]

        for dataset_name in datasets:
            if dataset_name in data:
                dataset = data[dataset_name]
                data_points = dataset.get("data", [])
                for d in data_points:
                    s = d.get("secondary", None)
                    if s is not None:
                        secondary_values.append(s)

        if not secondary_values:
            return (0, 1)
        else:
            min_secondary = min(secondary_values)
            max_secondary = max(secondary_values)
            padding = (
                (max_secondary - min_secondary) * 0.1
                if max_secondary != min_secondary
                else 1
            )
            return (min_secondary - padding, max_secondary + padding)

    @staticmethod
    def extract_names_units(dataset, data_type):
        if data_type == "primary":
            return (dataset.get("primaryName", ""), dataset.get("primaryUnits", ""))
        elif data_type == "secondary":
            return (dataset.get("secondaryName", ""), dataset.get("secondaryUnits", ""))
        else:
            raise ValueError("data_type must be 'primary' or 'secondary'")

    def create_layout(self, shapes, annotations, secondary_range):
        primary_name = ""
        primary_units = ""
        secondary_name = ""
        secondary_units = ""

        if "observed" in self.data:
            primary_name, primary_units = self.extract_names_units(
                self.data["observed"], "primary"
            )
            secondary_name, secondary_units = self.extract_names_units(
                self.data["observed"], "secondary"
            )
        elif "forecast" in self.data:
            primary_name, primary_units = self.extract_names_units(
                self.data["forecast"], "primary"
            )
            secondary_name, secondary_units = self.extract_names_units(
                self.data["forecast"], "secondary"
            )
        else:
            primary_name = "Primary"
            primary_units = ""
            secondary_name = "Secondary"
            secondary_units = ""

        layout = {
            "title": "<b>Gauge</b>: {} <br><sub>ID:{}</sub>".format(
                self.metadata.get("name", "Unknown"), self.id
            ),
            "xaxis": {"tickformat": "%I %p<br>%b %d"},
            "yaxis": {
                "title": f"{primary_name} ({primary_units})".strip(),
                "side": "left",
            },
            "yaxis2": {
                "title": f"{secondary_name} ({secondary_units})".strip(),
                "side": "right",
                "overlaying": "y",
                "showgrid": False,
                "range": secondary_range,
            },
            "legend": {
                "orientation": "h",
                "x": 0,
                "y": -0.2,
            },
            "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
            "hovermode": "x unified",
            "shapes": shapes,
            "annotations": annotations,
        }

        return layout
