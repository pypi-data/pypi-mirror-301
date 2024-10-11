# -*- coding: UTF-8 -*-

import os

from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pandas import DataFrame
import seaborn as sns

from ykenan_log import Logger

from scLift.util import path, project_name

log = Logger(f"{project_name}_plot_violin")


def violin_base(
    df: DataFrame,
    value: str = "value",
    y_name: str = "value",
    clusters: str = "clusters",
    width: float = 8,
    title: str = None,
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

        fig, ax = plt.subplots(figsize=(width, 4))
        fig.subplots_adjust(bottom=0.3)

        if title is not None:
            plt.title(title)

        # 排序
        df_mean: DataFrame = df.groupby(clusters, as_index=False)[value].median()
        df_mean.sort_values([value], ascending=False, inplace=True)
        y_names: list = list(df_mean[clusters])

        # scatter
        ax = sns.violinplot(data=df, x=clusters, y=value, order=y_names)

        # set coordinate
        # noinspection DuplicatedCode
        ax.set_xticklabels(labels=y_names, rotation=65, fontsize=15)
        plt.xlabel('Cell type', fontsize=15)
        plt.ylabel(y_name, fontsize=15)

        if output is not None:
            output_pdf = output if output.endswith(".pdf") else f"{output}.pdf"
            # plt.savefig(output_pdf, dpi=300)
            with PdfPages(output_pdf) as pdf:
                pdf.savefig(fig)

        if show:
            plt.show()

        plt.close()


def violin_trait(
    trait_df: DataFrame,
    trait_name: str = "All",
    trait_column_name: str = "id",
    value: str = "value",
    clusters: str = "clusters",
    y_name: str = "value",
    width: float = 8,
    title: str = None,
    output: path = None,
    show: bool = True
) -> None:
    """
    Violin plot of cell scores for traits/diseases
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
        log.info("Plotting violin {}".format(trait_))
        # get gene score
        trait_score = atac_cell_df_[atac_cell_df_[trait_column_name] == trait_]
        # Sort gene scores from small to large
        violin_base(
            df=trait_score,
            value=value,
            width=width,
            clusters=clusters,
            y_name=y_name,
            title=f"{title} {trait_}" if title is not None else title,
            output=os.path.join(output, f"cell_{trait_}_score_violin.pdf") if output is not None else None,
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
