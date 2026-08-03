import re
from dataclasses import dataclass

_KEYWORDS_BY_INTENT: dict[str, frozenset[str]] = {
    "forgotten_pin": frozenset({"forgot", "pin"}),
    "change_pin": frozenset({"change", "pin"}),
    "card_stolen": frozenset({"card", "stolen"}),
    "cash_withdrawal": frozenset({"cash", "withdrawal"}),
    "card_payment_fee_charged": frozenset({"card", "fee", "charged"}),
}


@dataclass(frozen=True)
class Classification:
    intent: str
    confidence: float


def classify(text: str, top_k: int) -> list[Classification]:
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    words = set(re.findall(r"[a-z0-9]+", text.casefold()))
    classifications: list[Classification] = []

    for intent, keywords in _KEYWORDS_BY_INTENT.items():
        matched_keywords = words & keywords

        if not matched_keywords:
            continue

        confidence = len(matched_keywords) / len(keywords)
        classifications.append(
            Classification(
                intent=intent,
                confidence=confidence,
            )
        )

    classifications.sort(
        key=lambda classification: classification.confidence,
        reverse=True,
    )

    if not classifications:
        return [Classification(intent="unclassified", confidence=0.0)]

    return classifications[:top_k]
