"""Package entry for fast_task_manager (src layout).

This package lives under `src/` so builds and editable installs behave
consistently (`pip install -e .` will pick up the package from `src/`).
"""

__all__ = [
    "crud",
    "database",
    "gui",
    "main",
    "models",
    "schemas",
]
