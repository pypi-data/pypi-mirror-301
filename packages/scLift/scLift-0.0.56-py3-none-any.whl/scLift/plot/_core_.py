# -*- coding: UTF-8 -*-

import os
from typing import Tuple, Literal

import pandas as pd
from anndata import AnnData
from pandas import DataFrame

from ykenan_file import StaticMethod
from ykenan_log import Logger

from ._scatter_ import scatter_trait, scatter_atac
from ._heat_map_ import heatmap_annotation
from ._pie_ import pie_trait
from ._box_ import box_trait
from ._barcode_ import barcode_trait
from ._violin_ import violin_trait
from ._bar_ import bar_trait
from ._kde_ import kde
from ._graph_ import communities_graph

from scLift.preprocessing import adata_group, adata_map_df
from scLift.util import path, project_name

file_method = StaticMethod(f"{project_name}_plot_core")
log = Logger(f"{project_name}_plot_core")


def group_heatmap(
    adata: AnnData,
    layer: str = None,
    dir_name: str = "heatmap",
    row_name: str = "labels",
    col_name: str = "clusters",
    clusters: str = "clusters",
    cluster_method: str = "average",
    cluster_metric: str = "correlation",
    row_cluster: bool = True,
    col_cluster: bool = True,
    row_index: list = None,
    col_index: list = None,
    is_sort: bool = True,
    width: float = 8.0,
    height: float = 4.0,
    axis: Literal[0, 1] = 0,
    plot_output: str = None,
    show: bool = True
) -> None:
    # The relationship between cluster and trait
    adata_cluster: AnnData = adata_group(
        adata,
        clusters,
        extra_column=None if col_name == clusters else col_name,
        layer=layer,
        axis=axis
    )

    if row_index is not None:
        adata_cluster = adata_cluster[row_index, :].copy()
        is_sort = False

    if col_index is not None:
        adata_cluster = adata_cluster[:, col_index].copy()
        is_sort = False

    new_path: path = os.path.join(plot_output, dir_name) if plot_output is not None else None
    # create path
    if plot_output is not None:
        file_method.makedirs(new_path)

    # plot
    try:
        heatmap_annotation(
            adata_cluster.T,
            row_name=row_name,
            col_name=col_name,
            width=width,
            height=height,
            label="Mean TRS",
            row_legend=True,
            cluster_method=cluster_method,
            cluster_metric=cluster_metric,
            row_cluster=row_cluster,
            col_cluster=col_cluster,
            is_sort=is_sort,
            row_show_names=True,
            col_show_names=True,
            x_name="Cell type",
            y_name="Trait",
            show=show,
            output=os.path.join(new_path, f"{layer}_trait_mean.pdf") if new_path is not None else None
        )
    except Exception as e:
        log.warn(f"Changing clustering parameters {e.args}")
        heatmap_annotation(
            adata_cluster.T,
            row_name=row_name,
            col_name=col_name,
            width=width,
            height=height,
            label="Mean TRS",
            cluster_method="median",
            cluster_metric="euclidean",
            row_legend=True,
            row_cluster=row_cluster,
            col_cluster=col_cluster,
            is_sort=is_sort,
            row_show_names=True,
            col_show_names=True,
            x_name="Cell type",
            y_name="Trait",
            show=show,
            output=os.path.join(new_path, f"{layer}_trait_mean.pdf") if new_path is not None else None
        )

    try:
        heatmap_annotation(
            adata_cluster.T,
            layer="matrix_sum",
            row_name=row_name,
            col_name=col_name,
            width=width,
            height=height,
            label="Sum TRS",
            row_legend=True,
            cluster_method=cluster_method,
            cluster_metric=cluster_metric,
            row_cluster=row_cluster,
            col_cluster=col_cluster,
            is_sort=is_sort,
            row_show_names=True,
            col_show_names=True,
            x_name="Cell type",
            y_name="Trait",
            show=show,
            output=os.path.join(new_path, f"{layer}_trait_sum.pdf") if new_path is not None else None
        )
    except Exception as e:
        log.warn(f"Changing clustering parameters {e.args}")
        heatmap_annotation(
            adata_cluster.T,
            layer="matrix_sum",
            row_name=row_name,
            col_name=col_name,
            width=width,
            height=height,
            label="Sum TRS",
            cluster_method="median",
            cluster_metric="euclidean",
            row_legend=True,
            row_cluster=row_cluster,
            col_cluster=col_cluster,
            is_sort=is_sort,
            row_show_names=True,
            col_show_names=True,
            x_name="Cell type",
            y_name="Trait",
            show=show,
            output=os.path.join(new_path, f"{layer}_trait_sum.pdf") if new_path is not None else None
        )

    try:
        heatmap_annotation(
            adata_cluster.T,
            layer="matrix_max",
            row_name=row_name,
            col_name=col_name,
            width=width,
            height=height,
            label="Max TRS",
            row_legend=True,
            cluster_method=cluster_method,
            cluster_metric=cluster_metric,
            row_cluster=row_cluster,
            col_cluster=col_cluster,
            is_sort=is_sort,
            row_show_names=True,
            col_show_names=True,
            x_name="Cell type",
            y_name="Trait",
            show=show,
            output=os.path.join(new_path, f"{layer}_trait_max.pdf") if new_path is not None else None
        )
    except Exception as e:
        log.warn(f"Changing clustering parameters {e.args}")
        heatmap_annotation(
            adata_cluster.T,
            layer="matrix_max",
            row_name=row_name,
            col_name=col_name,
            cluster_method="median",
            cluster_metric="euclidean",
            width=width,
            height=height,
            label="Max TRS",
            row_legend=True,
            row_cluster=row_cluster,
            col_cluster=col_cluster,
            is_sort=is_sort,
            row_show_names=True,
            col_show_names=True,
            x_name="Cell type",
            y_name="Trait",
            show=show,
            output=os.path.join(new_path, f"{layer}_trait_max.pdf") if new_path is not None else None
        )

    try:
        heatmap_annotation(
            adata_cluster.T,
            layer="matrix_min",
            row_name=row_name,
            col_name=col_name,
            width=width,
            height=height,
            label="Min TRS",
            row_legend=True,
            cluster_method=cluster_method,
            cluster_metric=cluster_metric,
            row_cluster=row_cluster,
            col_cluster=col_cluster,
            is_sort=is_sort,
            row_show_names=True,
            col_show_names=True,
            x_name="Cell type",
            y_name="Trait",
            show=show,
            output=os.path.join(new_path, f"{layer}_trait_min.pdf") if new_path is not None else None
        )
    except Exception as e:
        log.warn(f"Changing clustering parameters {e.args}")
        heatmap_annotation(
            adata_cluster.T,
            layer="matrix_min",
            row_name=row_name,
            col_name=col_name,
            width=width,
            height=height,
            label="Min TRS",
            cluster_method="median",
            cluster_metric="euclidean",
            row_legend=True,
            row_cluster=row_cluster,
            col_cluster=col_cluster,
            is_sort=is_sort,
            row_show_names=True,
            col_show_names=True,
            x_name="Cell type",
            y_name="Trait",
            show=show,
            output=os.path.join(new_path, f"{layer}_trait_min.pdf") if new_path is not None else None
        )


