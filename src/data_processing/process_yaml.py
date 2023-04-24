"""
Process yaml files for webpage.
Moves the assets to _data
"""
from typing import Dict, List, Optional
from pydantic import BaseModel
from enum import Enum
import yaml
from pathlib import Path
from data_processing.log import get_logger
from data_processing.console import console
from pydantic_yaml import YamlStrEnum, YamlModel

logger = get_logger(__file__)




class Role(YamlStrEnum):
    PI = 'PI'
    FELLOW = 'Fellow'
    STUDENT_ASSISTANT = 'Student assistant'
    TECHNICAL_ASSISTANT = 'Technical assistant'
    ALUMNI = 'Alumni'
    ASSOCIATED = 'Associated'


class Project(YamlStrEnum):
    QUALIPERF = 'QuaLiPerF'
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"
    P6 = "P6"
    P7 = "P7"
    P8 = "P8"
    P9 = "P9"
    DMP = 'DMP'
    COORDINATION = 'Coordination'
    SIMLIVA = 'SimLivA'
    STEAPKMOD = 'Stea-PK Mod'
    ATLAS = "ATLAS"


class Tag(YamlStrEnum):
    EXPERIMENTS = 'Experiments'
    MODELING = 'Modeling'
    CLINICS = 'Clinics'
    DATA_MANAGEMENT = 'Data management'
    DATA_INTEGRATION = 'Data integration'


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

class Persons(YamlModel):
  """Class for all person information"""
  persons: List[Person]


def clean_entry(d: Dict) -> List[Person]:
    """Parse and clean entries."""

    persons = []
    for pdata in d:
        name_tokens = pdata.pop("name").split(" ")
        firstname = " ".join(name_tokens[:-1])
        lastname = name_tokens[-1]
        pdata["firstname"] = firstname
        pdata["lastname"] = lastname
        p = Person(**pdata)
        console.print(p)
        # console.print(p.yaml())

        persons.append(p)

    return persons


def process_persons(persons_dir: Path) -> Persons:
    """Process persons data for validation"""

    all_persons: List[Person] = []
    for k, p in enumerate(sorted(Path(persons_dir).glob('*.yml'))):
        console.rule(style="white")
        print(p)
        # read yaml
        with open(p, "r") as f_yaml:
            try:
                d = yaml.load(f_yaml, Loader=yaml.FullLoader)
                pid = p.stem
                did = d[0].get("id", None)
                if pid != did:
                    logger.error(f"yaml id '{pid}.yaml' does not match 'id={did}")
                persons: List[Person] = clean_entry(d)
                all_persons += persons

            except Exception as err:
                logger.error(f"error in 'file://{p}'")
                raise err

    persons = Persons(persons=all_persons)
    return persons


if __name__ == "__main__":
    persons_dir = Path(__file__).parent.parent.parent / "assets" / "persons"
    persons_yaml = Path(__file__).parent.parent.parent / "assets" / "persons.yml"
    persons: Persons = process_persons(persons_dir=persons_dir)
    yaml_str = persons.yaml()
    with open(persons_yaml, "w") as f_yaml:
        f_yaml.write(yaml_str)
