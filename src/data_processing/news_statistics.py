"""Calculates statistics of news for presentation."""
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd
import jinja2

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
        "Related Project(s)": "Projects",
        "Related Project(s)": "Projects",
        "Authors from QuaLiPerF": "Authors Qualiperf",
    }

    console.rule(title="publications", style="white")
    df_publications = dfs["Publications"]
    df_ifs = dfs["IF"]
    df_publications = df_publications.merge(df_ifs, how="left", on="Journal_ID")
    df_publications.rename(columns=columns_dict, inplace=True)
    df_publications = df_publications[[
        "Title",
        "Authors",
        # "Abstract",
        "Journal",
        "IF",
        "Date",
        "Qualiperf",
        "Authors Qualiperf",
        "Projects",
        "Pubmed",
        "DOI",
        "Journal_ID",
    ]]
    console.print(df_publications)

    console.rule(title="preprints", style="white")
    df_preprints = dfs["Preprints"]
    df_preprints.rename(columns=columns_dict, inplace=True)
    df_preprints = df_preprints[df_preprints.Published == "No"]
    df_preprints = df_preprints[[
        "Title",
        "Authors",
        # "Abstract",
        "Journal",
        "Date",
        "Qualiperf",
        "Authors Qualiperf",
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
        # "Abstract",
        "Journal",
        "Date",
        "Qualiperf",
        "Authors Qualiperf",
        "Projects",
    ]]
    console.print(df_submissions)

    console.rule(title="theses", style="white")
    df_theses = dfs["Theses"]
    df_theses.rename(columns=columns_dict, inplace=True)
    df_theses = df_theses[[
        "Category",
        "Title",
        "Authors",
        # "Abstract",
        "Date",
        "Qualiperf",
        "Authors Qualiperf",
        "Projects",
    ]]
    console.print(df_theses)

    console.rule(title="posters", style="white")
    df_posters = dfs["Posters"]
    df_posters.rename(columns=columns_dict, inplace=True)
    df_posters = df_posters[[
        "Title",
        "Authors",
        # "Abstract",
        "Conference",
        "Date",
        "Qualiperf",
        "Authors Qualiperf",
        "Projects",
    ]]
    console.print(df_posters)

    console.rule(title="presentations", style="white")
    df_presentations = dfs["Presentations"]
    df_presentations.rename(columns=columns_dict, inplace=True)
    df_presentations = df_presentations[[
        "Title",
        "Authors",
        # "Abstract",
        "Conference",
        "Date",
        "Qualiperf",
        "Authors Qualiperf",
        "Projects",
    ]]
    console.print(df_presentations)

    # FIXME: process after updated excel sheet
    df_others = dfs["Others"]
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
        "theses": df_theses,
        "posters": df_posters,
        "presentations": df_presentations,
        "others": df_others,
    }

    # calculate statistics
    console.rule(title="statistics", style="white")
    types = [
        "publications",
        "preprints",
        "submissions",
        "theses",
        "posters",
        "presentations",
        "others",
    ]
    dataframes = [
        df_publications,
        df_preprints,
        df_submissions,
        df_theses,
        df_posters,
        df_presentations,
        df_others,
    ]
    counts = [len(df.Qualiperf) for df in dataframes]
    qualiperf_yes = [(df.Qualiperf == "Yes").values.sum() for df in dataframes]
    qualiperf_no = [(df.Qualiperf != "Yes").values.sum() for df in dataframes]

    df_statistics = pd.DataFrame(
        data={
            "type": types,
            "count": counts,
            "qualiperf acknowledged": qualiperf_yes,
            "qualiperf not acknowledged": qualiperf_no,
        }
    )
    console.print(df_statistics)
    results["statistics"] = df_statistics

    # serialize to excel
    with pd.ExcelWriter(xlsx_out) as writer:
        df_statistics.to_excel(writer, sheet_name="statistics", index=False)
        df_publications.to_excel(writer, sheet_name="publications", index=False)
        df_preprints.to_excel(writer, sheet_name="preprints", index=False)
        df_submissions.to_excel(writer, sheet_name="submissions", index=False)
        df_theses.to_excel(writer, sheet_name="theses", index=False)
        df_posters.to_excel(writer, sheet_name="posters", index=False)
        df_presentations.to_excel(writer, sheet_name="presentations", index=False)
        df_others.to_excel(writer, sheet_name="other", index=False)

    console.print(f"News: file://{xlsx_out}")

    return results


def visualize_publications_matplotlib(df: pd.DataFrame, fig_path: Path):
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


def create_html_report(output_dir: Path, dfs: Dict[str, pd.DataFrame]) -> None:
    """Write all tables as interactive DataTables in HTML.

    Use Jinja2 for rendering.
    """
    # create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # template environment
    template_dir = Path(__file__).parent
    template_file = "report_template.html"
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        extensions=[],
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_file)

    # resolve contexts
    context: Dict[str, Any] = {}
    console.print(dfs.keys())
    for key, df in dfs.items():
        table = df.to_html(
            table_id=key,
            border=0,
            index=False,
        )
        context[f"table_{key}"] = table
        context[f"count_{key}"] = len(df)

    # render all contexts:
    out_path = output_dir / f"qualiperf_report.html"
    html_str = str(template.render(context))
    with open(out_path, "w") as f_html:
        f_html.write(html_str)

    console.print(f"News: file://{out_path}")


def run_all() -> None:
    """Create all tables and figures."""
    results_dir: Path = Path(__file__).parent.parent.parent / "assets" / "news" / "results"
    xlsx_in = Path(__file__).parent.parent.parent / "assets" / "news" / "qualiperf_news.xlsx"
    xlsx_out = results_dir / "qualiperf_statistics.xlsx"
    dfs: Dict[str, pd.DataFrame] = create_statistics(xlsx_in=xlsx_in, xlsx_out=xlsx_out)

    report_dir = Path(__file__).parent / "report"
    fig_publications = report_dir / "fig_publications.png"
    visualize_publications_matplotlib(df=dfs["publications"], fig_path=fig_publications)
    create_html_report(
        output_dir=report_dir,
        dfs=dfs,
    )

    # FIXME: cumulative count diagrams for achievements
    # FIXME: graph for interactions between publications/preprints


if __name__ == "__main__":
    run_all()

