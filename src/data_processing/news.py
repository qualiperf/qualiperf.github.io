"""Process news items as YAML."""
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import pandas as pd
from pathlib import Path
from data_processing.log import get_logger
from data_processing.console import console
from pydantic_yaml import to_yaml_str

logger = get_logger(__file__)


class Publication(BaseModel):
  """Class for publication information."""

  title: str
  authors: str
  abstract: str
  journal: str
  # date: datetime.datetime
  qualiperf_funding: bool
  pubmed: str
  doi: str
  preprint: bool


class Publications(BaseModel):
  """Class for all publications information"""
  items: List[Publication]


class Other(BaseModel):
  """Class for ohter news information"""

  category: str
  title: str
  authors: str
  abstract: str
  journal: str
  conference: Optional[str]
  # date: str
  qualiperf_funding: bool
  projects: str

class Others(BaseModel):
  """Class for news information"""
  items: List[Other]


def create_news_yaml() -> None:
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
            # console.print(row)
            p = Publication(
                title=row["Title"].strip(),
                authors=row["Authors"].strip(),
                abstract=row["Abstract"].strip(),
                journal=row["Journal"].strip(),
                # date=row["Date"],
                qualiperf_funding=row["QuaLiPerf funding/support is acknowledged?"] == "Yes",
                pubmed=str(row["Pubmed"]),
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
            console.print(row)
            p = Other(
                category=row["Category"].strip(),
                title=row["Title"].strip(),
                authors=row["Authors"].strip(),
                abstract=row["Abstract"].strip(),
                journal=str(row["Journal"]).strip(),
                # date=row["Date"],
                conference=str(row["Conference"]),
                qualiperf_funding=row["QuaLiPerf funding/support is acknowledged?"] == "Yes",
                projects=row["Related Project(s)"],
            )
            console.print(p)
            others.append(p)
        return others

    # publications
    for key in ["publication", "preprint", "other"]:

        yaml_path = Path(__file__).parent.parent.parent / "assets" / f"{key}s.yml"

        if key in {"publication", "preprint"}:
            items_info: List[Any] = process_publications(
                df=dfs[f"{key.title()}s"],
                is_preprint=(key == "preprint"),
            )
            items: Publications = Publications(items=items_info)
        elif key == "other":
            items_info: List[Any] = process_other(
                df=dfs[f"{key.title()}s"],
            )
            items: Others = Others(items=items_info)

        with open(yaml_path, "w") as f_yaml:
            yaml_str = to_yaml_str(items)
            f_yaml.write(yaml_str)


if __name__ == "__main__":
    create_news_yaml()
