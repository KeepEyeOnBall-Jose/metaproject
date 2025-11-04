Title: Tour Set (group of tours) concept for MoBo
Created: 2025-08-26
Tags: mobo, backend, tours, orchestration, design

Purpose

Introduce a higher-level entity above a single `tour` called `TourSet` (or `TourGroup`) that groups multiple tours together so the system can manage, pause, resume, and apply policies across the group as a single unit.

Motivation

- Operations: ability to stop/start/scale a collection of tours (for maintenance, experiment rollout, or customer requests).
- Governance: apply access control, billing, or retention policies to a set rather than individually.
- Workflows: batch reprocessing, batch migrations, or group-level monitoring and alerts.

Core model sketch

- TourSet
  - id: uuid
  - name: string
  - owner_id / team_id
  - status: enum (active, paused, draining, archived)
  - policy: JSON/foreign-key to policy table (rate limits, retention)
  - created_at, updated_at

- Tour -> belongs_to -> TourSet (nullable for backward compatibility)

Behaviors & API surface

- Create / Read / Update / Delete TourSet
- Add/Remove tours from a TourSet (bulk operations supported)
- Actions: start, stop, pause, resume, drain
- Query: list tours in a set, count active, health summary
- Notifications: emit events on set-level state changes for downstream systems

Operational semantics

- stop/pause semantics: define whether pause is soft (pause new work) vs hard (stop ongoing processing).
- drain: allow current jobs to finish but block new jobs; useful for graceful shutdown before maintenance.
- consistency: operations should be idempotent and provide a job-id for async operations.

DB & migration notes

- Add nullable `tour_set_id` to `tours` table; backfill with a default set if needed or keep null for legacy tours.
- Create `tour_sets` table with indexes on owner and status.
- Consider an append-only audit log for set-level operations for accountability.

UI & UX

- In MoBo admin UI, add a TourSet detail page with quick actions (pause/resume), list of member tours, and an aggregated health view.
- For CLI/API clients, expose a single `tourset` endpoint and batch endpoints for add/remove.

Edge cases & questions

- What is the maximal size of a TourSet? (scalability concerns)
- How do billing and quotas apply to sets vs tours?
- Access control: who can perform destructive actions on a set?

Next small deliverables (pick one)

- A migration and DB schema PR to add `tour_sets` and `tour_set_id` to `tours` with simple backfill script.
- An API spec (OpenAPI fragment) for TourSet endpoints and async action jobs.
- A small probe script that lists tours without a set to estimate migration size.

Done: saved as `data/notes/tour_set_concept.md`.
