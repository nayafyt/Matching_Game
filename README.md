# Matching Game

A web version of the classic matching card game. Players take turns flipping pairs of cards from a face-down deck; matched ranks score points. Supports 2–8 players on a single device, three difficulty levels (16 / 40 / 52 cards), and full English + Greek translations.

## Stack

- **Backend** — Python 3.13 + FastAPI + Pydantic. Pure game-rule modules with no I/O, wrapped by a small REST API.
- **Frontend** — React 18 + Vite + TypeScript + Tailwind CSS v4 + i18next.
- **Containers** — Docker + Compose for local dev and production.

## Project layout

```
.
├── backend/
│   ├── app/
│   │   ├── game/        # pure game logic (deck, rules, state machine)
│   │   ├── api/         # FastAPI router
│   │   ├── schemas/     # Pydantic request/response models
│   │   ├── store.py     # in-memory game store (swap for Redis later)
│   │   └── main.py      # FastAPI app factory
│   ├── tests/           # pytest (game + API)
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── api/         # fetch client
│   │   ├── components/  # ui/ + game/
│   │   ├── hooks/       # useGame
│   │   ├── i18n/        # en + el locales
│   │   └── lib/         # types + cn() helper
│   ├── Dockerfile       # dev + prod stages
│   └── package.json
├── compose.yaml         # local dev
├── compose.prod.yaml    # production (nginx + uvicorn)
└── README.md
```

## Quick start (Docker)

```bash
docker compose up --build
```

- Frontend: <http://localhost:5173>
- Backend API: <http://localhost:8000>
- API docs (Swagger): <http://localhost:8000/docs>

## Running tests

```bash
docker compose run --rm backend pytest
```

## Production build

```bash
docker compose -f compose.prod.yaml up --build -d
```

The frontend is served as a static bundle behind nginx on port 80; the backend runs on port 8000. Front-end deploy targets like Vercel/Netlify can use `frontend/` with build command `npm run build` and output `dist/`.

## Game rules

- **Easy** uses 16 cards (ranks 10/J/Q/K). **Medium** uses 40 (A–10). **Hard** uses the full 52.
- A pair of matching ranks scores its face value: 2–10 → that number, A → 1, J/Q/K → 10.
- Pair of Jacks: bonus turn (same player plays again).
- Pair of Kings: next player loses their turn.
- King + Queen: flip a third card. If it's also a K or Q, the triple scores 10.

## API surface

| Method | Path                          | Purpose                                       |
| ------ | ----------------------------- | --------------------------------------------- |
| POST   | `/api/games`                  | Create a new game                             |
| GET    | `/api/games/{id}`             | Fetch current state                           |
| POST   | `/api/games/{id}/flip`        | Flip a card by board position (0-indexed)     |
| POST   | `/api/games/{id}/resolve`     | Resolve a revealed pair/triple, advance turn  |
| GET    | `/health`                     | Health check                                  |
