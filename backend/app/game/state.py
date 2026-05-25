from __future__ import annotations

import random
import uuid
from dataclasses import dataclass, field
from enum import StrEnum

from app.game.deck import Card, Difficulty, Rank, board_dimensions, shuffled_deck
from app.game.rules import is_king_queen_pair, match_points, triple_points

MIN_PLAYERS = 2
MAX_PLAYERS = 8


class Phase(StrEnum):
    AWAITING_FIRST = "awaiting_first"
    AWAITING_SECOND = "awaiting_second"
    REVEAL_PAIR = "reveal_pair"
    AWAITING_THIRD = "awaiting_third"
    REVEAL_TRIPLE = "reveal_triple"
    FINISHED = "finished"


class Outcome(StrEnum):
    MATCH = "match"
    MISS = "miss"
    BONUS_TURN = "bonus_turn"
    SKIP_NEXT = "skip_next"
    TRIPLE_MATCH = "triple_match"
    TRIPLE_MISS = "triple_miss"


@dataclass(slots=True)
class TurnResult:
    outcome: Outcome
    points: int
    player: int
    positions: list[int]


@dataclass(slots=True)
class GameState:
    id: str
    difficulty: Difficulty
    num_players: int
    deck: list[Card]
    matched: list[bool]
    pending: list[int]
    scores: list[int]
    current_player: int
    phase: Phase
    last_result: TurnResult | None = None
    _skip_next: bool = field(default=False, repr=False)

    @classmethod
    def new(
        cls,
        difficulty: Difficulty,
        num_players: int,
        rng: random.Random | None = None,
    ) -> "GameState":
        if not MIN_PLAYERS <= num_players <= MAX_PLAYERS:
            raise ValueError(f"num_players must be in [{MIN_PLAYERS}, {MAX_PLAYERS}]")
        deck = shuffled_deck(difficulty, rng=rng)
        return cls(
            id=uuid.uuid4().hex,
            difficulty=difficulty,
            num_players=num_players,
            deck=deck,
            matched=[False] * len(deck),
            pending=[],
            scores=[0] * num_players,
            current_player=1,
            phase=Phase.AWAITING_FIRST,
        )

    @property
    def board_size(self) -> tuple[int, int]:
        return board_dimensions(self.difficulty)

    @property
    def is_finished(self) -> bool:
        return all(self.matched)

    def flip(self, position: int) -> None:
        """Reveal a card. Caller must then call `resolve()` when the phase is REVEAL_*."""
        if self.phase == Phase.FINISHED:
            raise InvalidMove("game is finished")
        if self.phase in (Phase.REVEAL_PAIR, Phase.REVEAL_TRIPLE):
            raise InvalidMove("must resolve current reveal before flipping again")
        if not 0 <= position < len(self.deck):
            raise InvalidMove(f"position {position} out of range")
        if self.matched[position]:
            raise InvalidMove("card already matched")
        if position in self.pending:
            raise InvalidMove("card already flipped this turn")

        self.pending.append(position)

        if self.phase == Phase.AWAITING_FIRST:
            self.phase = Phase.AWAITING_SECOND
            return

        if self.phase == Phase.AWAITING_SECOND:
            a, b = (self.deck[i] for i in self.pending)
            if is_king_queen_pair(a, b):
                self.phase = Phase.AWAITING_THIRD
            else:
                self.phase = Phase.REVEAL_PAIR
            return

        if self.phase == Phase.AWAITING_THIRD:
            self.phase = Phase.REVEAL_TRIPLE
            return

    def resolve(self) -> TurnResult:
        """Commit the result of a REVEAL_* phase and advance turn."""
        if self.phase == Phase.REVEAL_PAIR:
            return self._resolve_pair()
        if self.phase == Phase.REVEAL_TRIPLE:
            return self._resolve_triple()
        raise InvalidMove(f"cannot resolve in phase {self.phase}")

    def _resolve_pair(self) -> TurnResult:
        a_pos, b_pos = self.pending
        a, b = self.deck[a_pos], self.deck[b_pos]
        points = match_points(a, b)
        positions = list(self.pending)
        actor = self.current_player

        if points == 0:
            self._end_turn(advance=True)
            outcome = Outcome.MISS
        else:
            self.matched[a_pos] = True
            self.matched[b_pos] = True
            self.scores[actor - 1] += points
            if a.rank == Rank.JACK:
                outcome = Outcome.BONUS_TURN
                self._end_turn(advance=False)
            elif a.rank == Rank.KING:
                outcome = Outcome.SKIP_NEXT
                self._skip_next = True
                self._end_turn(advance=True)
            else:
                outcome = Outcome.MATCH
                self._end_turn(advance=True)

        self.last_result = TurnResult(outcome, points, actor, positions)
        return self.last_result

    def _resolve_triple(self) -> TurnResult:
        a_pos, b_pos, c_pos = self.pending
        a, b, c = self.deck[a_pos], self.deck[b_pos], self.deck[c_pos]
        points = triple_points(a, b, c)
        positions = list(self.pending)
        actor = self.current_player

        if points > 0:
            self.scores[actor - 1] += points
            self.matched[c_pos] = True
            if a.rank == c.rank:
                self.matched[a_pos] = True
            else:
                self.matched[b_pos] = True
            outcome = Outcome.TRIPLE_MATCH
        else:
            outcome = Outcome.TRIPLE_MISS

        self._end_turn(advance=True)
        self.last_result = TurnResult(outcome, points, actor, positions)
        return self.last_result

    def _end_turn(self, *, advance: bool) -> None:
        self.pending = []
        if self.is_finished:
            self.phase = Phase.FINISHED
            return
        if advance:
            steps = 2 if self._skip_next else 1
            self._skip_next = False
            self.current_player = ((self.current_player - 1 + steps) % self.num_players) + 1
        self.phase = Phase.AWAITING_FIRST

    @property
    def winners(self) -> list[int]:
        """1-indexed list of players tied for the highest score. Empty if game not finished."""
        if not self.is_finished:
            return []
        top = max(self.scores)
        return [i + 1 for i, s in enumerate(self.scores) if s == top]


class InvalidMove(Exception):
    """Raised when a flip/resolve is not legal in the current phase."""
