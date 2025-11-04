Title: Dig one level deeper — mantra
Created: 2025-08-26
Tags: mantra, mindset, problem-solving

Mantra

"Always go one level below the current level of abstraction to solve the problem at the current layer." 

Short version: "Dig a little deeper — solid foundations solve surface problems."

Why this helps

- When a bug, design gap, or decision feels fuzzy, the root cause often lives one level deeper (data shape, invariants, or assumptions).
- Understanding the foundation avoids brittle patches and enables simpler, more correct solutions.

Practical uses

- Before coding or designing, ask: "What does this depend on? What assumptions are hidden?"
- When debugging, inspect a level deeper (inputs, types, state) before changing higher-level logic.
- Use as a review checklist item: can you explain the lower-level invariant that must hold?

Quick reminders

- Not an excuse to over-engineer — stop when the deeper level is clear and stable.
- Document discovered invariants in code or tests so future readers don't need to rediscover them.

Done: saved as `data/notes/dig_deeper_mantra.md`.
