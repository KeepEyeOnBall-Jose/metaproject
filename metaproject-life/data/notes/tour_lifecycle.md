Tour lifecycle: deleted vs archived vs unpublished

Recorded: 2025-08-23

Purpose
- Clarify semantics and lifecycle actions for a tour when it's deleted, archived, or unpublished. Useful for UI, API, retention, and legal/audit requirements.

Definitions
- Active: visible to end users; live records and assets served.
- Unpublished: removed from public listing but still editable by owner; assets retained; no public URLs.
- Archived: read-only snapshot for long-term storage; visible only to admins or via archive view; may be retained for audits; may have reduced availability (moved to cold storage).
- Deleted: intended removal; can be soft-delete (tombstone) or hard-delete (irreversible purge). Deleted items should follow retention and legal holds.

Recommended data model
- status: enum {active, unpublished, archived, deleted}
- deleted_at, archived_at, unpublished_at timestamps
- deleted_by, archived_by, unpublished_by user ids
- tombstone flag and tombstone_reason
- retention_policy_id and legal_hold boolean
- asset_refs: list of content assets with storage location + lifecycle class

Behavior & UX
- Unpublish: remove public routes, keep editing access; quick restore; no asset purge.
- Archive: set read-only, index in archive, move assets to cold storage after grace period; require admin to restore.
- Delete (soft): set tombstone, retain metadata & assets for retention window; provide restore API; disable all public access.
- Delete (hard): after retention window or manual purge; remove assets from storage, delete DB rows, write audit event.

APIs & hooks
- POST /tours/:id/unpublish -> sets status=unpublished
- POST /tours/:id/archive -> sets status=archived
- DELETE /tours/:id -> soft-delete (status=deleted) unless ?hard=true
- background worker: purge_deleted() respects legal_hold and retention_policy
- webhooks: emit events on state changes (unpublished, archived, deleted, purged)

Audit & compliance
- Always record who changed status and timestamps.
- Keep an immutable audit log for legal/forensics.
- Honor legal holds preventing purge.

Recovery & warnings
- Surface clear UX warnings before archive/purge.
- Provide a restore path for soft-deleted and archived items (with permission checks).

Implementation notes
- Use background jobs for asset movement/purge.
- Tag assets with lifecycle class for storage tiering.
- Tests: simulate transitions and retention enforcement, verify webhooks and audit entries.

Tags: tours, lifecycle, archive, delete, retention
