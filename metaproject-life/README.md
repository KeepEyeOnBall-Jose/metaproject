metaproject-life

Quick scaffold to track open questions for your life/projects.

Files:
- data/questions.csv    # CSV store of questions
- manager.py            # CLI to add/list entries

Usage examples:

Add a question:

```bash
python3 manager.py add "What should I tackle next week?" --category "work" --notes "related to repo X"
```

List questions:

```bash
python3 manager.py list
python3 manager.py list --status open
```

Next steps: I'll ask you one question at a time and append each answer to the tracker.
