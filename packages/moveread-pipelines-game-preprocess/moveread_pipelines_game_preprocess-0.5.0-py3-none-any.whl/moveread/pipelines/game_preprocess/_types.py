from typing import Sequence
from dataclasses import dataclass
import robust_extraction2 as re
import moveread.pipelines.preprocess as pre

@dataclass
class Input:
  model: re.ExtendedModel
  imgs: Sequence[str]

@dataclass
class Game:
  model: re.ExtendedModel
  imgIds: Sequence[str]

Output = Sequence[pre.Output]