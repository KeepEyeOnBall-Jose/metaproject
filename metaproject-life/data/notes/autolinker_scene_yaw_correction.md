Title: Autolinker — scene yaw correction (virtual north) unresolved
Created: 2025-08-26
Tags: autolinker, data-integrity, geometry, scene, yaw, major

Problem

Many images now have a "corrected virtual north" (scene yaw correction != 0). We have not fully handled the consequences for linking logic. This affects anchor coordinates, matching heuristics, and the global alignment of scenes — MAJOR IMPACT.

Why it's important

- Links assume a consistent coordinate frame; yaw correction changes that frame and can break existing links or produce incorrect link placements.
- Affected systems: linking algorithms, tour rendering, location-based heuristics, and any downstream consumers that assume raw orientation.

Immediate investigation checklist

- Find code paths that compute or assume scene yaw==0. Grep for yaw, north, orientation, corrected_north, scene_yaw across the autolinker codebase.
- Identify data sources that store the correction (image metadata, sidecar JSON, database fields) and sample a few corrected images.
- Create a failing test that reproduces an incorrect link when scene yaw correction != 0.
- Decide canonical coordinate transformation: apply correction at ingestion vs. apply per-link transform during linking.

Mitigation options

- Normalize coordinate frames at ingestion (recommended if possible): store canonical coordinates.
- Make linking transforms yaw-aware: include scene_yaw in link scoring and geometry transforms.
- Add a compatibility layer to detect legacy tours and reprocess links.

Deliverables

- A small detection script that lists how many scenes/images have non-zero yaw corrections.
- A PR that either normalizes coordinates or updates the linking code to be yaw-aware with unit tests.

Done: saved as `data/notes/autolinker_scene_yaw_correction.md`.
