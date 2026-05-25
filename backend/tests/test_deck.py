import random

from app.game.deck import Card, Difficulty, Rank, Suit, build_deck, shuffled_deck


def test_easy_deck_has_16_cards():
    deck = build_deck(Difficulty.EASY)
    assert len(deck) == 16
    assert {c.rank for c in deck} == {Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING}


def test_medium_deck_has_40_cards():
    assert len(build_deck(Difficulty.MEDIUM)) == 40


def test_hard_deck_has_52_cards():
    assert len(build_deck(Difficulty.HARD)) == 52


def test_card_id_combines_rank_and_suit():
    assert Card(Rank.ACE, Suit.SPADES).id == "AS"
    assert Card(Rank.TEN, Suit.HEARTS).id == "10H"


def test_shuffled_deck_is_deterministic_with_seeded_rng():
    a = shuffled_deck(Difficulty.HARD, rng=random.Random(42))
    b = shuffled_deck(Difficulty.HARD, rng=random.Random(42))
    assert a == b


def test_shuffle_preserves_all_cards():
    rng = random.Random(0)
    shuffled = shuffled_deck(Difficulty.HARD, rng=rng)
    assert sorted(c.id for c in shuffled) == sorted(c.id for c in build_deck(Difficulty.HARD))
