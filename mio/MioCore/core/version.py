from pathlib import Path

try:  # pragma: py-gte-311
    import tomllib  # pyright: ignore[reportMissingImports]
except ModuleNotFoundError:  # pragma: py-lt-311
    import tomli as tomllib

__version__ = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8")).get("project")["version"]