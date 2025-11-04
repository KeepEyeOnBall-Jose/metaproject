#!/usr/bin/env python3
"""start_frontend.py

Starts the React frontend (Vite) development server.

This script is intended to be run from the repository root or any location. It
uses absolute paths so it does not rely on an activated shell virtual
environment. It will forward SIGINT and SIGTERM to the vite process and
ensure the process is terminated on exit.

Exit codes:
 - 0 : success (vite exited normally or was stopped)
 - 1 : setup error (missing paths or unexpected error)
 - >1: vite's exit code

Usage:
  ./start_frontend.py

Notes:
 - Uses absolute paths to the workspace Node.js and frontend directory.
 - Adjust the NODE_EXEC or WORKDIR constants if your environment differs.
"""

import os
import sys
import subprocess
import signal
import time

# --- Configuration (ABSOLUTE paths) ---------------------------------------
WORKDIR = "/Users/jose/metaproject/question-interface/frontend"
NODE_EXEC = "/opt/homebrew/bin/node"

VITE_CMD = [
    NODE_EXEC,
    "./node_modules/.bin/vite",
    "--host",
    "0.0.0.0",
    "--port",
    "5173",
]
# ---------------------------------------------------------------------------


def _error(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def main():
    try:
        if not os.path.isdir(WORKDIR):
            _error(f"Frontend workdir not found: {WORKDIR}")
        if not os.path.isfile(NODE_EXEC):
            _error(f"Node.js executable not found: {NODE_EXEC}")

        print("Starting frontend: vite --host 0.0.0.0 --port 5173")
        print("Working directory:", WORKDIR)
        print("Using Node.js:", NODE_EXEC)

        proc = subprocess.Popen(VITE_CMD, cwd=WORKDIR)

        def _terminate(signum, frame):
            print(
                f"Received signal {signum}, shutting down vite (pid={proc.pid})...",
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
                print(f"vite exited with code {ret}")
                sys.exit(ret if isinstance(ret, int) else 0)
            time.sleep(0.5)

    except Exception as exc:
        _error(f"Unhandled exception while starting frontend: {exc}")


if __name__ == "__main__":
    main()
