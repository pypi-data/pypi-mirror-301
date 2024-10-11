# -*- coding: UTF-8 -*-

from typing import Optional, Union, Literal

import gseapy as gp
import numpy as np
import pandas as pd
from anndata import AnnData
from pandas import DataFrame

from ykenan_file import StaticMethod
from ykenan_log import Logger

from scLift.util import check_adata_get, to_dense, project_name

file_method = StaticMethod(f"{project_name}_preprocessing_gsea")
log = Logger(f"{project_name}_preprocessing_gsea")

_datasets_ = Optional[Literal['Human', 'Mouse', 'Yeast', 'Fly', 'Fish', 'Worm']]


def gsea_enrichr(
    gene_list: list[str],
    gene_sets: Union[list[str], set] = (
        "GO_Biological_Process_2023",
        "GO_Cellular_Component_2023",
        "GO_Molecular_Function_2023",
        "GWAS_Catalog_2023",
        "KEGG_2016"
    ),
    organism: _datasets_ = "human",
    output_dir: Optional[str] = None,
) -> DataFrame:

    # noinspection PyTypeChecker
    names = gp.get_library_name(organism)

    if not set(gene_sets).issubset(set(names)):
        log.error(f"The set of the {gene_sets} needs to include `gp.get_library_name(organism)`")
        raise ValueError(f"The set of the {gene_sets} needs to include `gp.get_library_name(organism)`")

    if output_dir is not None:
        file_method.makedirs(output_dir)

    log.info("GSEA enrichr.")
    # noinspection PyTypeChecker
    gsea = gp.enrichr(gene_list=gene_list, gene_sets=list(gene_sets), organism=organism, outdir=output_dir)
    return gsea.results


def get_gene_enrichment(
    adata: AnnData,
    top_number: int = 50,
    layer: Optional[str] = None,
    gene_sets: Union[list[str], set] = (
        "GO_Biological_Process_2023",
        "GO_Cellular_Component_2023",
        "GO_Molecular_Function_2023",
        "GWAS_Catalog_2023",
        "KEGG_2016"
    ),
    organism: _datasets_ = "human",
    output_dir: Optional[str] = None,
) -> DataFrame:
    log.info("Gene enrichment analysis.")
    # get data
    new_adata = check_adata_get(adata, layer=layer)

    enrichr_data_list = []

    cluster_list: list[str] = list(new_adata.var.index)
    gene_list: list = list(new_adata.obs_names)

    if len(gene_list) < top_number:
        log.warn(f"The number of parameters `top_number` ({top_number}) is greater than the number of genes ({len(gene_list)}).")
        top_number = len(gene_list)

    # Add data
    for cluster in cluster_list:
        log.info(f"Processing cluster: {cluster}")

        # get index
        _values_ = to_dense(new_adata[:, cluster].X, is_array=True).flatten()
        _top_index_ = np.argsort(_values_)[0:top_number]
        _cluster_gene_list_: list[str] = list(np.array(gene_list)[_top_index_])

        enrichr_data: DataFrame = gsea_enrichr(
            gene_list=_cluster_gene_list_,
            gene_sets=gene_sets,
            organism=organism,
            output_dir=output_dir
        )
        enrichr_data["cluster"] = cluster
        enrichr_data_list.append(enrichr_data)

        del _values_
        del _top_index_
        del _cluster_gene_list_

    data = pd.concat(enrichr_data_list, axis=0)

    return data
