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

logger = get_logger(__file__)

class Person(YamlModel):
  """Class for person information"""

  id: str
  firstname: str
  lastname: str
  title: Optional[str]
  role: Role
  groups: List[str]
  affiliations: List[str]
  orcid: str
  websites: Optional[List[str]]
  image: str
  description: str
  projects: List[Project]
  tags: List[Tag]
  publications: Optional[List[str]]


def process_news():
    """Process the cleaned news information in yaml entries."""
    news_xlsx = Path(__file__).parent.parent.parent / "assets" / "news" / "qualiperf_news.xlsx"
    dfs: Dict[str, pd.DataFrame] = pd.read_excel(
        news_xlsx, sheet_name=None, comment="#"
    )
    for key, df in dfs.items():
        if key.startswith("Form"):
            continue
        console.rule(title=key, style="white", align="left")
        console.print(df)




if __name__ == "__main__":

