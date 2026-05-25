from __future__ import annotations

from app.game.deck import Card, Rank

_NUMBER_POINTS: dict[Rank, int] = {
    Rank.TWO: 2, Rank.THREE: 3, Rank.FOUR: 4, Rank.FIVE: 5,
    Rank.SIX: 6, Rank.SEVEN: 7, Rank.EIGHT: 8, Rank.NINE: 9,
    Rank.TEN: 10,
}
_FACE_POINTS: dict[Rank, int] = {Rank.JACK: 10, Rank.QUEEN: 10, Rank.KING: 10}
_ACE_POINTS = 1


def match_points(a: Card, b: Card) -> int:
    """Points awarded when two flipped cards have the same rank. 0 otherwise."""
    if a.rank != b.rank:
        return 0
    if a.rank == Rank.ACE:
        return _ACE_POINTS
    if a.rank in _NUMBER_POINTS:
        return _NUMBER_POINTS[a.rank]
    return _FACE_POINTS[a.rank]


def is_king_queen_pair(a: Card, b: Card) -> bool:
    ranks = {a.rank, b.rank}
    return ranks == {Rank.KING, Rank.QUEEN}


def triple_points(a: Card, b: Card, c: Card) -> int:
    """K+Q (or Q+K) followed by a third card. 10 pts if the third completes a triple of K or Q."""
    if not is_king_queen_pair(a, b):
        return 0
    if c.rank in (Rank.KING, Rank.QUEEN):
        return 10
    return 0
