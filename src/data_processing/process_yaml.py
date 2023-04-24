"""
Process yaml files for webpage.
Moves the assets to _data
"""
from typing import Dict, List, Optional
from pydantic import BaseModel

import yaml
from pathlib import Path


class Person(BaseModel):
  """Class for person information"""

  id: str
  name: str
  title: Optional[str]
  role: str  # ["PI", "Fellow", "Alumni"]
  group: str
  affiliations: List[str]
  orcid: str
  websites: Optional[List[str]]
  image: str
  description: str
  projects: List[str]
  tags: List[str]
  publications: Optional[List[str]]


def clean_entry(d: Dict) -> List[Person]:
    """Parse and clean entries."""
    print(d)
    persons = []
    for pdata in d:
        p = Person(**pdata)
        persons.append(p)
    return persons


def process_persons():
    """Process persons data for validation"""
    people_dir = Path(__file__).parent.parent.parent / "assets" / "persons"

    for k, p in enumerate(sorted(Path(people_dir).glob('*.yml'))):
        print(p)
        # read yaml
        with open(p, "r") as f_yaml:
            try:
                d = yaml.load(f_yaml, Loader=yaml.FullLoader)
                clean_entry(d)
            except Exception as err:
                print(f"ERROR in 'file://{p}'")
                raise err


if __name__ == "__main__":
    process_persons()


