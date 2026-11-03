import sys
from pathlib import Path

# Ensure both backend directory and repo root are in sys.path
_current = Path(__file__).resolve()
_backend_dir = _current.parent.parent
_repo_root = _backend_dir.parent

for _p in (_repo_root, _backend_dir):
    _p_str = str(_p)
    if _p_str not in sys.path:
        sys.path.insert(0, _p_str)
