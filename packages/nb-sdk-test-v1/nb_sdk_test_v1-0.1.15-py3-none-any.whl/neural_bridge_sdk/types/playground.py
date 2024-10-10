from typing import Dict, List

from pydantic import BaseModel


class Sheet(BaseModel):
  columns: List[str]


class SynthesizeRequest(BaseModel):
  use_case_def: str
  num_output: int
  tables: Dict[str, Sheet] = {}