def map_df_plot(
    adata: AnnData,
    layer: str = None,
    trait_cluster_map: dict = None,
    clusters: str = "clusters",
    feature_name: str = "feature",
    width: float = 16,
    y_name: str = "value",
    column: str = "value",
    show: bool = True,
    plot_output: path = None
) -> None:
    # create path
    new_path: path = os.path.join(
        plot_output,
        f"{layer}" if layer is not None else feature_name
    ) if plot_output is not None else None

    # create path
    if plot_output is not None:
        file_method.makedirs(new_path)

    # create data
    adata_df: DataFrame = adata_map_df(adata, column=column, layer=layer)

    # pie plot
    if trait_cluster_map is not None:
        pie_trait(
            adata_df,
            trait_cluster_map=trait_cluster_map,
            clusters=clusters,
            title=feature_name,
            show=show,
            output=new_path if plot_output is not None else None
        )

    # box plot
    box_trait(
        adata_df,
        y_name=y_name,
        value=column,
        clusters=clusters,
        width=width,
        title=feature_name,
        show=show,
        output=new_path if plot_output is not None else None
    )

    # rank plot
    barcode_trait(
        adata_df,
        sort_column=column,
        clusters=clusters,
        title=feature_name,
        show=show,
        output=new_path if plot_output is not None else None
    )

    # violin plot
    violin_trait(
        adata_df,
        y_name=y_name,
        value=column,
        width=width,
        clusters=clusters,
        title=feature_name,
        show=show,
        output=new_path if plot_output is not None else None
    )


