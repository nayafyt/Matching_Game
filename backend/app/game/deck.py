from __future__ import annotations

import random
from dataclasses import dataclass
from enum import IntEnum, StrEnum


class Difficulty(IntEnum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class Suit(StrEnum):
    HEARTS = "H"
    DIAMONDS = "D"
    CLUBS = "C"
    SPADES = "S"


class Rank(StrEnum):
    ACE = "A"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"


_EASY_RANKS: tuple[Rank, ...] = (Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING)
_MEDIUM_RANKS: tuple[Rank, ...] = (
    Rank.ACE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE,
    Rank.SIX, Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN,
)
_HARD_RANKS: tuple[Rank, ...] = tuple(Rank)

_RANKS_BY_DIFFICULTY: dict[Difficulty, tuple[Rank, ...]] = {
    Difficulty.EASY: _EASY_RANKS,
    Difficulty.MEDIUM: _MEDIUM_RANKS,
    Difficulty.HARD: _HARD_RANKS,
}

# Two suits per difficulty so that doubling every (rank, suit) keeps the
# classic 16 / 40 / 52 board sizes while giving each card a literal twin.
_SUITS_IN_PLAY: tuple[Suit, ...] = (Suit.HEARTS, Suit.SPADES)

BOARD_ROWS = 4


_COPIES_PER_CARD = 2


@dataclass(frozen=True, slots=True)
class Card:
    rank: Rank
    suit: Suit


def build_deck(difficulty: Difficulty) -> list[Card]:
    """Two copies of each (rank, suit) so every card has a matching twin."""
    ranks = _RANKS_BY_DIFFICULTY[difficulty]
    unique = [Card(rank, suit) for rank in ranks for suit in _SUITS_IN_PLAY]
    return unique * _COPIES_PER_CARD


def shuffled_deck(difficulty: Difficulty, rng: random.Random | None = None) -> list[Card]:
    """Build and shuffle a deck. Pass an `rng` for deterministic shuffles in tests."""
    deck = build_deck(difficulty)
    (rng or random).shuffle(deck)
    return deck


def board_dimensions(difficulty: Difficulty) -> tuple[int, int]:
    """Return (rows, cols) for the board at this difficulty."""
    size = len(_RANKS_BY_DIFFICULTY[difficulty]) * len(_SUITS_IN_PLAY) * _COPIES_PER_CARD
    return BOARD_ROWS, size // BOARD_ROWS
