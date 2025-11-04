#!/usr/bin/env python3
"""kill_port_process.py

Kills processes using specific ports.

This script is intended to be run from the repository root or any location. It
safely terminates processes using the specified ports.

Exit codes:
 - 0 : success (processes killed or none found)
 - 1 : setup error (unexpected error)

Usage:
  ./kill_port_process.py --port PORT

Notes:
 - Uses lsof and kill commands to terminate processes
 - Only kills processes owned by the current user
"""

import sys
import argparse
import subprocess
import os


def get_process_using_port(port: int):
    """Find the process using a specific port using lsof."""
    try:
        result = subprocess.run(
            ["lsof", "-i", f":{port}"], capture_output=True, text=True, timeout=5
        )

        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split("\n")
            if len(lines) > 1:  # First line is header
                parts = lines[1].split()
                if len(parts) >= 2:
                    return {
                        "command": parts[0],
                        "pid": parts[1],
                        "user": parts[2] if len(parts) > 2 else "unknown",
                    }
    except (
        subprocess.TimeoutExpired,
        subprocess.SubprocessError,
        FileNotFoundError,
    ) as e:
        print(f"Warning: Could not check port {port}: {e}", file=sys.stderr)

    return None


def kill_process_on_port(port: int):
    """Kill the process using the specified port."""
    proc_info = get_process_using_port(port)
    if not proc_info:
        print(f"No process found using port {port}")
        return True

    pid = proc_info["pid"]
    command = proc_info["command"]
    user = proc_info["user"]

    print(f"Found process using port {port}:")
    print(f"  Command: {command}")
    print(f"  PID: {pid}")
    print(f"  User: {user}")

    # Only kill processes owned by current user
    current_user = os.getlogin()
    if user != current_user:
        print(f"Warning: Process owned by {user}, not {current_user}. Skipping.")
        return False

    try:
        # Try graceful termination first
        print(f"Sending SIGTERM to PID {pid}...")
        result = subprocess.run(
            ["kill", pid], capture_output=True, text=True, timeout=5
        )

        if result.returncode == 0:
            print(f"Successfully sent SIGTERM to PID {pid}")
            return True
        else:
            print(f"Failed to send SIGTERM to PID {pid}: {result.stderr}")
            return False

    except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
        print(f"Error killing process {pid}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Kill processes using specific ports")
    parser.add_argument(
        "--port", type=int, required=True, help="Port number to free up"
    )

    args = parser.parse_args()

    print(f"Attempting to kill process using port {args.port}...")

    success = kill_process_on_port(args.port)

    if success:
        print(f"Successfully handled port {args.port}")
        sys.exit(0)
    else:
        print(f"Failed to handle port {args.port}")
        sys.exit(1)


if __name__ == "__main__":
    main()
