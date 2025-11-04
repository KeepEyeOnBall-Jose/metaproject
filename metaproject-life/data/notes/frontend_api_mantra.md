Title: Mantra — Don't implement frontends in Python; use an API + JS frontend
Created: 2025-08-26
Tags: mantra, frontend, api, fastapi, javascript, architecture

Statement

Do not implement frontends in Python. Build a proper API (FastAPI recommended) and consume it from a dedicated JavaScript frontend (React, Svelte, Vue) for a better developer experience, performance, and UX.

Why

- Python excels at backend logic, data processing, and ML integration; modern JS frameworks provide superior interactive UI capabilities.
- Separation of concerns: API-first enables multiple clients (web, mobile, CLI), clearer versioning, and easier testing.
- Tooling: JS ecosystems have mature UI component libraries, dev servers with fast HMR, and bundlers optimizing for web delivery.

Quick recommendations

- Server: FastAPI for Python backends — lightweight, async-friendly, automatic OpenAPI docs, easy testing.
- Frontend: React (Vite), Svelte, or Vue for fast interactive UIs. Use component libraries for consistent UI (e.g., MUI, Tailwind UI, SvelteKit components).
- Auth: Keep auth logic centralized in the API; use secure cookies or JWT with proper refresh/rotation policies.
- Local dev: Run the frontend dev server (Vite) and proxy API calls to the FastAPI server during development. Use CORS and reverse proxy in production.
- Integration: Provide an OpenAPI/Swagger UI and generate typed clients (TypeScript) from the API schema when helpful.

Templates to consider (next actions)

- FastAPI minimal template with CORS and JWT auth.
- Vite + React minimal template calling the API with an example login flow.
- Docker Compose example to run both locally in a single dev environment.

Done: saved as `data/notes/frontend_api_mantra.md`.
