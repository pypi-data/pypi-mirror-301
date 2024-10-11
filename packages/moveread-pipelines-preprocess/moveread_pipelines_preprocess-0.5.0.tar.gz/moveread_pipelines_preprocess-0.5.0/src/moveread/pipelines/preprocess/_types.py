from typing import Literal
from dataclasses import dataclass
import pure_cv as vc
from moveread.core import Image
import robust_extraction2 as re

@dataclass
class Output:
  image: Image
  boxes: list[str]

@dataclass
class BaseInput:
  img: str
  model: re.ExtendedModel

@dataclass
class Uncorrected(BaseInput):
  tag: Literal['uncorrected'] = 'uncorrected'

@dataclass
class BaseCorrected(BaseInput):
  corrected: str
  corners: vc.Corners

@dataclass
class Corrected(BaseCorrected):
  tag: Literal['corrected'] = 'corrected'

@dataclass
class BaseExtracted(BaseCorrected):
  contours: vc.Contours
  contoured: str

@dataclass
class Extracted(BaseExtracted):
  tag: Literal['extracted'] = 'extracted'

@dataclass
class Selected(BaseCorrected):
  contours: vc.Contours
  tag: Literal['selected'] = 'selected'