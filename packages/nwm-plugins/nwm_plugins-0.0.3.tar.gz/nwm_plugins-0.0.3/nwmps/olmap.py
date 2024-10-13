from .utilities import (
    get_base_map_layers_dropdown,
    get_services_dropdown,
    DATA_SERVICES,
    rgb_to_hex,
    get_layer_info,
    get_drawing_info,
    get_centroid_huc,
)

from intake.source import base
from pyproj import Transformer
import json
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MapVisualization(base.DataSource):
    container = "python"
    version = "0.0.3"
    name = "nwmp_map"
    visualization_args = {
        "base_map_layer": get_base_map_layers_dropdown(),
        "zoom": "number",
        "huc_id": "text",
        "services": get_services_dropdown(),
    }
    visualization_group = "NWMP"
    visualization_label = "NWMP Map"
    visualization_type = "map"

    def __init__(self, base_map_layer, zoom, services, huc_id, metadata=None):
        self.zoom = zoom
        self.huc_id = huc_id
        parts = services.split("/")
        self.service = parts[-3]
        self.layer_id = int(parts[-1])
        self.BASE_URL = "/".join(parts[:-3])
        self.base_map_layer = self.get_esri_base_layer_dict(base_map_layer)
        self.service_layer = self.get_service_layer_dict()
        self.center = self.get_center()
        self.view = self.get_view_config(center=self.center, zoom=self.zoom)
        self.map_config = self.get_map_config()
        self.legend = self.make_legend()
        self.HUC_LAYER = self.get_wbd_layer()

        super(MapVisualization, self).__init__(metadata=metadata)

    def read(self):
        logger.info("Reading map data configuration")
        layers = [self.base_map_layer, self.HUC_LAYER, self.service_layer]
        return {
            "layers": layers,
            "view_config": self.view,
            "map_config": self.map_config,
            "legend": self.legend,
        }

    def get_service_layers(self):
        result = []
        logger.info("Fetching service layers")
        for service_value in DATA_SERVICES.items():
            service_dict = {
                "name": service_value["name"],
                "layers": [
                    {"name": layer["name"], "id": layer["id"]}
                    for layer in service_value["layers"]
                ],
            }
            result.append(service_dict)
        return result

    def get_service_layer_dict(self):
        service_url = f"{self.BASE_URL}/{self.service}/MapServer"
        layer_dict = {
            "type": "ImageLayer",
            "props": {
                "source": {
                    "type": "ImageArcGISRest",
                    "props": {
                        "url": service_url,
                        "params": {
                            "LAYERS": f"show:{self.layer_id}",
                        },
                    },
                },
                "name": f'{self.service.replace("_"," ").title()}',
            },
        }
        logger.info(f"Service layer dictionary created for {self.service}")
        return layer_dict

    def make_legend(self):
        """Create a list of dicts with color in hex and label."""
        logger.info("Creating legend for the map")
        layer_info = get_layer_info(self.BASE_URL, self.service, self.layer_id)
        drawing_info = get_drawing_info(layer_info, self.service, self.layer_id)
        legend = []
        for item in drawing_info:
            hex_color = rgb_to_hex(item["symbol"]["color"])
            legend.append({"color": hex_color, "label": item["label"]})

        logger.info("Legend created successfully")
        return legend

    @staticmethod
    def get_esri_base_layer_dict(base_map_layer):
        layer_dict = {
            "type": "WebGLTile",
            "props": {
                "source": {
                    "type": "ImageTile",
                    "props": {
                        "url": f"{base_map_layer}/tile/" + "{z}/{y}/{x}",
                        "attributions": f'Tiles © <a href="{base_map_layer}">ArcGIS</a>',
                    },
                },
                "name": f'{base_map_layer.split("/")[-2].replace("_"," ").title()}',
            },
        }
        logger.info("Base layer dictionary created")
        return layer_dict

    @staticmethod
    def get_view_config(center, zoom):
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
        x, y = transformer.transform(center[0], center[1])
        view_config = {
            "center": [x, y],
            "zoom": zoom,
        }
        logger.info("View configuration created")
        return view_config

    @staticmethod
    def get_map_config():
        map_config = {
            "className": "ol-map",
            "style": {"width": "100%", "height": "100%"},
        }
        logger.info("Map configuration created")
        return map_config

    def get_wbd_layer(self):
        layer_id = int(len(str(self.huc_id)) / 2)
        huc_level = f"huc{len(str(self.huc_id))}"
        logger.info(f"Creating WBD layer with HUC ID {self.huc_id}")
        return {
            "type": "ImageLayer",
            "props": {
                "source": {
                    "type": "ImageArcGISRest",
                    "props": {
                        "url": "https://hydro.nationalmap.gov/arcgis/rest/services/wbd/MapServer",
                        "params": {
                            "LAYERS": f"show:{layer_id}",
                            "layerDefs": json.dumps(
                                {f"{layer_id}": f"{huc_level}='{self.huc_id}'"}
                            ),
                        },
                    },
                },
                "name": "wbd Map Service",
            },
        }

    def get_center(self):
        """Get the center of the HUC."""
        center = [37.71859032558816, -98.71413513957045]
        try:
            center = get_centroid_huc(self.huc_id)
        except Exception as e:
            logger.warning(e)
        return center
