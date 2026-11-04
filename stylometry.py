
"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it as text — the
shape of it, without understanding a word.

Three measures are used:

    sentence_length_spread   How much sentence lengths vary
    type_token_ratio         How diverse the vocabulary is
    punctuation_density      How frequently punctuation appears

The style signal is a heuristic, not proof of AI authorship.

Limitations:
    - Short texts provide little information about writing style.
    - Formal human writing may appear unusually consistent.
    - Text length affects vocabulary diversity.
    - Editing punctuation or sentence boundaries can change the score
      without changing the underlying content.

Run:
    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures ────────────────────────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    Measure how much sentence lengths vary.

    Uses the coefficient of variation:
        standard deviation / mean sentence length

    Returns:
        A nonnegative float.
        Higher values mean greater sentence-length variation.

    A text with fewer than two sentences returns 0.0 because
    sentence-length variation cannot be estimated reliably.
    """

    sentence_list = sentences(text)

    if len(sentence_list) < 2:
        return 0.0

    lengths = [len(words(sentence)) for sentence in sentence_list]

    mean_length = statistics.mean(lengths)

    if mean_length == 0:
        return 0.0

    spread = statistics.stdev(lengths) / mean_length

    return round(spread, 4)


def type_token_ratio(text: str) -> float:
    """
    Measure vocabulary diversity.

    Formula:
        number of unique words / total number of words

    Returns:
        A float between 0 and 1.
        Higher values indicate more diverse vocabulary.

    Limitation:
        Longer texts naturally repeat more words, so this
        measurement is sensitive to text length.
    """

    word_list = words(text)

    if not word_list:
        return 0.0

    unique_words = len(set(word_list))
    total_words = len(word_list)

    ratio = unique_words / total_words

    return round(ratio, 4)


def punctuation_density(text: str) -> float:
    """
    Measure punctuation frequency relative to text length.

    Counts:
        . , ! ? ; : - — ( ) " '

    Formula:
        punctuation characters / total characters

    Returns:
        A float between 0 and 1.
        Higher values indicate greater punctuation density.

    Limitation:
        Punctuation frequency depends heavily on writing
        style, genre, and formatting.
    """

    if not text:
        return 0.0

    punctuation_marks = ".,!?;:-—()\"'"

    punctuation_count = sum(
        1 for char in text if char in punctuation_marks
    )

    density = punctuation_count / len(text)

    return round(density, 4)


# ── Combining the three measurements ─────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    Calculate the final stylometry score.

    Returns:
        A float between 0 and 1.
        Higher values mean more AI-like writing.

    Three equally weighted components:

        1. Sentence consistency
           Less variation -> higher AI-like score.

        2. Vocabulary repetition
           Less vocabulary diversity -> higher AI-like score.

        3. Punctuation simplicity
           Less punctuation -> higher AI-like score.

    These are heuristic assumptions and may misclassify
    ordinary human writing.
    """

    word_list = words(text)

    if not word_list:
        return 0.5

    # A single sentence cannot provide a reliable estimate
    # of sentence-length variation.
    if len(sentences(text)) < 2:
        sentence_score = 0.5
    else:
        spread = sentence_length_spread(text)

        # Normalize spread to a 0–1 scale.
        # A spread of 1.0 or greater maps to 0.
        normalized_spread = min(spread, 1.0)

        sentence_score = 1.0 - normalized_spread

    # Lower vocabulary diversity maps to a higher AI-like score.
    vocabulary_ratio = type_token_ratio(text)
    vocabulary_score = 1.0 - vocabulary_ratio

    # Normalize punctuation density using a reference value
    # of 0.10 punctuation characters per character.
    density = punctuation_density(text)
    normalized_density = min(density / 0.10, 1.0)

    punctuation_score = 1.0 - normalized_density

    # Give each component equal weight.
    combined = (
        sentence_score
        + vocabulary_score
        + punctuation_score
    ) / 3

    return round(max(0.0, min(combined, 1.0)), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density       {punctuation_density(text)}")
    print(f"style_signal              {style_signal(text)}   (higher = more likely AI)")
    print("\nThese are heuristic measurements, not proof of authorship.")
