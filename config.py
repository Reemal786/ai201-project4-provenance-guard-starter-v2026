
"""
Settings for Provenance Guard.

Everything you're likely to change lives here, at the top, on purpose.

You'll edit the thresholds in Milestone 5 and the rate limits in unit 8.
"""

import os
from pathlib import Path

ROOT = Path(__file__).parent


# ─── The service ─────────────────────────────────────────────────────────────

# `127.0.0.1` is loopback — only your own machine can reach it, which is what
# you want all through units 7 and 8. A host somewhere else has to accept
# traffic from outside the box, and that means `0.0.0.0`. Setting the env var
# is how you get it; the default keeps your local `curl` commands unchanged.
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))

# Flask's debug mode gives anyone who can reach the service an interactive
# Python prompt inside your process. Fine on loopback, a gift to strangers
# anywhere else — so it turns itself off the moment HOST isn't loopback.
DEBUG = os.getenv("AI201_DEBUG", "1") == "1" and HOST in ("127.0.0.1", "localhost")


# ─── The local model ─────────────────────────────────────────────────────────

# Your first signal runs a language model ON YOUR OWN MACHINE. No account, no
# key, no card. It downloads about 550 MB the first time — do that before
# class, not during it.
#
# What it measures: how predictable your text is to a language model. Text a
# model finds easy to predict tends to be text a model wrote.
#
# The first call is the slow one — ten to twenty seconds while the model loads,
# longer on an older laptop. After that it stays in memory and a submission
# takes a second or two. That cost is part of what you're learning: this is
# what running a model inline in a request actually looks like.

DETECTOR_MODEL = os.getenv("AI201_DETECTOR_MODEL", "gpt2")

# Longer text gives a steadier reading but takes longer. 400 tokens is roughly
# 300 words, which is enough for the signal to mean something.
DETECTOR_MAX_TOKENS = 400

# Reject excessively long submissions before running the detector.
# This is a character limit, separate from the model's token limit.
MAX_TEXT_LENGTH = 10000


# ─── Scoring (Milestone 4) ───────────────────────────────────────────────────

# How much each signal counts toward the combined score.
#
# Both signals contribute equally. When they disagree, the combined score
# moves toward the unsure range.

WEIGHT_MODEL_SIGNAL = 0.5
WEIGHT_STYLE_SIGNAL = 0.5


# ─── Thresholds (Milestone 5) ────────────────────────────────────────────────

# Where one label becomes another. Scores run from 0.0 (more human-like)
# to 1.0 (more AI-like).
#
#   score <= HUMAN_THRESHOLD       -> high-confidence human
#   between the two thresholds     -> unsure
#   score >= AI_THRESHOLD          -> high-confidence AI
#
# Widening the unsure band reduces confident classifications but may help
# avoid unsupported accusations. These scores are not proof of authorship.

HUMAN_THRESHOLD = 0.35
AI_THRESHOLD = 0.65

# A weighted average can only land between its two inputs.
# Our implemented stylometry signal varies with the submitted text.


# ─── Rate limiting (UNIT 8) ──────────────────────────────────────────────────

# Enabled for Unit 8, Milestone 1.
#
# 10 requests per minute allows reasonable retries and revisions while
# limiting rapid automated attempts to probe detection thresholds.
#
# 200 requests per day accommodates normal use and testing while placing
# a ceiling on repeated automated submissions.
#
# The README documents why these values were selected.

RATE_LIMITING_ENABLED = os.getenv("AI201_RATE_LIMITS", "1") == "1"

RATE_LIMIT_PER_MINUTE = 10
RATE_LIMIT_PER_DAY = 200

# In-memory storage is appropriate for this local prototype.
# Counters reset when the service restarts and are not shared between
# multiple service instances.
RATE_LIMIT_STORAGE = "memory://"


# ─── Paths ───────────────────────────────────────────────────────────────────

LOG_DIR = ROOT / "logs"
AUDIT_LOG = LOG_DIR / "audit.jsonl"
RESULTS_DIR = ROOT / "results"
