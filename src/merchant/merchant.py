from typing import Any, Dict, NamedTuple
from pathlib import Path
from merchant.database import DatabaseHandler


class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int
