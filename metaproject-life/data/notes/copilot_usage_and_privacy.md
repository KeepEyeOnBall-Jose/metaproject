Title: Copilot usage, billing, models, and workspace context
Created: 2025-09-01
Tags: copilot, billing, privacy, dev-environment

Summary

Notes about GitHub Copilot / Copilot Chat billing, quotas, model/version visibility, and what editor/workspace context is sent to the service. Keep this note as a quick reference and link for privacy checks.

Key points

- Billing: Copilot is usually subscription-based (per-user or per-seat). Check GitHub billing pages for invoices and seat counts.
- Quotas: Interactive suggestions are covered by subscription; rate-limits exist but per-request meters are uncommon for consumer plans. Enterprise accounts may have usage dashboards.
- Model/version: Extension version in VS Code and Copilot Chat UI labels indicate the model/variant; check Extension view and chat 'about' sections.
- Context: Copilot uses local file/editor context and conversation history; extension settings control telemetry and workspace usage.

Quick actions

- Inspect extension version in VS Code → Extensions → GitHub Copilot.
- Check GitHub billing: https://github.com/settings/billing or organization billing page.
- Review Copilot settings: https://github.com/settings/copilot and VS Code settings (Cmd+, → search "copilot").

Privacy controls

- Disable workspace file sharing in extension settings for sensitive repos.
- Use separate VS Code profiles or disable the extension in specific workspaces.
- For enterprise-grade control contact GitHub sales/support for private options.

Done: saved as `data/notes/copilot_usage_and_privacy.md`.
