from __future__ import annotations

import threading
from collections import OrderedDict

from app.game.state import GameState

DEFAULT_CAPACITY = 1000


class GameStore:
    """In-memory LRU-capped game store. Swap for Redis later by re-implementing this interface."""

    def __init__(self, capacity: int = DEFAULT_CAPACITY) -> None:
        self._games: OrderedDict[str, GameState] = OrderedDict()
        self._lock = threading.Lock()
        self._capacity = capacity

    def add(self, game: GameState) -> None:
        with self._lock:
            self._games[game.id] = game
            self._games.move_to_end(game.id)
            while len(self._games) > self._capacity:
                self._games.popitem(last=False)

    def get(self, game_id: str) -> GameState | None:
        with self._lock:
            game = self._games.get(game_id)
            if game is not None:
                self._games.move_to_end(game_id)
            return game

    def __len__(self) -> int:
        return len(self._games)


store = GameStore()
