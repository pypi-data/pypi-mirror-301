from typing import Dict, List

from pydantic import BaseModel


class Sheet(BaseModel):
  columns: List[str]


class SynthesizeRequest(BaseModel):
  use_case_def: str
  num_output: int
  tables: Dict[str, Sheet] = {}


class OutputRequest(BaseModel):
  queries: List[str]
  use_case_def: List[str]
  tables: List[Dict[str, Sheet]] = []


class ExampleRow(BaseModel):
  input: str
  plan: str
  output: str
