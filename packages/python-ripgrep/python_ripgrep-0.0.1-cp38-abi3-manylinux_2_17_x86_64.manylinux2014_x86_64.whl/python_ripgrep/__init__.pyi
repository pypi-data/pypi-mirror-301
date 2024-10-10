import enum

class PyArgs:
    def __init__(
        self,
        patterns: list[str],
        paths: list[str] | None = None,
        globs: list[str] | None = None,
        heading: bool | None = None,
        separator_field_context: str | None = None,
        separator_field_match: str | None = None,
        separator_context: str | None = None,
        sort: PySortMode | None = None,
        max_count: int | None = None,
    ): ...

class PySortMode:
    kind: PySortModeKind
    reverse: bool = False

    def __init__(self, kind: PySortModeKind, reverse: bool = False): ...

class PySortModeKind(enum.Enum):
    Path = enum.auto()
    LastModified = enum.auto()
    LastAccessed = enum.auto()
    Created = enum.auto()

def search(args: PyArgs) -> list[str]: ...
def files(args: PyArgs) -> list[str]: ...
