import requests
import httpx
import logging
from pygeoogc.exceptions import ZeroMatchedError
from pygeohydro import WBD

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DATA_SERVICES = {
    "riv_gauges": {
        "name": " National Water Prediction Service (NWPS) River Gauge System",
        "url": "https://mapservices.weather.noaa.gov/eventdriven/rest/services/water",
        "layers": [
            {
                "name": "Observed River Stages (0)",
                "filter_attr": "status",
                "id": 0,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "River Stages 24 hour Forecast (1)",
                "filter_attr": "status",
                "id": 1,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "River Stages 48 hour Forecast (2)",
                "filter_attr": "status",
                "id": 2,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "River Stages 72 hour Forecast (3)",
                "filter_attr": "status",
                "id": 3,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "River Stages 96 hour Forecast (4)",
                "filter_attr": "status",
                "id": 4,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "River Stages 120 hour Forecast (5)",
                "filter_attr": "status",
                "id": 5,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "River Stages 144 hour Forecast (6)",
                "filter_attr": "status",
                "id": 6,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "River Stages 168 hour Forecast (7)",
                "filter_attr": "status",
                "id": 7,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "River Stages 216 hour Forecast (9)",
                "filter_attr": "status",
                "id": 9,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "River Stages 240 hour Forecast (10)",
                "filter_attr": "status",
                "id": 10,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "River Stages 264 hour Forecast (11)",
                "filter_attr": "status",
                "id": 11,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "River Stages 288 hour Forecast (12)",
                "filter_attr": "status",
                "id": 12,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "River Stages 312 hour Forecast (13)",
                "filter_attr": "status",
                "id": 13,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "River Stages 336 hour Forecast (14)",
                "filter_attr": "status",
                "id": 14,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "Full Forecast Period Stages (15)",
                "filter_attr": "status",
                "id": 15,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
        ],
    },
    "ana_high_flow_magnitude": {
        "name": "National Water Model (NWM) High Flow Magnitude Analysis",
        "url": "https://maps.water.noaa.gov/server/rest/services/nwm",
        "layers": [
            {
                "name": "Est. Annual Exceedance Probability (0)",
                "filter_attr": "recur_cat",
                "id": 0,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            }
        ],
    },
    "ana_past_14day_max_high_flow_magnitude": {
        "name": "National Water Model (NWM) Past 14-Day Max High Flow Magnitude Analysis",
        "url": "https://maps.water.noaa.gov/server/rest/services/nwm",
        "layers": [
            {
                "name": "Past 7 Days - Est. Annual Exceedance Probability (0)",
                "filter_attr": "recur_cat_7day",
                "id": 0,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "Past 14 Days - Est. Annual Exceedance Probability (1)",
                "filter_attr": "recur_cat_14day",
                "id": 1,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
        ],
    },
    "srf_18hr_high_water_arrival_time": {
        "name": "National Water Model (NWM) 18 / 48-Hour High Water Arrival Time Forecast",
        "url": "https://maps.water.noaa.gov/server/rest/services/nwm",
        "layers": [
            {
                "name": "18 Hours - High Water Arrival Time (0)",
                "filter_attr": "high_water_arrival_hour",
                "id": 0,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "18 Hours - High Water End Time (1)",
                "filter_attr": "below_bank_return_hour",
                "id": 1,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
        ],
    },
    "srf_18hr_rapid_onset_flooding": {
        "name": "National Water Model (NWM) 18-Hour Rapid Onset Flooding Forecast",
        "url": "https://maps.water.noaa.gov/server/rest/services/nwm",
        "layers": [
            {
                "name": "18 Hours - Rapid Onset Flood Arrival Time (0)",
                "filter_attr": "flood_start_hour",
                "id": 0,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "18 Hours - Rapid Onset Flood Duration (1)",
                "filter_attr": "flood_length",
                "id": 1,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "18 Hours - NWM Waterway Length Flooded (2)",
                "filter_attr": "nwm_waterway_length_flooded_percent",
                "id": 2,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
        ],
        #
    },
    "srf_12hr_rapid_onset_flooding_probability": {
        "name": "National Water Model (NWM) 12-Hour Rapid Onset Flooding Probability Forecast",
        "url": "https://maps.water.noaa.gov/server/rest/services/nwm",
        "layers": [
            {
                "name": "Hours 1-6 - Rapid Onset Flooding Probability (0)",
                "filter_attr": "rapid_onset_prob_1_6",
                "id": 0,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "Hours 7-12 - Rapid Onset Flooding Probability (1)",
                "filter_attr": "rapid_onset_prob_7_12",
                "id": 1,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "Hours 1-12 - Rapid Onset Flooding Probability (2)",
                "filter_attr": "rapid_onset_prob_all",
                "id": 2,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "Hours 1-12 - Hotspots - Average Rapid Onset Flooding Probability (3)",
                "filter_attr": "weighted_mean",
                "id": 3,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
        ],
    },
    "srf_12hr_max_high_water_probability": {
        "name": "National Water Model (NWM) 12-Hour Max High Water Probability Forecast",
        "url": "https://maps.water.noaa.gov/server/rest/services/nwm",
        "layers": [
            {
                "name": "12 Hours - High Water Probability (0)",
                "filter_attr": "srf_prob",
                "id": 0,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "12 Hours - Hotspots - Average High Water Probability (1)",
                "filter_attr": "avg_prob",
                "id": 1,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
        ],
    },
    "srf_18hr_max_high_flow_magnitude": {
        "name": "National Water Model (NWM) 18 / 48-Hour Max High Flow Magnitude Forecast",
        "url": "https://maps.water.noaa.gov/server/rest/services/nwm",
        "layers": [
            {
                "name": "18 Hours - Est. Annual Exceedance Probability (0)",
                "filter_attr": "recur_cat",
                "id": 0,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
        ],
    },
    "mrf_gfs_10day_high_water_arrival_time": {
        "name": "National Water Model(NWM) GFS 10-Day High Water Arrival Time Forecast",
        "url": "https://maps.water.noaa.gov/server/rest/services/nwm",
        "layers": [
            {
                "name": "3 Days - High Water Arrival Time (0)",
                "filter_attr": "high_water_arrival_hour",
                "id": 0,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "10 Days - High Water Arrival Time (1)",
                "filter_attr": "high_water_arrival_hour",
                "id": 1,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "10 Days - High Water End Time (2)",
                "filter_attr": "below_bank_return_hour",
                "id": 2,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
        ],
    },
    "mrf_gfs_5day_max_high_water_probability": {
        "name": "National Water Model (NWM) GFS 5-Day High Water Probability Forecast",
        "url": "https://maps.water.noaa.gov/server/rest/services/nwm",
        "layers": [
            {
                "name": "Day 1 - High Water Probability (0)",
                "filter_attr": "hours_3_to_24",
                "id": 0,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "Day 2 - High Water Probability (1)",
                "filter_attr": "hours_27_to_48",
                "id": 1,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "Day 3 - High Water Probability (2)",
                "filter_attr": "hours_51_to_72",
                "id": 2,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "Days 4-5 - High Water Probability (3)",
                "filter_attr": "hours_75_to_120",
                "id": 3,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "Days 1-5 - High Water Probability (4)",
                "filter_attr": "hours_3_to_120",
                "id": 4,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "Days 1-5 - Hotspots - Average High Water Probability (5)",
                "filter_attr": "avg_prob",
                "id": 5,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
        ],
    },
    "mrf_gfs_10day_max_high_flow_magnitude": {
        "name": "National Water Model (NWM) GFS 10-Day Max High Flow Magnitude Forecast",
        "url": "https://maps.water.noaa.gov/server/rest/services/nwm",
        "layers": [
            {
                "name": "3 Days - Est. Annual Exceedance Probability (0)",
                "filter_attr": "recur_cat_3day",
                "id": 0,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "5 Days - Est. Annual Exceedance Probability (1)",
                "filter_attr": "recur_cat_5day",
                "id": 1,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
            {
                "name": "10 Days - Est. Annual Exceedance Probability (2)",
                "filter_attr": "recur_cat_10day",
                "id": 2,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
        ],
    },
    "mrf_gfs_10day_rapid_onset_flooding": {
        "name": "National Water Model (NWM) GFS 10-Day Rapid Onset Flooding Forecast",
        "url": "https://maps.water.noaa.gov/server/rest/services/nwm",
        "layers": [
            {
                "name": "10 Day - Rapid Onset Flood Arrival Time (0)",
                "filter_attr": "flood_start_hour",
                "id": 0,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "10 Day - Rapid Onset Flood Duration (1)",
                "filter_attr": "flood_length",
                "id": 1,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "10 Day - NWM Waterway Length Flooded (2)",
                "filter_attr": "nwm_waterway_length_flooded_percent",
                "id": 2,
                "drawingInfoAttr": "uniqueValueInfos",
                "drawingInfoValueAttr": "value",
            },
        ],
    },
    "mrf_gfs_5day_rapid_onset_flooding_probability": {
        "name": "National Water Model (NWM) GFS 5-Day Rapid Onset Flooding Probability Forecast",
        "url": "https://maps.water.noaa.gov/server/rest/services/nwm",
        "layers": [
            {
                "name": "Day 1 - Rapid Onset Flooding Probability (0)",
                "filter_attr": "rapid_onset_prob_day1",
                "id": 0,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "Day 2 - Rapid Onset Flooding Probability (1)",
                "filter_attr": "rapid_onset_prob_day2",
                "id": 1,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "Day 3 - Rapid Onset Flooding Probability (2)",
                "filter_attr": "rapid_onset_prob_day3",
                "id": 2,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "Days 4-5 - Rapid Onset Flooding Probability (3)",
                "filter_attr": "rapid_onset_prob_day4_5",
                "id": 3,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "Days 1-5 - Rapid Onset Flooding Probability (4)",
                "filter_attr": "rapid_onset_prob_all",
                "id": 4,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
            {
                "name": "Days 1-5 - Hotspots - Average Rapid Onset Flooding Probability (5)",
                "filter_attr": "weighted_mean",
                "id": 5,
                "drawingInfoAttr": "classBreakInfos",
                "drawingInfoValueAttr": "classMaxValue",
            },
        ],
    },
}


def get_base_map_layers_dropdown():
    return [
        {
            "label": "ArcGIS Map Service Base Maps",
            "options": [
                {
                    "label": "World Light Gray Base",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Light_Gray_Base/MapServer",
                },
                {
                    "label": "World Dark Gray Base",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer",
                },
                {
                    "label": "World Topo Map",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer",
                },
                {
                    "label": "World Imagery",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer",
                },
                {
                    "label": "World Terrain Base",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/World_Terrain_Base/MapServer",
                },
                {
                    "label": "World Street Map",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer",
                },
                {
                    "label": "World Physical Map",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/World_Physical_Map/MapServer",
                },
                {
                    "label": "World Shaded Relief",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/World_Shaded_Relief/MapServer",
                },
                {
                    "label": "World Terrain Reference",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/World_Terrain_Reference/MapServer",
                },
                {
                    "label": "World Hillshade Dark",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade_Dark/MapServer",
                },
                {
                    "label": "World Hillshade",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer",
                },
                {
                    "label": "World Boundaries and Places Alternate",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Reference/World_Boundaries_and_Places_Alternate/MapServer",
                },
                {
                    "label": "World Boundaries and Places",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Reference/World_Boundaries_and_Places/MapServer",
                },
                {
                    "label": "World Reference Overlay",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Reference/World_Reference_Overlay/MapServer",
                },
                {
                    "label": "World Transportation",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Reference/World_Transportation/MapServer",
                },
                {
                    "label": "World Ocean Base ",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Ocean/World_Ocean_Base/MapServer",
                },
                {
                    "label": "World Ocean Reference",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Ocean/World_Ocean_Reference/MapServer",
                }
            ],
        }
    ]


def get_services_dropdown():
    return [
        {
            "label": service["name"],
            "options": [
                {
                    "label": layer["name"],
                    "value": f"{service['url']}/{service_key}/MapServer/{layer['id']}",
                }
                for layer in service["layers"]
            ],
        }
        for service_key, service in DATA_SERVICES.items()
    ]


def get_service_layers():
    layers = []
    # Iterate over DATA_SERVICES
    for _, service_value in DATA_SERVICES.items():
        for layer in service_value["layers"]:
            obj = {"label": layer["name"], "value": f"{layer['id']}"}
            layers.append(obj)
    return layers


def rgb_to_hex(rgb_color):
    """Convert RGB color to hex color code."""
    if rgb_color and len(rgb_color) >= 3:
        return "#{:02x}{:02x}{:02x}".format(*rgb_color[:3])
    return "#000000"


def get_drawing_info_attr(service_name, layer_id):
    service = DATA_SERVICES.get(service_name)
    if not service:
        return None

    layers = service.get("layers", [])
    for layer in layers:
        if layer.get("id") == layer_id:
            return layer.get("drawingInfoAttr")

    return None


def get_drawing_info(layer_info, service, layer_id):
    """Extract drawing information from layer info."""
    renderer = layer_info.get("drawingInfo", {}).get("renderer", {})
    drawing_attr = get_drawing_info_attr(service, layer_id)
    drawings = renderer.get(drawing_attr, {})
    return drawings


def get_layer_info(base_url, service, layer_id):
    """Retrieve layer information from the NWMP service."""
    layer_url = f"{base_url}/{service}/MapServer/{layer_id}"
    try:
        response = requests.get(f"{layer_url}?f=json")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching layer info: {e}")
        return {}


def get_metadata_from_api(api_url, id, type_feature):
    try:
        with httpx.Client(verify=False) as client:
            r = client.get(
                url=f"{api_url}/{type_feature}/{id}",
                timeout=None,
            )
            if r.status_code != 200:
                logger.error(f"Error: {r.status_code}")
                return None
            else:
                return r.json()
    except httpx.HTTPError as exc:
        logger.error(
            f"Error while requesting {exc.request.url!r}: {str(exc.__class__.__name__)}"
        )
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None


def get_huc_boundary(huc_level, huc_id):
    """
    Retrieve the watershed boundary geometry for a given HUC code.
    """
    wbd = WBD(huc_level)
    try:
        gdf = wbd.byids(huc_level, huc_id)
        return gdf.iloc[0]["geometry"]
    except ZeroMatchedError:
        logger.warning(f"No HUC boundary found for HUC ID {huc_id}")
        return None
    except Exception as e:
        logger.error(f"Error fetching HUC boundary: {e}")
        return None


def get_centroid_huc(huc_id):
    huc_level = f"huc{len(str(huc_id))}"
    geom = get_huc_boundary(huc_level, huc_id)
    centroid = geom.centroid
    return [centroid.x, centroid.y]
