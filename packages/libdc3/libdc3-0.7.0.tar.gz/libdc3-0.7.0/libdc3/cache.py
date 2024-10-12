import importlib.metadata
from pathlib import Path


project_name = importlib.metadata.metadata("libdc3")["Name"]
cache_directory = Path.home() / ".cache" / project_name
cache_directory.mkdir(parents=True, exist_ok=True)
