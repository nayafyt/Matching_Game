from fastapi.testclient import TestClient

from app.main import create_app


def client() -> TestClient:
    return TestClient(create_app())


def test_health():
    assert client().get("/health").json() == {"status": "ok"}


def test_create_game_returns_state():
    c = client()
    r = c.post("/api/games", json={"difficulty": 1, "num_players": 2})
    assert r.status_code == 201
    body = r.json()
    assert body["num_players"] == 2
    assert body["rows"] == 4
    assert body["cols"] == 4
    assert len(body["cards"]) == 16
    assert all(card["face_up"] is False for card in body["cards"])
    assert body["current_player"] == 1
    assert body["phase"] == "awaiting_first"


def test_get_game_404_on_unknown_id():
    assert client().get("/api/games/does-not-exist").status_code == 404


def test_flip_then_resolve_roundtrip():
    c = client()
    game = c.post("/api/games", json={"difficulty": 1, "num_players": 2}).json()
    gid = game["id"]

    r1 = c.post(f"/api/games/{gid}/flip", json={"position": 0}).json()
    assert r1["pending"] == [0]
    assert r1["cards"][0]["face_up"] is True
    assert r1["phase"] == "awaiting_second"

    r2 = c.post(f"/api/games/{gid}/flip", json={"position": 1}).json()
    assert r2["pending"] == [0, 1]
    assert r2["phase"] in ("reveal_pair", "awaiting_third")

    if r2["phase"] == "reveal_pair":
        r3 = c.post(f"/api/games/{gid}/resolve").json()
        assert r3["last_result"] is not None


def test_flip_invalid_position_returns_409():
    c = client()
    game = c.post("/api/games", json={"difficulty": 1, "num_players": 2}).json()
    r = c.post(f"/api/games/{game['id']}/flip", json={"position": 999})
    assert r.status_code == 409


def test_create_game_rejects_bad_player_count():
    c = client()
    r = c.post("/api/games", json={"difficulty": 1, "num_players": 1})
    assert r.status_code == 422
