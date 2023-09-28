"""Calculates statistics of news for presentation."""
from pathlib import Path
from typing import Dict, List
import pandas as pd

from data_processing.console import console

import matplotlib
from matplotlib import pyplot as plt

SMALL_SIZE = 12
MEDIUM_SIZE = 15
BIGGER_SIZE = 25

matplotlib.rc('font', size=SMALL_SIZE)          # controls default text sizes
matplotlib.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
matplotlib.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
matplotlib.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
matplotlib.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
matplotlib.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
matplotlib.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

def create_statistics(xlsx_in: Path, xlsx_out: Path) -> Dict[str, pd.DataFrame]:
    """Creates tables for presentation."""
    dfs: Dict[str, pd.DataFrame] = pd.read_excel(
        xlsx_in, sheet_name=None, comment="#"
    )

    columns_dict = {
        "QuaLiPerf funding/support is acknowledged?": "Qualiperf",
        "Related Project(s)": "Projects"
    }

    # Process publications
    # ---------------------
    console.rule(title="publications", style="white")
    df_publications = dfs["Publications"]
    df_ifs = dfs["IF"]
    df_publications = df_publications.merge(df_ifs, how="left", on="Journal_ID")
    df_publications.rename(columns=columns_dict, inplace=True)
    df_publications = df_publications[[
        "Title",
        "Authors",
        "Journal",
        "IF",
        "Date",
        "Qualiperf",
        "Projects",
        "Pubmed",
        "DOI",
        "Journal_ID",
    ]]
    console.print(df_publications)

    console.rule(title="preprints", style="white")
    df_preprints = dfs["Preprints"]
    df_preprints.rename(columns=columns_dict, inplace=True)
    df_preprints = df_preprints[[
        "Title",
        "Authors",
        "Journal",
        "Date",
        "Qualiperf",
        "Projects",
        "Pubmed",
        "DOI",
    ]]
    console.print(df_preprints)

    console.rule(title="submissions", style="white")
    df_submissions = dfs["Submissions"]
    df_submissions.rename(columns=columns_dict, inplace=True)
    df_submissions = df_submissions[[
        "Title",
        "Authors",
        "Journal",
        "Date",
        "Qualiperf",
        "Projects",
    ]]
    console.print(df_submissions)

    # FIXME: process after updated excel sheet
    df_others = dfs["Other"]
    df_others.rename(columns=columns_dict, inplace=True)
    df_others = df_others[[
        "Title",
        "Authors",
        "Journal",
        "Date",
        "Qualiperf",
        "Projects",
    ]]
    results: Dict[str, pd.DataFrame] = {
        "publications": df_publications,
        "preprints": df_preprints,
        "submissions": df_submissions,
        "others": df_others,
    }

    # calculate statistics
    console.rule(title="statistics", style="white")
    types = [
        "publications",
        "preprints",
        "submissions",
        "others",
    ]
    counts = [
        len(df_publications.Qualiperf),
        len(df_preprints.Qualiperf),
        len(df_submissions.Qualiperf),
        len(df_others.Qualiperf),
    ]
    qualiperf_yes = [
        (df_publications.Qualiperf == "Yes").values.sum(),
        (df_preprints.Qualiperf == "Yes").values.sum(),
        (df_submissions.Qualiperf == "Yes").values.sum(),
        (df_others.Qualiperf == "Yes").values.sum(),
    ]
    qualiperf_no = [
        (df_publications.Qualiperf == "No").values.sum(),
        (df_preprints.Qualiperf == "No").values.sum(),
        (df_submissions.Qualiperf == "No").values.sum(),
        (df_others.Qualiperf == "No").values.sum(),
    ]
    df_statistics = pd.DataFrame(
        data={
            "type": types,
            "count": counts,
            "qualiperf acknowledged": qualiperf_yes,
            "qualiperf not acknowledged": qualiperf_no,
        }
    )
    console.print(df_statistics)

    # serialize to excel
    with pd.ExcelWriter(xlsx_out) as writer:
        df_statistics.to_excel(writer, sheet_name="statistics", index=False)
        df_publications.to_excel(writer, sheet_name="publications", index=False)
        df_preprints.to_excel(writer, sheet_name="preprints", index=False)
        df_submissions.to_excel(writer, sheet_name="submissions", index=False)
        df_others.to_excel(writer, sheet_name="other", index=False)

    return results


def visualize_publications(df: pd.DataFrame, fig_path: Path):
    """Visualize publications."""

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(5, 5), dpi=300)
    fig.suptitle("Qualiperf publications")

    ax1.set_xlabel("Date", fontdict={"weight": "bold"})
    ax1.set_ylabel("Impact Factor", fontdict={"weight": "bold"})

    # FIXME: add preprints in different symbol

    dfs = [
        # Filter IF = 0
        df[(df.Qualiperf == "Yes") & (df.IF > 0)],
        df[(df.Qualiperf == "No") & (df.IF > 0)]
    ]
    colors = ["tab:blue", "tab:orange"]
    labels = ["Qualiperf: Yes", "Qualiperf: No"]

    for k, df in enumerate(dfs):
        ax1.plot(
            df.Date, df.IF,
            linestyle="",
            marker="o",
            markersize=12,
            alpha=0.7,
            markeredgecolor="black",
            color=colors[k],
            label=labels[k],
        )
        ax1.set_yscale("log")
        # annotate Jornals
        for index, row in df.iterrows():
            ax1.annotate(
                row.Journal_ID, xy=(row.Date, row.IF),
                fontsize="xx-small",
                alpha=0.8,
            )

    # rotate labels
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)

    ax1.legend(loc=2, prop={'size': 8}, frameon=True)
    plt.show()
    fig.savefig(fig_path, bbox_inches="tight")


if __name__ == "__main__":
    xlsx_in = Path(__file__).parent.parent.parent / "assets" / "news" / "qualiperf_news.xlsx"
    xlsx_out = Path(__file__).parent.parent.parent / "assets" / "news" / "qualiperf_statistics.xlsx"
    dfs: Dict[str, pd.DataFrame] = create_statistics(xlsx_in=xlsx_in, xlsx_out=xlsx_out)

    fig_publications = Path(__file__).parent.parent.parent / "assets" / "news" / "qualiperf_publications.png"
    visualize_publications(df=dfs["publications"], fig_path=fig_publications)

    # FIXME: cumulative count diagrams for achievements
