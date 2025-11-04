#!/usr/bin/env python3
"""check_port_usage.py

Checks what processes are using specific ports (default: 8000, 5173, 11434, 1234).

This script is intended to be run from the repository root or any location. It
uses system commands to check port usage safely.

Exit codes:
 - 0 : success (found processes or none found)
 - 1 : setup error (unexpected error)

Usage:
  ./check_port_usage.py [--ports PORT1,PORT2,...]

Notes:
 - Uses lsof command to check port usage
 - Checks common ports used by the question-interface project
"""

import sys
import argparse
import subprocess


def get_process_using_port(port: int):
    """Find the process using a specific port using lsof."""
    try:
        # Use lsof to find process using the port
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
                        "fd": parts[3] if len(parts) > 3 else "unknown",
                        "type": parts[4] if len(parts) > 4 else "unknown",
                        "device": parts[5] if len(parts) > 5 else "unknown",
                        "size_off": parts[6] if len(parts) > 6 else "unknown",
                        "node": parts[7] if len(parts) > 7 else "unknown",
                        "name": " ".join(parts[8:]) if len(parts) > 8 else "unknown",
                    }
    except (
        subprocess.TimeoutExpired,
        subprocess.SubprocessError,
        FileNotFoundError,
    ) as e:
        print(f"Warning: Could not check port {port}: {e}", file=sys.stderr)

    return None


def main():
    parser = argparse.ArgumentParser(description="Check processes using specific ports")
    parser.add_argument(
        "--ports",
        type=str,
        default="8000,5173,11434,1234",
        help="Comma-separated list of ports to check",
    )

    args = parser.parse_args()

    try:
        ports = [int(p.strip()) for p in args.ports.split(",")]
    except ValueError as e:
        print(f"ERROR: Invalid port specification: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Checking processes using ports: {', '.join(map(str, ports))}")
    print("-" * 80)

    found_any = False
    for port in ports:
        proc_info = get_process_using_port(port)
        if proc_info:
            found_any = True
            print(f"Port {port}:")
            print(f"  Command: {proc_info['command']}")
            print(f"  PID: {proc_info['pid']}")
            print(f"  User: {proc_info['user']}")
            print(f"  Details: {proc_info['name']}")
            print()
        else:
            print(f"Port {port}: No process found")
            print()

    if not found_any:
        print("No processes found using the specified ports.")
    else:
        print("Found processes using one or more ports.")

    sys.exit(0)


if __name__ == "__main__":
    main()
