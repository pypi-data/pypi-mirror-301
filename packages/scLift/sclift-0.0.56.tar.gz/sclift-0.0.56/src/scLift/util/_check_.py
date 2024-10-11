# -*- coding: UTF-8 -*-

from anndata import AnnData
from ykenan_log import Logger

from ._matrix_ import to_dense, to_sparse
from ._constant_ import project_name

log = Logger(f"{project_name}_util_check")


def check_adata_get(adata: AnnData, layer: str = None, is_dense: bool = True, is_matrix: bool = False) -> AnnData:
    # judge input data
    if adata.shape[0] == 0:
        log.warn("Input data is empty")
        raise ValueError("Input data is empty")

    # get data
    data: AnnData = adata.copy()

    # judge layers
    if layer is not None:
        if layer not in list(data.layers):
            log.error("The `layer` parameter needs to include in `adata.layers`")
            raise ValueError("The `layer` parameter needs to include in `adata.layers`")

        data.X = to_dense(data.layers[layer], is_array=True) if is_dense else to_sparse(
            data.layers[layer], is_matrix=is_matrix
        )
    else:
        data.X = to_dense(data.X, is_array=True) if is_dense else to_sparse(data.X, is_matrix=is_matrix)

    return data
