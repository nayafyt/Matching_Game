from __future__ import annotations

from pydantic import BaseModel, Field

from app.game.deck import Difficulty
from app.game.state import GameState, Phase, TurnResult


class CreateGameRequest(BaseModel):
    difficulty: Difficulty
    num_players: int = Field(ge=2, le=8)


class FlipRequest(BaseModel):
    position: int = Field(ge=0)


class CardView(BaseModel):
    rank: str | None
    suit: str | None
    face_up: bool


class TurnResultView(BaseModel):
    outcome: str
    points: int
    player: int
    positions: list[int]


class GameView(BaseModel):
    id: str
    difficulty: int
    num_players: int
    rows: int
    cols: int
    current_player: int
    phase: Phase
    scores: list[int]
    cards: list[CardView]
    pending: list[int]
    last_result: TurnResultView | None
    is_finished: bool
    winners: list[int]

    @classmethod
    def from_state(cls, state: GameState) -> "GameView":
        rows, cols = state.board_size
        cards: list[CardView] = []
        for i, card in enumerate(state.deck):
            face_up = state.matched[i] or i in state.pending
            cards.append(
                CardView(
                    rank=card.rank.value if face_up else None,
                    suit=card.suit.value if face_up else None,
                    face_up=face_up,
                )
            )
        return cls(
            id=state.id,
            difficulty=int(state.difficulty),
            num_players=state.num_players,
            rows=rows,
            cols=cols,
            current_player=state.current_player,
            phase=state.phase,
            scores=state.scores,
            cards=cards,
            pending=list(state.pending),
            last_result=_view_result(state.last_result),
            is_finished=state.is_finished,
            winners=state.winners,
        )


def _view_result(result: TurnResult | None) -> TurnResultView | None:
    if result is None:
        return None
    return TurnResultView(
        outcome=result.outcome.value,
        points=result.points,
        player=result.player,
        positions=result.positions,
    )
