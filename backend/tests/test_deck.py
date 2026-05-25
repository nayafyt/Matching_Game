import random
from collections import Counter

from app.game.deck import Difficulty, Rank, build_deck, shuffled_deck


def test_easy_deck_has_16_cards():
    deck = build_deck(Difficulty.EASY)
    assert len(deck) == 16
    assert {c.rank for c in deck} == {Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING}


def test_medium_deck_has_40_cards():
    assert len(build_deck(Difficulty.MEDIUM)) == 40


def test_hard_deck_has_52_cards():
    assert len(build_deck(Difficulty.HARD)) == 52


def test_every_card_appears_exactly_twice():
    counts = Counter(build_deck(Difficulty.HARD))
    assert set(counts.values()) == {2}


def test_shuffled_deck_is_deterministic_with_seeded_rng():
    a = shuffled_deck(Difficulty.HARD, rng=random.Random(42))
    b = shuffled_deck(Difficulty.HARD, rng=random.Random(42))
    assert a == b


def test_shuffle_preserves_all_cards():
    rng = random.Random(0)
    shuffled = shuffled_deck(Difficulty.HARD, rng=rng)
    assert Counter(shuffled) == Counter(build_deck(Difficulty.HARD))
