# -*- coding: UTF-8 -*-

from typing import Optional, Literal

import pandas as pd
from pandas import DataFrame
from anndata import AnnData
import numpy as np

from ykenan_log import Logger

from scLift.util import collection, matrix_data, to_sparse, to_dense, number, check_adata_get, project_name

log = Logger(f"{project_name}_preprocessing_anndata")


def adata_group(
    adata: AnnData,
    column: str,
    extra_column: Optional[str] = None,
    axis: Literal[0, 1] = 0,
    layer: str = None,
    method: collection = ("mean", "sum", "max", "min")
) -> AnnData:
    """
    Group x types to obtain relevant information
    :param adata: input data;
    :param column: grouping column;
    :param extra_column: grouping column;
    :param axis: {0: adata.obs, 1: adata.var};
    :param layer: Specify the matrix to be processed;
    :param method: Sum or average or two total.
    :return: Data grouped by AnnData.
    """
    # judge input data
    if adata.shape[0] == 0:
        log.warn("Input data is empty")
        return adata

    # judge axis
    if not isinstance(axis, number) or axis not in range(2):
        log.error("The `axis` parameter must be either 0 or 1")
        raise ValueError("The `axis` parameter must be either 0 or 1")

    # get data
    data: AnnData = adata.copy() if axis == 0 else adata.copy().T

    # judge layers
    if layer is not None:
        if layer not in list(data.layers):
            log.error("The `layer` parameter needs to include in `adata.layers`")
            raise ValueError("The `layer` parameter needs to include in `adata.layers`")
        data.X = data.layers[layer]

    # get group information
    data_obs: DataFrame = data.obs
    if column not in data_obs.columns:
        log.error(f"The grouped column {column} are not in the corresponding columns {data_obs.columns}")
        raise ValueError(f"The grouped column {column} are not in the corresponding columns {data_obs.columns}")

    if extra_column is not None and extra_column not in data_obs.columns:
        log.error(f"The grouped extra-column {extra_column} are not in the corresponding columns {data_obs.columns}")
        raise ValueError(
            f"The grouped extra-column {extra_column} are not in the corresponding columns {data_obs.columns}"
        )

    # handle group information
    if extra_column is not None:
        obs: DataFrame = pd.DataFrame(data_obs[[extra_column, column]]).drop_duplicates()
        obs.index = obs[column].astype(str)
    else:
        obs: DataFrame = pd.DataFrame(data_obs[[column]]).drop_duplicates()
        obs.index = obs[column].astype(str)

    obs.sort_index(inplace=True)
    obs.rename_axis("group_column_index", inplace=True)
    column_size = obs.shape[0]
    column_group = list(obs[column])
    # create container
    matrix_sum: matrix_data = np.zeros((column_size, data.shape[1]))
    matrix_mean: matrix_data = np.zeros((column_size, data.shape[1]))
    matrix_max: matrix_data = np.zeros((column_size, data.shape[1]))
    matrix_min: matrix_data = np.zeros((column_size, data.shape[1]))

    # add data
    for i in range(column_size):
        # 获取 data_obs 下的索引信息
        data_obs_column: DataFrame = data_obs[data_obs[column] == column_group[i]]
        # sum value
        overlap_variant = data[list(data_obs_column.index), :]

        if "mean" in method:
            matrix_mean[i] = overlap_variant.X.mean(axis=0)

        if "sum" in method:
            matrix_sum[i] = overlap_variant.X.sum(axis=0)

        if "max" in method:
            matrix_max[i] = np.amax(to_dense(overlap_variant.X, is_array=True), axis=0)

        if "min" in method:
            matrix_min[i] = np.amin(to_dense(overlap_variant.X, is_array=True), axis=0)

    # create result
    ann_data = AnnData(to_sparse(matrix_mean), obs=obs, var=data.var)

    if "sum" in method:
        ann_data.layers["matrix_sum"] = to_sparse(matrix_sum)

    if "max" in method:
        ann_data.layers["matrix_max"] = to_sparse(matrix_max)

    if "min" in method:
        ann_data.layers["matrix_min"] = to_sparse(matrix_min)

    return ann_data if axis == 0 else ann_data.T


def adata_map_df(
    adata: AnnData,
    column: str = "value",
    layer: str = None
) -> DataFrame:
    """
    Convert AnnData to a form of `row   column  value`
    :param adata: Enter the AnnData data to be converted;
    :param column: Specify the column name of the value;
    :param layer: Specify the matrix to be processed;
    :return: The DataFrame data of the `row   column  value`.
    """
    # judge input data
    data: AnnData = check_adata_get(adata, layer=layer)

    # get group information
    data_obs: DataFrame = data.obs.copy()
    data_var: DataFrame = data.var.copy()

    if column in data_obs.columns or column in data_var.columns:
        log.error(f"The newly generated column cannot be within the existing column name")
        raise ValueError(f"The newly generated column cannot be within the existing column name")

    # rename index
    __on__: str = "on_5645465353221"
    data_var.rename_axis("y_index", inplace=True)
    data_var.reset_index(inplace=True)
    data_var["on_"] = __on__
    data_obs.rename_axis("x_index", inplace=True)
    data_obs.reset_index(inplace=True)
    data_obs["on_"] = __on__

    # create data
    log.info("Create Table")
    data_df: DataFrame = data_var.merge(data_obs, on="on_", how="outer")
    data_df.drop(["on_"], axis=1, inplace=True)
    data_df[column] = to_dense(data.X.T, is_array=True).flatten()
    return data_df
