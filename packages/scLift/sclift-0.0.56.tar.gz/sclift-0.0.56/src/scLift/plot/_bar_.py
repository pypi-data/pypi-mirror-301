# -*- coding: UTF-8 -*-

import os
from typing import Tuple

import numpy as np
from pandas import DataFrame

import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from statannotations.Annotator import Annotator

from ykenan_log import Logger

from scLift.util import path, collection, plot_color_types, project_name

log = Logger(f"{project_name}_plot_bar")


def bar(
    ax_x: collection,
    ax_y: collection,
    x_name: str = None,
    y_name: str = None,
    title: str = None,
    color: str = "#70b5de",
    text_color: str = "#000205",
    width: float = 4,
    height: float = 4,
    bottom: float = 0,
    text_left_move: float = 0.1,
    output: path = None,
    show: bool = True
):
    if output is None and not show:
        log.info(f"At least one of the `output` and `show` parameters is required")
    else:
        fig, ax = plt.subplots(figsize=(width, height))
        fig.subplots_adjust(bottom=bottom)

        if title is not None:
            plt.title(title)

        ax_x = np.array(ax_x).astype(str)
        ax.bar(ax_x, ax_y, color=color)

        if x_name is not None:
            ax.set_xlabel(x_name)

        if y_name is not None:
            ax.set_ylabel(y_name)

        ax.set_xticklabels(labels=list(ax_x), rotation=65)

        # Draw numerical values
        for i, v in enumerate(list(ax_y)):
            plt.text(
                x=i - text_left_move,
                y=0.03 if v < 0.03 else v / 2,
                s=str(round(v, 3)),
                rotation=90,
                color=text_color
            )

        if output is not None:
            output_pdf = output if output.endswith(".pdf") else f"{output}.pdf"
            # plt.savefig(output_pdf, dpi=300)
            with PdfPages(output_pdf) as pdf:
                pdf.savefig(fig)

        if show:
            plt.show()

        plt.close()


def two_bar(
    ax_x: collection,
    ax_y: Tuple,
    x_name: str = None,
    y_name: str = None,
    legend: Tuple = ("1", "2"),
    color: Tuple = ("#2e6fb7", "#f7f7f7"),
    text_color: str = "#000205",
    width: float = 4,
    height: float = 4,
    bottom: float = 0,
    text_left_move: float = 0.15,
    title: str = None,
    output: path = None,
    show: bool = True
):
    if output is None and not show:
        log.info(f"At least one of the `output` and `show` parameters is required")
    else:
        fig, ax = plt.subplots(figsize=(width, height))
        fig.subplots_adjust(bottom=bottom)

        if title is not None:
            plt.title(title)

        ax_x = np.array(ax_x).astype(str)
        ax.bar(ax_x, ax_y[0], label=legend[0], color=color[0])
        ax.bar(ax_x, ax_y[1], bottom=ax_y[0], label=legend[1], color=color[1])

        ax.legend()

        if x_name is not None:
            ax.set_xlabel(x_name)

        if y_name is not None:
            ax.set_ylabel(y_name)

        ax.set_xticklabels(labels=list(ax_x), rotation=65)

        # Draw numerical values
        for i, v in enumerate(list(ax_y[0])):
            plt.text(
                x=i - text_left_move,
                y=0.03 if v < 0.03 else v / 2,
                s=str(round(v, 3)),
                rotation=90,
                color=text_color
            )

        if output is not None:
            output_pdf = output if output.endswith(".pdf") else f"{output}.pdf"
            # plt.savefig(output_pdf, dpi=300)
            with PdfPages(output_pdf) as pdf:
                pdf.savefig(fig)

        if show:
            plt.show()

        plt.close()


def class_bar(
    df: DataFrame,
    value: str = "rate",
    by: str = "value",
    clusters: str = "clusters",
    color: Tuple = ("#2e6fb7", "#f7f7f7"),
    x_name: str = "Cell type",
    y_name: str = "Enrichment ratio",
    legend: Tuple = ("Enrichment", "Conservative"),
    text_color: str = "#000205",
    width: float = 4,
    height: float = 4,
    bottom: float = 0,
    title: str = None,
    text_left_move: float = 0.15,
    output: path = None,
    show: bool = True
):
    if output is None and not show:
        log.info(f"At least one of the `output` and `show` parameters is required")
    else:

        df1 = df[df[by] == 1]
        df2 = df[df[by] == 0]

        # Sort
        df1 = df1.sort_values([value], ascending=False)
        df2 = df2.sort_values([value])

        two_bar(
            ax_x=df1[clusters],
            ax_y=(df1[value], df2[value]),
            x_name=x_name,
            y_name=y_name,
            legend=legend,
            width=width,
            height=height,
            color=color,
            text_color=text_color,
            bottom=bottom,
            text_left_move=text_left_move,
            title=title,
            output=output,
            show=True
        )


