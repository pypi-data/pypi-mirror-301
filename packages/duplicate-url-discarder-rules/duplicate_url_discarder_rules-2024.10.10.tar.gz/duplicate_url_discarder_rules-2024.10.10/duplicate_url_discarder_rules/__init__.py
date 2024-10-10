from glob import glob
from pathlib import Path
from typing import List, Optional

_current_path = Path(__file__).parent.resolve()
RULE_PATHS: Optional[List[str]] = glob(str(_current_path / "**/*.json"), recursive=True)


__version__ = "2024.10.10"
