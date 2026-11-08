"""Starter test. It passes on every card, so it can't tell a good card from a bad one. Replace it."""


def test_the_card_mentions_accuracy(card):
    assert "accuracy" in card.lower()
