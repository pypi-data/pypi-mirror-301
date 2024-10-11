# -*- coding: UTF-8 -*-

import pandas as pd
from pandas import DataFrame
from ykenan_log import Logger

from ._constant_ import project_name

log = Logger(f"{project_name}_util_check")


def add_cluster_info(data: DataFrame, data_ref: DataFrame, cluster: str) -> DataFrame:

    new_data: DataFrame = data.copy()
    if data_ref is not None and cluster not in new_data.columns:

        new_data: DataFrame = pd.merge(new_data, data_ref, how="left", left_index=True, right_index=True)

        if "barcode_x" in new_data.columns:
            new_data["barcode"] = new_data["barcode_x"]
            new_data.drop("barcode_x", axis=1, inplace=True)

            if "barcode_y" in new_data.columns:
                new_data.drop("barcode_y", axis=1, inplace=True)

        if "barcodes_x" in new_data.columns:
            new_data["barcodes"] = new_data["barcodes_x"]
            new_data.drop("barcodes_x", axis=1, inplace=True)

            if "barcodes_y" in new_data.columns:
                new_data.drop("barcodes_y", axis=1, inplace=True)

    if cluster not in new_data.columns:
        log.error(f"`{cluster}` is not in `adata.obs.columns`.")
        raise ValueError(f"`{cluster}` is not in `columns` ({new_data.columns}).")

    return new_data
