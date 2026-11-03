import sys
import os
import uvicorn
from pathlib import Path

# Add workspace to sys.path
_current = Path(__file__).resolve().parent
_repo_root = _current.parent

for _p in (_repo_root, _current):
    _p_str = str(_p)
    if _p_str not in sys.path:
        sys.path.insert(0, _p_str)

from backend.app.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", settings.PORT))
    print(f"Starting Personal Finance API on http://{host}:{port}")
    uvicorn.run(
        "backend.app.main:app",
        host=host,
        port=port,
        reload=False,
    )