def complete_ratio(
    adata: AnnData,
    layer: str = None,
    column: str = "value",
    clusters: str = "clusters"
) -> DataFrame:
    # create data
    adata_df: DataFrame = adata_map_df(adata, column=column, layer=layer)
    clusters_group = adata_df.groupby(["id", clusters], as_index=False).size()
    value_group = adata_df.groupby(["id", clusters, "value"], as_index=False).size()
    new_value_group = value_group.merge(clusters_group, on=["id", clusters], how="left")

    # Completion
    id_list = list(set(new_value_group["id"]))
    clusters_list = list(set(new_value_group[clusters]))
    value_list = [1.0, 0.0]
    total_size = len(id_list) * len(clusters_list) * len(value_list)

    if total_size != new_value_group.shape[0]:
        new_value_group_index = (
            new_value_group["id"].astype(str) + "_"
            + new_value_group[clusters].astype(str) + "_"
            + new_value_group["value"].astype(int).astype(str)
        )
        new_value_group.index = new_value_group_index
        new_value_group_index = list(new_value_group_index)

        trait_df: DataFrame = pd.DataFrame(columns=new_value_group.columns)

        # [id clusters  value  size_x  size_y]
        for _id_ in id_list:
            for _clusters_ in clusters_list:
                for _value_ in value_list:

                    # At this point, it means that the enrichment effect is 1, while the non enrichment effect is 0,
                    # so it does not exist during grouping and needs to be added here
                    if (_id_ + "_" + _clusters_ + "_" + str(int(_value_))) not in new_value_group_index:
                        exit_value = 0 if int(_value_) == 1 else 1
                        exit_index = _id_ + "_" + _clusters_ + "_" + str(exit_value)
                        exit_data = new_value_group[new_value_group.index == exit_index]
                        exit_data.loc[exit_index, "value"] = _value_
                        exit_data.loc[exit_index, "size_x"] = 0
                        exit_data.index = [_id_ + "_" + _clusters_ + "_" + str(int(_value_))]
                        trait_df = pd.concat((trait_df, exit_data), axis=0)

        new_value_group = pd.concat((trait_df, new_value_group), axis=0)

    new_value_group["rate"] = new_value_group["size_x"] / new_value_group["size_y"]

    return new_value_group


