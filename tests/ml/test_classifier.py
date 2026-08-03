import pytest

from ticketroute.ml.classifier import Classification, classify


@pytest.mark.parametrize(
    ("text", "expected_intent"),
    [
        ("I FORGOT MY PIN!", "forgotten_pin"),
        ("I want to change my PIN", "change_pin"),
        ("My card was stolen", "card_stolen"),
        ("I made a cash withdrawal", "cash_withdrawal"),
        ("My card was charged a fee", "card_payment_fee_charged"),
    ],
)
def test_classify_returns_best_intent(
    text: str,
    expected_intent: str,
) -> None:
    result = classify(text, top_k=1)

    assert result == [
        Classification(
            intent=expected_intent,
            confidence=1.0,
        )
    ]


def test_classify_returns_ranked_alternatives() -> None:
    result = classify("I forgot my PIN", top_k=2)

    assert result == [
        Classification(intent="forgotten_pin", confidence=1.0),
        Classification(intent="change_pin", confidence=0.5),
    ]


def test_classify_limits_results_to_top_k() -> None:
    result = classify(
        "forgot pin change card stolen cash withdrawal fee charged",
        top_k=2,
    )
    assert len(result) == 2
    assert all(classification.confidence == 1.0 for classification in result)


def test_classify_returns_unclassified_when_no_keywords_match() -> None:
    result = classify("I need help with my account", top_k=3)

    assert result == [
        Classification(
            intent="unclassified",
            confidence=0.0,
        )
    ]


@pytest.mark.parametrize("top_k", [0, -1])
def test_classify_rejects_invalid_top_k(top_k: int) -> None:
    with pytest.raises(ValueError, match="top_k must be at least 1"):
        classify("I forgot my PIN", top_k=top_k)
