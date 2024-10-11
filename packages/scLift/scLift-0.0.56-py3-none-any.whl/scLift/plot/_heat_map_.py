# -*- coding: UTF-8 -*-

from anndata import AnnData
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backends.backend_pdf import PdfPages
from PyComplexHeatmap import HeatmapAnnotation, anno_simple, ClusterMapPlotter, anno_label
from matplotlib.colors import ListedColormap
from pandas import DataFrame
import seaborn as sns
from ykenan_log import Logger

from scLift.util import path, type_20_colors, type_50_colors, project_name

log = Logger(f"{project_name}_plot_heat_map")


def heatmap_annotation(
    adata: AnnData,
    layer: str = None,
    width: float = 4,
    height: float = 4,
    title: str = None,
    label: str = "value",
    row_name: str = None,
    col_name: str = None,
    row_anno_label: bool = False,
    col_anno_label: bool = False,
    row_anno_text: bool = False,
    col_anno_text: bool = False,
    row_legend: bool = False,
    col_legend: bool = False,
    row_show_names: bool = False,
    col_show_names: bool = False,
    row_cluster: bool = False,
    col_cluster: bool = False,
    cluster_method: str = "average",
    cluster_metric: str = "correlation",
    row_names_side: str = "left",
    col_names_side: str = "bottom",
    top: float = 0.05,
    right: float = 0.15,
    bottom: float = 0.05,
    left: float = 0.05,
    label_size: float = 17,
    fontsize: float = 17,
    is_position: bool = False,
    x_label_rotation: float = 75,
    y_label_rotation: float = 0,
    row_color_start_index: int = 0,
    col_color_start_index: int = 10,
    x_name: str = None,
    y_name: str = None,
    cmap: str = "Oranges",
    is_sort: bool = True,
    show: bool = True,
    output: path = None
):
    if output is None and not show:
        log.info(f"At least one of the `output` and `show` parameters is required")
    else:
        log.info("Start plotting the heatmap")
        # noinspection DuplicatedCode
        fig, ax = plt.subplots(figsize=(width, height))
        data = adata.copy()

        # judge layers
        if layer is not None:

            if layer not in list(data.layers):
                log.error("The `layer` parameter needs to include in `adata.layers`")
                raise ValueError(f"The `{layer}` parameter needs to include in `adata.layers`")

            data.X = data.layers[layer]

        if is_sort:
            data = data[data.obs.sort_values(row_name).index, data.var.sort_values(col_name).index]

        # DataFrame
        df: DataFrame = data.to_df()

        if is_position:
            plt.subplots_adjust(left=left, right=1 - right, top=1 - top, bottom=bottom)

        row_anno: DataFrame = data.obs.copy()

        col_anno: DataFrame = data.var.copy()

        if row_name is not None:
            row_colors = type_20_colors[row_color_start_index:] if len(
                list(set(row_anno[row_name]))
            ) <= 20 else type_50_colors[row_color_start_index:]
        else:
            row_colors = "cmap50"

        if col_name is not None:
            col_colors = type_20_colors[col_color_start_index:] if len(
                list(set(col_anno[col_name]))
            ) <= 20 else type_50_colors[col_color_start_index:]
        else:
            col_colors = "cmap50"

        if title is not None:
            plt.title(title)

        # noinspection PyTypeChecker
        row_ha = HeatmapAnnotation(
            label=anno_label(
                row_anno[row_name], cmap=ListedColormap(row_colors), merge=True
            ) if row_anno_label else None,
            Category=anno_simple(
                row_anno[row_name],
                cmap=ListedColormap(row_colors),
                legend=row_legend,
                add_text=row_anno_text,
                text_kws=dict(color="black", rotation=0),
            ) if row_name is not None else None,
            axis=0,
            verbose=0,
            label_kws=dict(color="white", rotation=90, horizontalalignment="left")
        )

        col_ha_args = {"rotation": 90}
        # noinspection PyTypeChecker
        col_ha = HeatmapAnnotation(
            label=anno_label(
                col_anno[col_name], cmap=ListedColormap(col_colors), merge=True, **col_ha_args
            ) if col_anno_label else None,
            Category=anno_simple(
                col_anno[col_name],
                cmap=ListedColormap(col_colors),
                add_text=col_anno_text,
                legend=col_legend
            ) if col_name is not None else None,
            axis=1,
            verbose=0,
            label_side='left',
            label_kws=dict(color="white", rotation=0, horizontalalignment="right")
        )

        """
        It is worth noting here that, `row_cluster_metric="correlation"`, When the default parameter 
        `row_cluster_metric` in method `ClusterMapPlotter` is passed into method `distance.pdist`, 
        that is `metric='correlation'`, and this method derives from this 
        `https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.distance.pdist.html`,
        it can be inferred that there is a division formula in one step, which may result in the possibility of `NA`.
        
        For example, in this scATAC-seq data, if there are two or more traits without any intersection, 
        the denominator will appear as zero.
        
        Therefore, use the `"median"` value for parameter `row_cluster_method`
        Therefore, use the `"euclidean"` value for parameter `row_cluster_metric`
        """

        ClusterMapPlotter(
            data=df,
            top_annotation=col_ha if col_name is not None else None,
            left_annotation=row_ha if row_name is not None else None,
            label=label,
            row_cluster_method=cluster_method,
            row_cluster_metric=cluster_metric,
            col_cluster_method=cluster_method,
            col_cluster_metric=cluster_metric,
            show_rownames=row_show_names,
            show_colnames=col_show_names,
            row_names_side=row_names_side,
            col_names_side=col_names_side,
            xticklabels_kws=dict(labelrotation=x_label_rotation, labelcolor='black', labelsize=label_size),
            yticklabels_kws=dict(labelrotation=y_label_rotation, labelcolor='black', labelsize=label_size),
            cmap=cmap,
            xlabel=x_name,
            ylabel=y_name,
            xlabel_kws=dict(color='black', fontsize=fontsize),
            ylabel_kws=dict(color='black', fontsize=fontsize),
            col_cluster=col_cluster,
            row_cluster=row_cluster,
            col_dendrogram=col_cluster,
            row_dendrogram=row_cluster
        )

        # noinspection DuplicatedCode
        if output is not None:

            if output.endswith(".png") or output.endswith(".jpg"):
                plt.savefig(output, dpi=300)
            else:
                output_pdf = output if output.endswith(".pdf") else f"{output}.pdf"

                with PdfPages(output_pdf) as pdf:
                    pdf.savefig(fig)

        if show:
            plt.show()

        plt.close()


