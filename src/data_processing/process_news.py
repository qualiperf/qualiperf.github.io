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


class News(YamlModel):
  """Class for news information"""

  title: str
  authors: str
  abstract: str
  journal: str
  # date: str
  qualiperf_funding: str
  pubmed: str
  doi: str


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


if __name__ == "__main__":
    process_news()
