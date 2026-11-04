
"""
Turning two numbers into one, and one number into something a person can read.
← YOU BUILD THIS IN MILESTONES 4 AND 5

combine_signals:
    Combines the GPT-2 model signal and stylometry signal.

score_to_label:
    Converts the combined score into a reader-facing classification.

The combining rule is implemented in scoring.py::combine_signals.
"""

import config


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Combine two signals into one score between 0 and 1.

    Both signals use the same direction:
        0.0 = more human-like
        1.0 = more AI-like

    The model signal measures text predictability.
    The style signal measures structural writing patterns.

    Combining rule:
        combined_score = (0.5 * model_score) + (0.5 * style_score)

    The weights are defined in config.py.

    When the signals disagree, the weighted average moves
    toward the middle, reflecting uncertainty.

    This is intentional because falsely accusing a human
    writer is more harmful than missing some AI-generated text.

    Args:
        model_score: GPT-2 model signal, between 0 and 1.
        style_score: Stylometry signal, between 0 and 1.

    Returns:
        Combined score between 0 and 1.
    """

    combined_score = (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
    )

    # Ensure the final score stays within the expected range.
    combined_score = max(0.0, min(combined_score, 1.0))

    return round(combined_score, 4)


def score_to_label(score: float) -> tuple[str, str]:
    """
    Convert a combined score into a classification and
    a reader-friendly explanation.

    Returns:
        (guess, label_text)

    Classification thresholds:
        score <= 0.35: human
        0.35 < score < 0.65: unsure
        score >= 0.65: ai

    These classifications describe patterns in the text.
    They do not establish authorship.
    """

    if score >= config.AI_THRESHOLD:
        return (
            "ai",
            "This writing shows patterns associated with AI-generated "
            "text, but this result is not proof of AI use."
        )

    if score <= config.HUMAN_THRESHOLD:
        return (
            "human",
            "This writing appears more consistent with human-written "
            "text, but we cannot verify its authorship."
        )

    return (
        "unsure",
        "We cannot confidently determine whether this writing was "
        "created by a person or AI. This result is not an accusation."
    )


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers.

    Thresholds come from config.py so the ranges remain
    consistent with the classification logic.
    """

    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f">{config.HUMAN_THRESHOLD:.2f} – <{config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]
