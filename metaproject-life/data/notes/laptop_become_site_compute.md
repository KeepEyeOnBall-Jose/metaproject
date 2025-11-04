Title: Make my laptop part of site compute
Created: 2025-08-23
Tags: infrastructure, goals, laptop, compute

Short goal

I want my personal laptop to act as one of the compute nodes for the site (run jobs, testing, light CI, or scheduled compute tasks) while maintaining security and not disrupting normal use.

Why

- Add flexible, low-cost compute capacity for short/ephemeral workloads.
- Use for lightweight CI, data collection, experiment runs, or scheduled tasks.

Constraints / non-goals

- Not intended to be production critical. No putting sensitive customer data without hard controls.
- Avoid impacting laptop battery life or developer productivity.

Small checklist (first steps)

- Inventory & baseline
  - Record hostname, OS details, free disk, RAM, battery health.
  - Note current SSH keys and remote access methods.

- Security hardening
  - Create a dedicated system user (eg. "compute") with limited permissions.
  - Ensure SSH uses key-based auth only; add a jump-host or VPN if needed.
  - Configure firewall rules to restrict incoming ports (ufw / pfctl / macOS built-in firewall).
  - Enable full-disk encryption and backups for personal data.

- Runtime & orchestration
  - Install lightweight runtime: Docker (or podman), Git, Python/Rust toolchain as needed.
  - Consider systemd services (or launchd on macOS) to run containerized agents safely.
  - Tag/label the node in inventory (e.g., "laptop/jose/low-priority").

- Workload constraints
  - Limit CPU and IO for compute tasks (cgroups, Docker cpus, nice/ionice) to avoid lag.
  - Schedule heavy runs only while plugged in and on LAN.

- Monitoring & safety nets
  - Add low-overhead monitoring (Prometheus node exporter or simple heartbeats to central server).
  - Add automatic pause/disable when battery < X% or on specific Wi‑Fi networks.

- Automation & onboarding
  - Script onboarding steps in a single repo/playbook for reproducibility.
  - Add a simple health-check endpoint or heartbeat file to confirm availability.

Quick follow-ups

- Decide which workloads are allowed (tests, ETL, model training small, backups?).
- Decide ownership & emergency kill-switch (a central toggle to stop or drain node).
- If ok, write an onboarding script and a small systemd/launchd service template.

Notes

- Keep strict separation between personal files and compute runtimes (use containers or dedicated user + separate data paths).
- Prioritize non-invasive, reversible changes.

Done: saved as `data/notes/laptop_become_site_compute.md`.