def bar_trait(
    trait_df: DataFrame,
    trait_name: str = "All",
    trait_column_name: str = "id",
    value: str = "rate",
    clusters: str = "clusters",
    x_name: str = "Cell type",
    y_name: str = "Enrichment ratio",
    color: Tuple = ("#2e6fb7", "#f7f7f7"),
    legend: Tuple = ("Enrichment", "Conservative"),
    text_color: str = "#000205",
    width: float = 4,
    height: float = 4,
    bottom: float = 0,
    title: str = None,
    text_left_move: float = 0.15,
    output: path = None,
    show: bool = True
):
    def trait_plot(trait_: str, cell_df_: DataFrame) -> None:
        """
        show plot
        :param trait_: trait name
        :param cell_df_:
        :return: None
        """
        log.info("Plotting bar {}".format(trait_))
        # get gene score
        trait_score = cell_df_[cell_df_[trait_column_name] == trait_]
        # Sort gene scores from small to large
        class_bar(
            df=trait_score,
            value=value,
            clusters=clusters,
            title=f"{title} {trait_}" if title is not None else title,
            color=color,
            legend=legend,
            width=width,
            x_name=x_name,
            y_name=y_name,
            height=height,
            bottom=bottom,
            text_left_move=text_left_move,
            text_color=text_color,
            output=os.path.join(output, f"cell_{trait_}_enrichment_bar.pdf") if output is not None else None,
            show=show
        )

    trait_list = list(set(trait_df[trait_column_name]))
    # judge trait
    if trait_name != "All" and trait_name not in trait_list:
        log.error(
            f"The {trait_name} trait/disease is not in the trait/disease list {trait_list}, "
            f"Suggest modifying the {trait_column_name} parameter information"
        )
        raise ValueError(
            f"The {trait_name} trait/disease is not in the trait/disease list {trait_list}, "
            f"Suggest modifying the {trait_column_name} parameter information"
        )

    # plot
    if trait_name == "All":
        for trait in trait_list:
            trait_plot(trait_=trait, cell_df_=trait_df)
    else:
        trait_plot(trait_name, trait_df)


def bar_significance(
    df: DataFrame,
    x: str = "x_index",
    y: str = "value",
    x_name: str = "ToDs",
    y_name: str = "Score",
    hue: str = "labels",
    hue_order: list = None,
    anchor: str = None,
    legend: str = None,
    legend_list: list = None,
    width: float = 4,
    height: float = 4,
    legend_gap: float = 1.15,
    line_width: float = 0.5,
    start_color_index: int = 0,
    color_step_size: int = 0,
    color_type: str = "set",
    x_deviation: float = 0.02,
    y_deviation: float = 0.02,
    anno: bool = False,
    anno_fontsize: float = 15,
    colors: list = None,
    title: str = None,
    output: path = None,
    show: bool = True
) -> None:

    if output is None and not show:
        log.info(f"At least one of the `output` and `show` parameters is required")
    else:

        fig, ax = plt.subplots(figsize=(width, height))

        if legend_list is not None:
            new_data: DataFrame = df[df[hue].isin(legend_list)].copy()
        else:
            new_data: DataFrame = df.copy()

        if legend is None:
            legend = "category"

        new_data.loc[:, legend] = new_data[hue].astype(str)

        new_data_columns = list(new_data.columns)

        hue_types = hue_order if hue_order is not None else list(set(new_data[legend]))

        # noinspection DuplicatedCode
        if colors is not None:
            palette = colors
        else:
            if "color" in new_data_columns:
                palette = new_data["color"]
            else:
                palette = []

                for i in range(len(hue_types)):
                    palette.append(plot_color_types[color_type][start_color_index + i * color_step_size + i])

        ax = sns.barplot(
            data=new_data,
            x=x,
            y=y,
            hue=legend,
            hue_order=hue_order,
            ci="sd",
            capsize=.1,
            errwidth=line_width,
            errcolor="k",
            ax=ax,
            palette=palette,
            **{"edgecolor": "k", "linewidth": line_width}
        )

        if anno:
            for p in ax.patches:
                y_value = p.get_height()
                height = p.get_height() / 2 - y_deviation
                height = 0.03 if height < 0.03 else height
                x = p.get_x() + p.get_width() / 2 + x_deviation
                ax.annotate(
                    f'{y_value:.2f}',
                    (x, height),
                    textcoords="offset points",
                    ha='center',
                    va='bottom',
                    rotation=90,
                    fontsize=anno_fontsize
                )

        if anchor is not None:

            # Add p value
            box_pairs: list = []

            x_list = list(np.unique(new_data[x]))
            class_list = list(np.unique(new_data[legend]))

            if anchor not in class_list:
                log.error(f"`anchor` ({anchor}) is not in the `df[hue]` ({class_list})")
                raise ValueError(f"`anchor` ({anchor}) is not in the `df[hue]` ({class_list})")

            class_list.remove(anchor)

            for x_ele in x_list:

                for class_ele in class_list:
                    box_pairs.append(((x_ele, anchor), (x_ele, class_ele)))

            annotator = Annotator(ax=ax, data=new_data, x=x, y=y, hue=legend, pairs=box_pairs)
            annotator.configure(test='t-test_ind', text_format='star', line_height=0.03, line_width=1)
            annotator.apply_and_annotate()

        ax.tick_params(which='major', direction='in', length=3, width=1.0, bottom=False)

        for spine in ["top", "left", "right"]:
            ax.spines[spine].set_visible(False)

        ax.spines['bottom'].set_linewidth(2)
        ax.grid(axis='y', ls='--', c='gray')
        ax.set_axisbelow(True)

        plt.legend(loc='upper left', bbox_to_anchor=(0.0, legend_gap), ncol=2)

        if title is not None:
            plt.title(title)

        if x_name is not None:
            plt.xlabel(x_name)

        if y_name is not None:
            plt.ylabel(y_name, rotation=90)

        if output is not None:
            output_pdf = output if output.endswith(".pdf") else f"{output}.pdf"
            # plt.savefig(output_pdf, dpi=300)
            with PdfPages(output_pdf) as pdf:
                pdf.savefig(fig)

        if show:
            plt.show()

        plt.close()
