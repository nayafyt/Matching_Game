from app.game.deck import Card, Rank, Suit
from app.game.rules import match_points, triple_points


def c(rank: Rank, suit: Suit = Suit.SPADES) -> Card:
    return Card(rank, suit)


def test_number_pair_awards_face_value():
    assert match_points(c(Rank.TWO, Suit.HEARTS), c(Rank.TWO, Suit.SPADES)) == 2
    assert match_points(c(Rank.SEVEN, Suit.HEARTS), c(Rank.SEVEN, Suit.CLUBS)) == 7


def test_ten_pair_awards_10():
    assert match_points(c(Rank.TEN, Suit.HEARTS), c(Rank.TEN, Suit.SPADES)) == 10


def test_ace_pair_awards_1():
    assert match_points(c(Rank.ACE, Suit.HEARTS), c(Rank.ACE, Suit.SPADES)) == 1


def test_face_pair_awards_10():
    for r in (Rank.JACK, Rank.QUEEN, Rank.KING):
        assert match_points(c(r, Suit.HEARTS), c(r, Suit.SPADES)) == 10


def test_non_matching_ranks_score_zero():
    assert match_points(c(Rank.TWO), c(Rank.THREE)) == 0
    assert match_points(c(Rank.KING), c(Rank.QUEEN)) == 0


def test_triple_kqk_scores_10():
    assert triple_points(c(Rank.KING), c(Rank.QUEEN), c(Rank.KING)) == 10


def test_triple_qkq_scores_10():
    assert triple_points(c(Rank.QUEEN), c(Rank.KING), c(Rank.QUEEN)) == 10


def test_triple_kqj_scores_zero():
    assert triple_points(c(Rank.KING), c(Rank.QUEEN), c(Rank.JACK)) == 0


def test_triple_not_kq_pair_scores_zero():
    assert triple_points(c(Rank.TWO), c(Rank.TWO), c(Rank.TWO)) == 0
