import random

import pytest

from app.game.deck import Card, Difficulty, Rank, Suit
from app.game.state import GameState, InvalidMove, Outcome, Phase


def _state_with_deck(deck: list[Card], players: int = 2) -> GameState:
    """Helper that builds a state and overrides the deck for deterministic scenarios."""
    state = GameState.new(Difficulty.EASY, players, rng=random.Random(0))
    state.deck = deck
    state.matched = [False] * len(deck)
    return state


def test_new_game_starts_with_player_1_and_awaiting_first():
    g = GameState.new(Difficulty.EASY, 2)
    assert g.current_player == 1
    assert g.phase == Phase.AWAITING_FIRST
    assert g.scores == [0, 0]
    assert len(g.deck) == 16


def test_new_game_rejects_too_few_players():
    with pytest.raises(ValueError):
        GameState.new(Difficulty.EASY, 1)


def test_simple_match_awards_points_and_advances_turn():
    deck = [Card(Rank.FIVE, Suit.HEARTS), Card(Rank.FIVE, Suit.SPADES)] + [
        Card(Rank.TWO, Suit.HEARTS)
    ] * 14
    g = _state_with_deck(deck, players=2)
    g.flip(0)
    g.flip(1)
    assert g.phase == Phase.REVEAL_PAIR
    result = g.resolve()
    assert result.outcome == Outcome.MATCH
    assert result.points == 5
    assert g.scores == [5, 0]
    assert g.current_player == 2
    assert g.matched[0] and g.matched[1]


def test_miss_keeps_score_and_advances_turn():
    deck = [Card(Rank.TWO, Suit.HEARTS), Card(Rank.THREE, Suit.SPADES)] + [
        Card(Rank.FOUR, Suit.HEARTS)
    ] * 14
    g = _state_with_deck(deck, players=2)
    g.flip(0)
    g.flip(1)
    result = g.resolve()
    assert result.outcome == Outcome.MISS
    assert result.points == 0
    assert g.scores == [0, 0]
    assert g.current_player == 2
    assert not g.matched[0] and not g.matched[1]


def test_jack_match_grants_bonus_turn():
    deck = [Card(Rank.JACK, Suit.HEARTS), Card(Rank.JACK, Suit.SPADES)] + [
        Card(Rank.TWO, Suit.HEARTS)
    ] * 14
    g = _state_with_deck(deck, players=3)
    g.flip(0)
    g.flip(1)
    result = g.resolve()
    assert result.outcome == Outcome.BONUS_TURN
    assert g.current_player == 1


def test_king_match_skips_next_player():
    deck = [Card(Rank.KING, Suit.HEARTS), Card(Rank.KING, Suit.SPADES)] + [
        Card(Rank.TWO, Suit.HEARTS)
    ] * 14
    g = _state_with_deck(deck, players=3)
    g.flip(0)
    g.flip(1)
    result = g.resolve()
    assert result.outcome == Outcome.SKIP_NEXT
    assert g.current_player == 3


def test_kq_pair_enters_awaiting_third_phase():
    deck = [Card(Rank.KING, Suit.HEARTS), Card(Rank.QUEEN, Suit.SPADES)] + [
        Card(Rank.KING, Suit.CLUBS)
    ] + [Card(Rank.TWO, Suit.HEARTS)] * 13
    g = _state_with_deck(deck, players=2)
    g.flip(0)
    g.flip(1)
    assert g.phase == Phase.AWAITING_THIRD
    g.flip(2)
    assert g.phase == Phase.REVEAL_TRIPLE
    result = g.resolve()
    assert result.outcome == Outcome.TRIPLE_MATCH
    assert result.points == 10
    assert g.scores[0] == 10
    assert g.matched[0]
    assert g.matched[2]
    assert not g.matched[1]


def test_kq_triple_miss_keeps_all_face_down():
    deck = [Card(Rank.KING, Suit.HEARTS), Card(Rank.QUEEN, Suit.SPADES)] + [
        Card(Rank.TWO, Suit.CLUBS)
    ] + [Card(Rank.FIVE, Suit.HEARTS)] * 13
    g = _state_with_deck(deck, players=2)
    g.flip(0)
    g.flip(1)
    g.flip(2)
    result = g.resolve()
    assert result.outcome == Outcome.TRIPLE_MISS
    assert result.points == 0
    assert not any(g.matched[:3])
    assert g.current_player == 2


def test_cannot_flip_same_card_twice():
    g = GameState.new(Difficulty.EASY, 2, rng=random.Random(0))
    g.flip(0)
    with pytest.raises(InvalidMove):
        g.flip(0)


def test_cannot_flip_after_reveal_without_resolving():
    deck = [Card(Rank.TWO, Suit.HEARTS), Card(Rank.THREE, Suit.SPADES)] + [
        Card(Rank.FOUR, Suit.HEARTS)
    ] * 14
    g = _state_with_deck(deck, players=2)
    g.flip(0)
    g.flip(1)
    with pytest.raises(InvalidMove):
        g.flip(2)


def test_game_finishes_when_all_matched():
    deck = [Card(Rank.FIVE, Suit.HEARTS), Card(Rank.FIVE, Suit.SPADES)]
    g = _state_with_deck(deck, players=2)
    g.flip(0)
    g.flip(1)
    g.resolve()
    assert g.phase == Phase.FINISHED
    assert g.is_finished
    assert g.winners == [1]


def test_winners_returns_all_tied_players():
    g = GameState.new(Difficulty.EASY, 3, rng=random.Random(0))
    g.scores = [5, 5, 3]
    g.matched = [True] * len(g.deck)
    assert g.winners == [1, 2]
