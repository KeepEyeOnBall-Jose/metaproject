#!/usr/bin/env python3
"""Simple manager to record and list open questions for the metaproject.
Usage:
  python3 manager.py add "My question?" --category "life" --notes "context"
  python3 manager.py list --status open
"""
import csv
import os
import argparse
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_PATH = os.path.join(DATA_DIR, "questions.csv")
HEADER = ["id", "question", "category", "created_at", "status", "notes"]


def ensure_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)


def add(question, category="", notes="", status="open"):
    ensure_data()
    uid = str(int(datetime.utcnow().timestamp() * 1000))
    created_at = datetime.utcnow().isoformat() + "Z"
    row = [uid, question, category, created_at, status, notes]
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)
    print(uid)


def list_entries(status=None, limit=None):
    ensure_data()
    with open(CSV_PATH, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if status:
        rows = [r for r in rows if r.get("status") == status]
    if limit:
        rows = rows[: int(limit)]
    for r in rows:
        print(
            f"{r['id']}\t[{r['status']}]\t{r['category']}\t{r['created_at']}\n  {r['question']}\n  notes: {r['notes']}\n"
        )


def main():
    parser = argparse.ArgumentParser(description="Manage metaproject questions")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add")
    p_add.add_argument("question")
    p_add.add_argument("--category", "-c", default="")
    p_add.add_argument("--notes", "-n", default="")

    p_list = sub.add_parser("list")
    p_list.add_argument("--status", "-s", default=None)
    p_list.add_argument("--limit", "-l", default=None)

    args = parser.parse_args()
    if args.cmd == "add":
        add(args.question, args.category, args.notes)
    elif args.cmd == "list":
        list_entries(args.status, args.limit)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
