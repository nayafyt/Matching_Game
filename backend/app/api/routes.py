from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.game.state import GameState, InvalidMove
from app.schemas.game import CreateGameRequest, FlipRequest, GameView
from app.store import store

router = APIRouter(prefix="/api/games", tags=["games"])


@router.post("", response_model=GameView, status_code=status.HTTP_201_CREATED)
def create_game(req: CreateGameRequest) -> GameView:
    game = GameState.new(difficulty=req.difficulty, num_players=req.num_players)
    store.add(game)
    return GameView.from_state(game)


@router.get("/{game_id}", response_model=GameView)
def get_game(game_id: str) -> GameView:
    game = store.get(game_id)
    if game is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "game not found")
    return GameView.from_state(game)


@router.post("/{game_id}/flip", response_model=GameView)
def flip_card(game_id: str, req: FlipRequest) -> GameView:
    game = store.get(game_id)
    if game is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "game not found")
    try:
        game.flip(req.position)
    except InvalidMove as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    return GameView.from_state(game)


@router.post("/{game_id}/resolve", response_model=GameView)
def resolve_turn(game_id: str) -> GameView:
    game = store.get(game_id)
    if game is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "game not found")
    try:
        game.resolve()
    except InvalidMove as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    return GameView.from_state(game)
