import sys
from typing import Any, List, Optional

endl = object()


class Cout:
    def __init__(self, line: Optional[List[str]] = None) -> None:
        self.line: List[str] = line or []

    def __lshift__(self, other: Any) -> Optional["Cout"]:
        if other is endl:
            sys.stdout.write("".join(self.line))
            sys.stdout.write("\n")
            sys.stdout.flush()
            return None
        return Cout(self.line + [str(other)])

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Cout) and self.line == other.line


cout = Cout()
