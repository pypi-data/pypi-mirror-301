import requests
import pandas as pd
from shapely.geometry import MultiPolygon
from pygeoogc import ArcGISRESTful
import pygeoutils as geoutils
from pygeoogc.exceptions import ZeroMatchedError
from intake.source import base
from .utilities import (
    get_services_dropdown,
    DATA_SERVICES,
    get_layer_info,
    get_drawing_info,
    rgb_to_hex,
    get_huc_boundary,
)
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NWMPService(base.DataSource):
    """
    A data source class for NWMP services, extending Intake's DataSource.
    """

    container = "python"
    version = "0.0.3"
    name = "nwmp_data_service"
    visualization_args = {
        "huc_id": "text",
        "service_and_layer_id": get_services_dropdown(),
    }
    visualization_group = "NWMP"
    visualization_label = "NWMP Data Service"
    visualization_type = "card"

    def __init__(self, service_and_layer_id, huc_id, metadata=None):
        """
        Initialize the NWMPService data source.
        """
        super().__init__(metadata=metadata)
        parts = service_and_layer_id.split("/")
        self.service = parts[-3]
        self.layer_id = int(parts[-1])
        self.BASE_URL = "/".join(parts[:-3])
        self.huc_level = f"huc{len(str(huc_id))}"
        self.huc_id = huc_id
        self.layer_info = get_layer_info(self.BASE_URL, self.service, self.layer_id)
        self.title = None
        self.description = None

    def read(self):
        """
        Read data from NWMP service and return a dictionary with title, data, and description.
        """
        logger.info("Reading data from NWMP service")
        logger.info(f"Service: {self.BASE_URL}/{self.service}/MapServer")
        logger.info(f"Layer ID: {self.layer_id}")
        logger.info(f"HUC IDs: {self.huc_id}")
        service_url = f"{self.BASE_URL}/{self.service}/MapServer"
        self.title = self.make_title()
        geometry = get_huc_boundary(self.huc_level, self.huc_id)
        if geometry is None:
            df = pd.DataFrame()
        else:
            df = self.get_river_features(service_url, geometry)
        if not df.empty:
            df = self.add_symbols(df)
            stats = self.get_statistics(df)
        else:
            stats = {}

        return {
            "title": self.title,
            "data": stats,
        }

    def make_title(self):
        """Create a title for the data."""
        return self.layer_info.get("name", "NWMP Data")

    def get_service_info(self):
        """Retrieve service information from the NWMP service."""
        service_url = f"{self.BASE_URL}/{self.service}/MapServer"
        try:
            response = requests.get(f"{service_url}?f=json")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching service info: {e}")
            return {}

    @staticmethod
    def get_drawing_info_value_attr(service_name, layer_id):
        service = DATA_SERVICES.get(service_name)
        if not service:
            return None

        layers = service.get("layers", [])
        for layer in layers:
            if layer.get("id") == layer_id:
                return layer.get("drawingInfoValueAttr")
        return None

    def get_label_and_color_for_value(self, filter_attr, symbol_dict):
        match = symbol_dict.get(filter_attr, None)
        if match:
            return match["label"], match["symbol"]["color"]
        return None, None

    def add_symbols_info(self, df, symbols, filter_attr):
        drawing_info_val_attr = self.get_drawing_info_value_attr(
            self.service, self.layer_id
        )
        if drawing_info_val_attr == "value":
            df = self.assign_labels_and_colors_based_on_value(df, symbols, filter_attr)
        else:
            df = self.assign_labels_and_colors_based_on_range(df, filter_attr, symbols)
        return df

    def assign_labels_and_colors_based_on_value(self, df, symbol_list, filter_attr):
        symbol_dict = {str(item["value"]): item for item in symbol_list}
        df["label"], df["color"] = zip(
            *df[filter_attr].apply(
                lambda x: self.get_label_and_color_for_value(str(x), symbol_dict)
            )
        )
        df["hex"] = df["color"].apply(lambda x: rgb_to_hex(x))
        return df

    def assign_labels_and_colors_based_on_range(
        self,
        df,
        value_column,
        symbol_list,
        label_column="label",
        color_column="hex",
    ):
        """
        Assign labels and colors to a DataFrame based on a value column and a symbol list.
        """
        bins = [0] + [item["classMaxValue"] for item in symbol_list[:-1]] + [np.inf]
        labels = [item["label"] for item in symbol_list]
        colors = [item["symbol"]["color"] for item in symbol_list]

        label_to_color = dict(zip(labels, colors))
        df[value_column] = pd.to_numeric(df[value_column], errors="coerce")

        df[label_column] = pd.cut(
            df[value_column], bins=bins, labels=labels, right=True, include_lowest=True
        )

        label_to_color_hex = {
            label: rgb_to_hex(color) for label, color in label_to_color.items()
        }
        df[color_column] = df[label_column].map(label_to_color_hex)
        return df

    def add_symbols(self, df):
        """Add symbols to the DataFrame."""
        filter_attr = self.get_color_attribute()
        symbols = get_drawing_info(self.layer_info, self.service, self.layer_id)
        if not symbols:
            logger.warning("No drawing symbols found.")
            return df
        df = self.add_symbols_info(df, symbols, filter_attr)
        return df

    def get_color_attribute(self):
        """Get the attribute name used for coloring."""
        service_info = DATA_SERVICES.get(self.service, {})
        layers = service_info.get("layers", [])
        layer_info = next(
            (layer for layer in layers if layer.get("id") == self.layer_id), {}
        )
        attr_name = layer_info.get("filter_attr")
        if not attr_name:
            logger.warning(f"No filter attribute found for layer ID {self.layer_id}")
        return attr_name

    def get_river_features(self, url, geometry):
        """Fetch river features from the service within the given geometry."""
        hr = ArcGISRESTful(url, self.layer_id)
        dfs = []
        geometries = (
            geometry.geoms if isinstance(geometry, MultiPolygon) else [geometry]
        )
        for geom in geometries:
            try:
                oids = hr.oids_bygeom(geom, spatial_relation="esriSpatialRelContains")
                if oids:
                    resp = hr.get_features(oids)
                    df_temp = geoutils.json2geodf(resp)
                    dfs.append(df_temp)
                else:
                    logger.warning("No OIDs found for the geometry.")
            except ZeroMatchedError:
                logger.warning(
                    "ZeroMatchedError: No features found within the given geometry."
                )
                continue
            except Exception as e:
                logger.error(f"Error fetching features for a geometry: {e}")
                continue
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            return df
        else:
            logger.warning("No river features found in any of the geometries.")
            return pd.DataFrame()

    def get_statistics(self, df):
        """Compute statistics from the DataFrame."""
        grouped = df.groupby(by=["label", "hex"], as_index=False).size()
        grouped = grouped[grouped["size"] > 0].reset_index(drop=True)  # tmp fix
        stats = grouped.to_dict("records")
        return stats