def rate_bar_plot(
    adata: AnnData,
    layer: str = None,
    trait_name: str = "All",
    dir_name: str = "feature",
    column: str = "value",
    clusters: str = "clusters",
    color: Tuple = ("#2e6fb7", "#f7f7f7"),
    legend: Tuple = ("Enrichment", "Conservative"),
    x_name: str = "Cell type",
    y_name: str = "Enrichment ratio",
    text_color: str = "#000205",
    width: float = 4,
    height: float = 4,
    bottom: float = 0,
    title: str = None,
    text_left_move: float = 0.15,
    plot_output: path = None,
    show: bool = True
) -> None:

    if dir_name is not None:
        # create path
        new_path = os.path.join(plot_output, f"{dir_name}_{layer}") if plot_output is not None else None
        # create path
        if plot_output is not None:
            file_method.makedirs(new_path)
    else:
        plot_output = None
        new_path = None

    # create data
    new_value_group = complete_ratio(adata=adata, layer=layer, column=column, clusters=clusters)

    bar_trait(
        trait_df=new_value_group,
        value="rate",
        clusters=clusters,
        title=title,
        x_name=x_name,
        y_name=y_name,
        trait_name=trait_name,
        color=color,
        legend=legend,
        text_color=text_color,
        width=width,
        height=height,
        bottom=bottom,
        text_left_move=text_left_move,
        output=new_path if plot_output is not None else None,
        show=show
    )


def init_score_plot(
    init_score: AnnData,
    plot_output: str,
    clusters: str = "clusters",
    plot_columns: Tuple[str, str] = ("UMAP1", "UMAP2"),
    trait_cluster_map: dict = None,
    width: float = 8
) -> None:
    # plot
    file_method.makedirs(os.path.join(plot_output, "trait_cell"))
    layers: list = list(init_score.layers)

    scatter_trait(init_score, output=os.path.join(plot_output, "trait_cell"), title="", columns=plot_columns)
    scatter_trait(
        init_score, output=os.path.join(plot_output, "trait_cell"), title="", layers=layers, columns=plot_columns
    )

    try:
        kde(
            init_score,
            axis=0,
            title="Initialization score with weights",
            output=os.path.join(plot_output, f"init_score_weight_kde")
        )
    except Exception as e:
        log.warn(f"{e}")
        log.warn(f"Can try to improve the version of `seaborn`. `pip install --upgrade seaborn`")

    group_heatmap(adata=init_score, dir_name="heatmap", col_name=clusters, clusters=clusters, plot_output=plot_output)
    map_df_plot(
        adata=init_score,
        trait_cluster_map=trait_cluster_map,
        feature_name="cell",
        clusters=clusters,
        y_name="Initial score",
        column="value",
        width=width,
        plot_output=plot_output
    )

    # Display of Heat Map and Violin Map
    for layer in layers:
        kde(init_score, axis=0, layer=layer, title=layer, output=os.path.join(plot_output, f"{layer}_kde"))
        group_heatmap(
            adata=init_score,
            layer=layer,
            dir_name="heatmap",
            col_name=clusters,
            clusters=clusters,
            plot_output=plot_output
        )
        map_df_plot(
            adata=init_score,
            layer=layer,
            trait_cluster_map=trait_cluster_map,
            feature_name="cell",
            clusters=clusters,
            y_name="Initial score",
            column="value",
            width=width,
            plot_output=plot_output
        )


def cell_cell_plot(
    cc_data: AnnData,
    plot_output: str,
    clusters: str = "clusters",
    is_graph: bool = False
) -> None:
    layers: list = list(cc_data.layers)
    # heatmap
    heatmap_annotation(
        cc_data,
        layer="cell_affinity",
        col_name=clusters,
        row_name=clusters,
        row_legend=True,
        row_anno_label=True,
        col_anno_label=True,
        output=os.path.join(plot_output, "cc_heatmap.png")
    )
    heatmap_annotation(
        cc_data,
        col_name=clusters,
        row_name=clusters,
        row_legend=True,
        row_anno_label=True,
        col_anno_label=True,
        output=os.path.join(plot_output, "cc_heatmap_mknn_weight.png")
    )

    if "cell_mutual_knn" in layers:
        heatmap_annotation(
            cc_data,
            layer="cell_mutual_knn",
            col_name=clusters,
            row_name=clusters,
            row_legend=True,
            row_anno_label=True,
            col_anno_label=True,
            output=os.path.join(plot_output, "cc_heatmap_mknn.png")
        )

    if is_graph:
        # Cell-cell network
        communities_graph(
            adata=cc_data,
            clusters=clusters,
            labels=cc_data.obs[clusters],
            output=os.path.join(plot_output, "cc_weight_graph")
        )

        if "cell_mutual_knn" in layers:
            communities_graph(
                adata=cc_data,
                layer="cell_mutual_knn",
                clusters=clusters,
                labels=cc_data.obs[clusters],
                output=os.path.join(plot_output, "cc_graph")
            )


