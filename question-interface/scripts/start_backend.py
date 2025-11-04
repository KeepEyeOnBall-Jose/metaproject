#!/usr/bin/env python3
"""start_backend.py

Starts the FastAPI backend (uvicorn) for development with proper cleanup.

This script is intended to be run from the repository root or any location. It
uses absolute paths so it does not rely on an activated shell virtual
environment. It will forward SIGINT and SIGTERM to the uvicorn process and
ensure the process is terminated on exit.

Exit codes:
 - 0 : success (uvicorn exited normally or was stopped)
 - 1 : setup error (missing paths or unexpected error)
 - >1: uvicorn's exit code

Usage:
  ./start_backend.py

Notes:
 - Uses absolute paths to the workspace Python interpreter and backend directory.
 - Adjust the PYTHON_EXEC or WORKDIR constants if your environment differs.
"""

import os
import sys
import subprocess
import signal
import time

# --- Configuration (ABSOLUTE paths) ---------------------------------------
WORKDIR = "/Users/jose/metaproject/question-interface/backend"
PYTHON_EXEC = "/Users/jose/metaproject/.venv/bin/python"

UVICORN_CMD = [
    PYTHON_EXEC,
    "-m",
    "uvicorn",
    "main:app",
    "--reload",
    "--host",
    "0.0.0.0",
    "--port",
    "8000",
]
# ---------------------------------------------------------------------------


def _error(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def main():
    try:
        if not os.path.isdir(WORKDIR):
            _error(f"Backend workdir not found: {WORKDIR}")
        if not os.path.isfile(PYTHON_EXEC):
            _error(f"Python executable not found: {PYTHON_EXEC}")

        print("Starting backend: uvicorn main:app on http://0.0.0.0:8000")
        print("Working directory:", WORKDIR)
        print("Using Python:", PYTHON_EXEC)

        proc = subprocess.Popen(UVICORN_CMD, cwd=WORKDIR)

        def _terminate(signum, frame):
            print(
                f"Received signal {signum}, shutting down uvicorn (pid={proc.pid})...",
                flush=True,
            )
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
            sys.exit(0)

        signal.signal(signal.SIGINT, _terminate)
        signal.signal(signal.SIGTERM, _terminate)

        # Monitor the child process and forward its exit code
        while True:
            ret = proc.poll()
            if ret is not None:
                print(f"uvicorn exited with code {ret}")
                sys.exit(ret if isinstance(ret, int) else 0)
            time.sleep(0.5)

    except Exception as exc:
        _error(f"Unhandled exception while starting backend: {exc}")


if __name__ == "__main__":
    main()
