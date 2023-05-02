"""Process news items as YAML."""
from typing import Dict, List, Optional
from pydantic import BaseModel
from enum import Enum
import yaml
import pandas as pd
from pathlib import Path
from data_processing.log import get_logger
from data_processing.console import console
from pydantic_yaml import YamlStrEnum, YamlModel
import datetime

logger = get_logger(__file__)


class Publication(YamlModel):
  """Class for publication information"""

  title: str
  authors: str
  abstract: str
  journal: str
  # date: datetime.datetime
  qualiperf_funding: bool
  pubmed: str
  doi: str
  preprint: bool


class Publications(YamlModel):
  """Class for all publications information"""
  items: List[Publication]


class Other(YamlModel):
  """Class for ohter news information"""

  category: str
  title: str
  authors: str
  abstract: str
  journal: str
  conference: str
  # date: str
  qualiperf_funding: str
  projects: str

class Others(YamlModel):
  """Class for news information"""
  items: List[Other]


def process_news():
    """Process the cleaned news information in yaml entries."""
    news_xlsx = Path(__file__).parent.parent.parent / "assets" / "news" / "qualiperf_news.xlsx"
    dfs: Dict[str, pd.DataFrame] = pd.read_excel(
        news_xlsx, sheet_name=None, comment="#"
    )
    def process_publications(df: pd.DataFrame, is_preprint: bool) -> List[Publication]:
        """Process publications and preprints."""
        # FIXME: remove '\n' in abstracts
        publications: List[Publication] = []
        for k, row in df.iterrows():
            p = Publication(
                title=row["Title"].strip(),
                authors=row["Authors"].strip(),
                abstract=row["Abstract"].strip(),
                journal=row["Journal"].strip(),
                # date=row["Date"],
                qualiperf_funding=row["QuaLiPerf funding/support is acknowledged?"] == "Yes",
                pubmed=row["Pubmed"],
                doi=row["DOI"].strip(),
                preprint=is_preprint,
            )
            console.print(p)
            publications.append(p)
        return publications

    def process_other(df: pd.DataFrame) -> List[Other]:
        """Process other news items."""
        others: List[Other] = []
        for k, row in df.iterrows():
            p = Other(
                category=row["Category"].strip(),
                title=row["Title"].strip(),
                authors=row["Authors"].strip(),
                abstract=row["Abstract"].strip(),
                journal=str(row["Journal"]).strip(),
                # date=row["Date"],
                conference=row["Conference"],
                qualiperf_funding=row["QuaLiPerf funding/support is acknowledged?"] == "Yes",
                projects=row["Related Project(s)"],
            )
            console.print(p)
            others.append(p)
        return others

    # publications
    publications_yaml = Path(__file__).parent.parent.parent / "assets" / "publications.yml"
    publications_info: List[Publication] = process_publications(
        df=dfs["Publications"],
        is_preprint=False,
    )
    publications: Publications = Publications(items=publications_info)
    with open(publications_yaml, "w") as f_yaml:
        yaml_str = publications.yaml()
        f_yaml.write(yaml_str)

    # preprint
    preprints_yaml = Path(__file__).parent.parent.parent / "assets" / "preprints.yml"
    preprints_info: List[Publication] = process_publications(
        df=dfs["Preprints"],
        is_preprint=True,
    )
    preprints: Publications = Publications(items=preprints_info)
    with open(preprints_yaml, "w") as f_yaml:
        yaml_str = preprints.yaml()
        f_yaml.write(yaml_str)

    # other items
    others_yaml = Path(__file__).parent.parent.parent / "assets" / "others.yml"
    others_info: List[Publication] = process_other(
        df=dfs["Other"]
    )
    with open(others_yaml, "w") as f_yaml:
        yaml_str = Others(items=others_info).yaml()
        f_yaml.write(yaml_str)


if __name__ == "__main__":
    process_news()
