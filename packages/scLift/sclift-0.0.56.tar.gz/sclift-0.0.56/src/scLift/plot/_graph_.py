# -*- coding: UTF-8 -*-

import networkx as nx
import numpy as np
from anndata import AnnData
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as plt

from scLift.util import (
    matrix_data,
    collection,
    path,
    list_index,
    to_dense,
    type_20_colors,
    type_50_colors,
    check_adata_get,
    project_name
)

from ykenan_log import Logger

log = Logger(f"{project_name}_plot_graph")


def graph(
    data: matrix_data,
    labels: collection = None,
    node_size: int = 50,
    is_font: bool = False,
    output: path = None,
    show: bool = True
) -> None:
    """
    plot graph from adjacency matrix
    :param data: input data
    :param labels: Label of data node
    :param node_size: Size of data node
    :param is_font: Is there a word on the data node
    :param output: Image output path
    :param show: Whether to display pictures
    :return: None
    """
    if output is None and not show:
        log.info(f"At least one of the `output` and `show` parameters is required")
    else:
        plt.figure(figsize=(4, 4), dpi=150)

        # Determine whether it is a square array
        if data.shape[0] != data.shape[1]:
            log.error("The input data must be a square matrix.")
            raise ValueError("The input data must be a square matrix.")

        # set labels
        labels_dict = {}

        if labels is not None:

            if data.shape[0] != np.asarray(labels).size:
                log.error(
                    f"The number of input data nodes {data.shape[0]} and the number of "
                    f"labels {np.asarray(labels).size} must be consistent"
                )
                raise ValueError(
                    f"The number of input data nodes {data.shape[0]} and the number of "
                    f"labels {np.asarray(labels).size} must be consistent"
                )

            labels_dict: dict = dict(zip(range(len(labels)), labels))

        rows, cols = np.where(data == 1)
        edges = zip(rows.tolist(), cols.tolist())
        gr = nx.Graph(name="Cell-cell graph")
        gr.add_edges_from(edges)
        pos = nx.spring_layout(gr, k=0.15, iterations=35, seed=2023)

        options: dict = {
            "node_color": "black",
            "node_size": node_size,
            "linewidths": 0,
            "width": 0.1
        }

        if is_font:
            if labels is not None:
                nx.draw(gr, pos=pos, labels=labels_dict, **options)
            else:
                nx.draw(gr, pos=pos, **options)
        else:
            nx.draw(gr, pos=pos, labels={}, **options)

        if show:
            plt.show()

        if output is not None:
            plt.savefig(output if output.endswith(".pdf") else f"{output}.pdf")

        plt.close()


def communities_graph(
    adata: AnnData,
    labels: collection,
    layer: str = None,
    clusters: str = "clusters",
    width: float = 4,
    height: float = 4,
    title: str = None,
    node_size: float = 2.0,
    line_widths: float = 0.001,
    start_color_index: int = 0,
    color_step_size: int = 0,
    output: path = None,
    show: bool = True
):
    if output is None and not show:
        log.info(f"At least one of the `output` and `show` parameters is required")
    else:
        log.info("Start cell-cell network diagram")

        new_data = check_adata_get(adata=adata, layer=layer)

        # adjust matrix
        adj_matrix = to_dense(new_data.X)
        communities, node_labels = list_index(labels)

        df = new_data.obs.copy()

        __hue_order__ = list(np.sort(list(set(df[clusters]))))

        type_colors = type_20_colors if len(__hue_order__) <= 20 else type_50_colors

        log.info("Get position")
        color_index = 0
        g = nx.from_numpy_array(adj_matrix)
        partition = [0 for _ in range(g.number_of_nodes())]
        for c_i, nodes in enumerate(communities):
            for i in nodes:
                partition[i] = type_colors[start_color_index + color_index * color_step_size + c_i]
            color_index += 1

        pos = nx.spring_layout(g)

        pos1 = [p[0] for p in pos.values()]
        pos2 = [p[1] for p in pos.values()]
        new_data.obs["pos1"] = pos1
        new_data.obs["pos2"] = pos2

        fig = plt.figure(figsize=(width, height))

        if title is not None:
            plt.title(title)

        plt.axis("off")

        nx.draw_networkx_nodes(
            g,
            pos=pos,
            node_size=node_size,
            node_color=partition,
            linewidths=line_widths
        )
        # nodes.set_edgecolor("b")
        nx.draw_networkx_edges(
            g,
            pos=pos,
            node_size=node_size,
            edge_color=(0, 0, 0, 0.3),
            width=line_widths
        )

        # noinspection DuplicatedCode
        if output is not None:
            output_pdf = output if output.endswith(".pdf") else f"{output}.pdf"
            # plt.savefig(output_pdf, dpi=300)
            with PdfPages(output_pdf) as pdf:
                pdf.savefig(fig)

        if show:
            plt.grid(True)
            plt.show()

        plt.close()