def data_plot(
    init_score: AnnData,
    cc_data: AnnData,
    trs: AnnData,
    plot_output: str,
    clusters: str = "clusters",
    plot_columns: Tuple[str, str] = ("UMAP1", "UMAP2"),
    trait_cluster_map: dict = None,
    is_graph: bool = False,
    width: float = 8
) -> None:
    # scatter
    scatter_atac(trs, clusters=clusters, output=os.path.join(plot_output, "scATAC_cluster.pdf"), columns=plot_columns)

    kde(
        init_score, axis=0, title="Initial score with weight (scale)",
        output=os.path.join(plot_output, "init_score_weight_scale_kde")
    )

    trs_plot(
        trs=trs,
        plot_output=plot_output,
        clusters=clusters,
        plot_columns=plot_columns,
        trait_cluster_map=trait_cluster_map,
        width=width
    )

    cell_cell_plot(
        cc_data=cc_data,
        plot_output=plot_output,
        clusters=clusters,
        is_graph=is_graph
    )


def trs_plot(
    trs: AnnData,
    plot_output: str,
    clusters: str = "clusters",
    plot_columns: Tuple[str, str] = ("UMAP1", "UMAP2"),
    trait_cluster_map: dict = None,
    width: float = 8
) -> None:
    trs_layers: list = list(trs.layers)

    # plot
    file_method.makedirs(os.path.join(plot_output, "kde"))
    file_method.makedirs(os.path.join(plot_output, "trait_cell"))
    scatter_trait(trs, output=os.path.join(plot_output, "trait_cell"), title="", columns=plot_columns)
    scatter_trait(
        trs,
        output=os.path.join(plot_output, "trait_cell"),
        title="",
        layers=trs_layers,
        columns=plot_columns
    )

    group_heatmap(adata=trs, dir_name="heatmap", col_name=clusters, clusters=clusters, plot_output=plot_output)
    map_df_plot(
        adata=trs,
        feature_name="init_score_weight",
        trait_cluster_map=trait_cluster_map,
        clusters=clusters,
        y_name="Cell score",
        column="value",
        width=width,
        plot_output=plot_output
    )

    try:
        kde(
            adata=trs,
            axis=0,
            title="Initialization score with weights",
            output=os.path.join(plot_output, "kde", f"init_score_weight_kde")
        )
    except Exception as e:
        log.warn(f"{e}")
        log.warn(f"Can try to improve the version of `seaborn`. `pip install --upgrade seaborn`")

    # Display of Heat Map and Violin Map
    for layer in trs_layers:
        group_heatmap(
            adata=trs,
            layer=layer,
            dir_name="heatmap",
            col_name=clusters,
            clusters=clusters,
            plot_output=plot_output
        )
        map_df_plot(
            adata=trs,
            layer=layer,
            feature_name="",
            trait_cluster_map=trait_cluster_map,
            clusters=clusters,
            y_name="Cell score",
            column="value",
            width=width,
            plot_output=plot_output
        )

        try:
            kde(
                adata=trs,
                axis=0,
                layer=layer,
                title=f"Distribution of {layer}",
                output=os.path.join(plot_output, "kde", f"{layer}_kde")
            )
        except Exception as e:
            log.warn(f"{e}")
            log.warn(f"Can try to improve the version of `seaborn`. `pip install --upgrade seaborn`")

        if layer.startswith("run_en"):
            rate_bar_plot(
                adata=trs,
                dir_name="enrichment",
                clusters=clusters,
                layer=layer,
                width=width,
                column="value",
                plot_output=plot_output
            )
