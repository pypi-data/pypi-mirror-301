# -*- coding: UTF-8 -*-

import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from pandas import DataFrame

from ykenan_log import Logger

from scLift.util import path, project_name

log = Logger(f"{project_name}_plot_bubble")


def bubble(
    df: DataFrame,
    x: str,
    y: str,
    hue: str = None,
    size: str = None,
    title: str = None,
    output: path = None,
    show: bool = True
):
    fig, ax = plt.subplots(figsize=(4, 4))

    if title is not None:
        plt.title(title, fontsize=15)

    if size is not None:
        _size_ = df[size].values
        sizes = (np.array(_size_).min(), np.array(_size_).max())
    else:
        sizes = None

    sns.relplot(
        x=x,
        y=y,
        hue=hue,
        size=size,
        sizes=sizes,
        alpha=.5,
        palette="muted",
        height=6,
        data=df
    )

    if output is not None:
        output_pdf = output if output.endswith(".pdf") else f"{output}.pdf"
        # plt.savefig(output_pdf, dpi=300)
        with PdfPages(output_pdf) as pdf:
            pdf.savefig(fig)

    if show:
        plt.show()

    plt.close()
