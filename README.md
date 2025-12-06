# Fast Task Manager

A FastAPI backend with NiceGUI frontend for managing tasks efficiently.

## Features

- **REST API** built with FastAPI for task management
- **Web UI** built with NiceGUI for interactive task viewing and editing
- **SQLite Database** for persistent task storage
- **Python 3.13** with modern async/await patterns

## Quick Start

### Prerequisites

- Nix with flakes support
- direnv (for automatic environment loading)

### Setup

1. Clone the repository
2. Allow direnv to load the environment:
   ```bash
   cd fast_task_manager
   direnv allow
   ```

3. Start both the API and GUI:
   ```bash
   ./start.sh
   ```

The application will automatically launch:
- **API**: http://127.0.0.1:8000 (with interactive docs at `/docs`)
- **GUI**: http://127.0.0.1:8080

### Manual Start

If you prefer to run services separately:

```bash
# Start API only
uvicorn fast_task_manager.main:app --port 8000

# Start GUI only (in another terminal)
python -c 'from fast_task_manager.gui import run_gui; run_gui()'
```

## Project Structure

```
fast_task_manager/
├── src/fast_task_manager/
│   ├── main.py          # FastAPI application and routes
│   ├── gui.py           # NiceGUI frontend
│   ├── crud.py          # Database operations
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   └── database.py      # Database configuration
├── flake.nix            # Nix flake for development environment
├── .envrc               # direnv configuration
└── pyproject.toml       # Project metadata and dependencies
```

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `pydantic` - Data validation
- `nicegui` - Web UI framework
- `httpx` - HTTP client

## Development

The development environment is automatically loaded when you enter the directory (via direnv + flake.nix). The environment creates a Python 3.13 virtual environment with all dependencies installed.

## Stopping the Application

Press `CTRL+C` to stop the application. Both API and GUI will shut down gracefully.