def heatmap(
    adata: AnnData,
    layer: str = None,
    width: float = 4,
    height: float = 4,
    annot: bool = False,
    square: bool = True,
    is_cluster: bool = False,
    cmap: str = "Oranges",
    line_widths: float = 1,
    fmt: str = ".2f",
    rotation: float = 65,
    x_name: str = None,
    y_name: str = None,
    output: path = None,
    show: bool = True
) -> None:
    if output is None and not show:
        log.info(f"At least one of the `output` and `show` parameters is required")
    else:
        # noinspection DuplicatedCode
        fig, ax = plt.subplots(figsize=(width, height))
        data = adata.copy()

        # judge layers
        if layer is not None:

            if layer not in list(data.layers):
                log.error("The `layer` parameter needs to include in `adata.layers`")
                raise ValueError("The `layer` parameter needs to include in `adata.layers`")

            data.X = data.layers[layer]

        # DataFrame
        log.info(f"to DataFrame")
        df: DataFrame = data.to_df()
        # seaborn
        heat_map: Axes = sns.clustermap(data=df, square=square, annot=annot, cmap=cmap, fmt=fmt) \
            if is_cluster else \
            sns.heatmap(data=df, square=square, annot=annot, cmap=cmap, linewidths=line_widths, fmt=fmt)

        if not is_cluster:
            plt.subplots_adjust(left=0, bottom=0)
            plt.setp(
                heat_map.get_xticklabels(), rotation=65, ha="right", rotation_mode="anchor"
            )
        else:
            # noinspection PyUnresolvedReferences
            plt.setp(heat_map.ax_heatmap.get_xticklabels(), rotation=rotation)

        if x_name is not None:
            plt.xlabel(x_name, fontsize=15)

        if y_name is not None:
            plt.ylabel(y_name, fontsize=15)

        # noinspection DuplicatedCode
        if output is not None:

            if output.endswith(".png") or output.endswith(".jpg"):
                plt.savefig(output, dpi=300)
            else:
                output_pdf = output if output.endswith(".pdf") else f"{output}.pdf"

                if is_cluster:
                    plt.savefig(output_pdf, dpi=300)
                else:
                    with PdfPages(output_pdf) as pdf:
                        pdf.savefig(fig)

        if show:
            plt.show()

        plt.close()
