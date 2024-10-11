# -*- coding: UTF-8 -*-

import os
from typing import Tuple, Union

from pandas import DataFrame
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

from ykenan_log import Logger

from scLift.util import path, project_name

log = Logger(f"{project_name}_plot_box")


def box_base(
    df: DataFrame,
    value: str = "value",
    x_name: str = "Cell type",
    y_name: str = "value",
    clusters: str = "clusters",
    palette: Union[Tuple, list] = None,
    width: float = 4,
    height: float = 4,
    bottom: float = 0.3,
    line_width: float = 0.5,
    title: str = None,
    is_sort: bool = True,
    order_names: list = None,
    output: path = None,
    show: bool = True
) -> None:
    if output is None and not show:
        log.info(f"At least one of the `output` and `show` parameters is required")
    else:
        # judge
        # noinspection DuplicatedCode
        df_columns = list(df.columns)

        if value not in df_columns:
            log.error(f"The `value` ({value}) parameter must be in the `df` parameter data column name ({df_columns})")
            raise ValueError(
                f"The `value` ({value}) parameter must be in the `df` parameter data column name ({df_columns})"
            )

        fig, ax = plt.subplots(figsize=(width, height))
        # noinspection DuplicatedCode
        fig.subplots_adjust(bottom=bottom)

        if title is not None:
            plt.title(title)

        group_columns = [clusters]

        new_df: DataFrame = df.groupby(group_columns, as_index=False)[value].median()

        if "color" in df_columns:
            new_df_color: DataFrame = df.groupby(group_columns, as_index=False)["color"].first()

            new_df = new_df.merge(new_df_color, how="left", on=clusters)

        # sort
        if is_sort:
            new_df.sort_values([value], ascending=False, inplace=True)
            y_names: Union[list, None] = list(new_df[clusters])
        else:
            new_df.index = new_df[clusters]
            if order_names is not None:
                y_names: list = order_names
            else:
                y_names = new_df[clusters]

        # scatter
        ax = sns.boxplot(
            data=df,
            x=clusters,
            y=value,
            order=y_names,
            boxprops={'linewidth': line_width},
            whiskerprops={'linewidth': line_width},
            medianprops={'linewidth': line_width},
            palette=palette if palette is not None else (new_df["color"] if "color" in df_columns else None)
        )

        # set coordinate
        # noinspection DuplicatedCode
        ax.set_xticklabels(labels=y_names, rotation=65)
        plt.xlabel(x_name)
        plt.ylabel(y_name)

        if output is not None:
            output_pdf = output if output.endswith(".pdf") else f"{output}.pdf"
            # plt.savefig(output_pdf, dpi=300)
            with PdfPages(output_pdf) as pdf:
                pdf.savefig(fig)

        if show:
            plt.show()

        plt.close()


def box_trait(
    trait_df: DataFrame,
    trait_name: str = "All",
    trait_column_name: str = "id",
    value: str = "value",
    clusters: str = "clusters",
    x_name: str = "Cell type",
    y_name: str = "value",
    palette: Tuple = None,
    width: float = 4,
    height: float = 4,
    line_width: float = 0.1,
    bottom: float = 0.3,
    is_sort: bool = True,
    order_names: list = None,
    title: str = None,
    output: path = None,
    show: bool = True
) -> None:
    """
    Violin plot of cell scores for traits/diseases
    :param order_names:
    :param is_sort:
    :param line_width:
    :param palette:
    :param bottom:
    :param height:
    :param x_name:
    :param clusters:
    :param width:
    :param title:
    :param y_name:
    :param value:
    :param trait_column_name:
    :param trait_df: data
    :param trait_name: trait/disease name or All, 'All' show all traits/diseases
    :param output: Image output path
    :param show: Whether to display pictures
    :return: None
    """

    data: DataFrame = trait_df.copy()

    def trait_plot(trait_: str, atac_cell_df_: DataFrame) -> None:
        """
        show plot
        :param trait_: trait name
        :param atac_cell_df_:
        :return: None
        """
        log.info("Plotting box {}".format(trait_))
        # get gene score
        trait_score = atac_cell_df_[atac_cell_df_[trait_column_name] == trait_]
        # Sort gene scores from small to large
        box_base(
            df=trait_score,
            value=value,
            x_name=x_name,
            y_name=y_name,
            width=width,
            palette=palette,
            height=height,
            bottom=bottom,
            is_sort=is_sort,
            order_names=order_names,
            line_width=line_width,
            clusters=clusters,
            title=f"{title} {trait_}" if title is not None else title,
            output=os.path.join(output, f"cell_{trait_}_score_box.pdf") if output is not None else None,
            show=show
        )

    # noinspection DuplicatedCode
    trait_list = list(set(data['id']))
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
            trait_plot(trait, trait_df)
    else:
        trait_plot(trait_name, trait_df)
