# Provenance Guard

> **New to this repository? Read [RUNNING.md](RUNNING.md) first.**
>
> Run the environment checks:
>
> ```bat
> python test.py
> ```
>
> Start the service in one terminal:
>
> ```bat
> python app.py
> ```
>
> Use a second terminal to send requests and run evaluations.

---

## What This Does

1. A writer submits text and a creator ID to `POST /submit`. The Flask route validates the JSON and required fields.
2. `detector.model_signal()` uses GPT-2 to calculate perplexity and convert it into a score between 0 and 1.
3. `stylometry.style_signal()` measures sentence-length variation, vocabulary diversity, and punctuation density.
4. `scoring.combine_signals()` combines the two signals using a 50/50 weighted average.
5. `scoring.score_to_label()` maps the combined score to `human`, `unsure`, or `ai`.
6. The service creates a content ID and records the decision through `audit.log_decision()`.
7. The response includes the content ID, classification, reader-facing label, classification-strength indicator, and both signal scores.

A writer can challenge a result through `POST /appeal`. The service records the reasoning and appends an `under_review` event without deleting the original decision.

Missing or invalid fields return HTTP 400. Text exceeding 10,000 characters returns HTTP 413. Text that the detector cannot score because it is too short now returns HTTP 400 instead of HTTP 500.

The classifications describe heuristic writing patterns. They do not establish who wrote the text.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:**

GPT-2 calculates perplexity: how predictable the submitted text is to that model. Lower perplexity produces a higher AI-like score.

The conversion is:

```text
model_score = 1 / (1 + (perplexity / 45.0) ** 1.6)
```

**Why that might differ between human and AI writing:**

Language models generate text using likely next-token patterns. Some generated writing may therefore be predictable to another language model. Human writing can include unusual vocabulary and unexpected constructions.

This is an assumption used by the prototype, not a reliable rule about authorship.

**What it cannot see:**

GPT-2 does not verify the author or the writing process. Plain human writing, formal templates, and careful second-language writing can be predictable. Unusual AI-generated writing can be less predictable.

The midpoint of 45.0 and steepness of 1.6 are heuristic scoring choices. The resulting score is not a calibrated probability of AI authorship.

The detector also truncates input at its configured token limit. Content outside that window does not contribute to the model signal.

### Signal two — the style signal

**What it measures:**

The style signal uses three measurements:

- Sentence-length spread: standard deviation divided by mean sentence length.
- Type-token ratio: unique words divided by total words.
- Punctuation density: punctuation characters divided by total characters.

The measurements are converted into three equally weighted components:

```text
sentence_score = 1 - min(sentence_length_spread, 1)
vocabulary_score = 1 - type_token_ratio
punctuation_score = 1 - min(punctuation_density / 0.10, 1)

style_score = (
    sentence_score
    + vocabulary_score
    + punctuation_score
) / 3
```

For fewer than two sentences, the sentence component is set to 0.5. Text with no recognized words receives a style signal of 0.5.

**Why that might differ between human and AI writing:**

The heuristic assumes that consistent sentence lengths, repeated vocabulary, and simple punctuation may be associated with generated writing.

**What it cannot see:**

The signal does not understand meaning or verify authorship. Human writing can follow the same patterns. Typos, punctuation changes, quotations, and sentence splitting can change its score without changing the underlying ideas.

Type-token ratio is sensitive to passage length. Longer passages have more opportunities to repeat vocabulary.

The word extraction pattern recognizes English letters, digits, and apostrophes. It does not provide meaningful vocabulary analysis for many other scripts.

### The combining rule

**The rule:**

Both signals contribute equally:

```text
combined_score = (0.50 * model_score) + (0.50 * style_score)
```

The result is clamped to the range 0–1 and rounded to four decimal places.

**The numbers:**

| Setting | Value |
|---|---:|
| Model signal weight | 0.50 |
| Style signal weight | 0.50 |
| Human threshold | 0.35 |
| AI threshold | 0.65 |

Conflicting signals can produce an unsure classification. This reflects my preference to avoid making an accusation from one weak signal.

Equal weighting does not guarantee an unsure result whenever signals disagree, and it does not guarantee a low false-positive rate.

**Where it lives:**

`scoring.py::combine_signals`

**Classification-strength indicator:**

The API returns a field named `confidence`:

```text
confidence = 2 * abs(combined_score - 0.50)
```

This measures distance from the midpoint. It is not the combined score and is not a calibrated probability.

The attack reports label this field `Score`. That column must not be compared directly with the 0.35 and 0.65 classification thresholds. Those thresholds apply to `combined_score`.

**A case where the signals split:**

If the model score is 0.90 and the style score is 0.10:

```text
combined_score = (0.50 * 0.90) + (0.50 * 0.10)
combined_score = 0.50
```

The result is unsure.

In an actual submission, the service returned:

```text
Text:
I spent the afternoon walking through the park and watching the birds near the pond.

Model signal: 0.6568
Style signal: 0.5270
Combined score: 0.5919
Classification: unsure
Confidence field: 0.1838
```

Although the model signal exceeded 0.65, the combined score remained inside the unsure range.

---

## Label Variants

| Label | Combined-score range | Exact reader-facing text |
|---|---|---|
| high-confidence human | 0.00–0.35 inclusive | This writing appears more consistent with human-written text, but we cannot verify its authorship. |
| unsure | Greater than 0.35 and less than 0.65 | We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation. |
| high-confidence AI | 0.65–1.00 inclusive | This writing shows patterns associated with AI-generated text, but this result is not proof of AI use. |

**Why I worded the unsure label this way:**

An uncertain result should not imply that a writer did something wrong. The label explicitly says that the result is not an accusation.

The other labels also avoid claiming proof of authorship. “High-confidence” describes the application's threshold rules, not verified certainty.

---

## Sample Run

### A submission

Request from Windows Command Prompt:

```bat
curl.exe -X POST "http://127.0.0.1:5000/submit" -H "Content-Type: application/json" -d "{\"text\":\"I spent the afternoon walking through the park and watching the birds near the pond.\",\"creator_id\":\"student_001\"}"
```

Response:

```json
{
  "confidence": 0.1838,
  "content_id": "8d2eb280-776e-430c-ad22-1ce34a492627",
  "guess": "unsure",
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "model_score": 0.6568,
  "style_score": 0.527
}
```

The combined score was 0.5919, so the result was unsure.

### An appeal

Request:

```bat
curl.exe -X POST "http://127.0.0.1:5000/appeal" -H "Content-Type: application/json" -d "{\"content_id\":\"8d2eb280-776e-430c-ad22-1ce34a492627\",\"reasoning\":\"I wrote this text myself and would like the classification reviewed.\"}"
```

Response:

```json
{
  "content_id": "8d2eb280-776e-430c-ad22-1ce34a492627",
  "message": "Your appeal has been recorded and is awaiting review.",
  "status": "under_review"
}
```

### What the log shows afterwards

Request:

```bat
curl.exe "http://127.0.0.1:5000/log?limit=2"
```

Response:

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.5919,
      "content_id": "8d2eb280-776e-430c-ad22-1ce34a492627",
      "creator_id": "student_001",
      "guess": "unsure",
      "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
      "model_score": 0.6568,
      "status": "decided",
      "style_score": 0.527,
      "timestamp": "2026-11-04T04:27:32+00:00"
    },
    {
      "content_id": "8d2eb280-776e-430c-ad22-1ce34a492627",
      "creator_id": "student_001",
      "event": "appeal",
      "reasoning": "I wrote this text myself and would like the classification reviewed.",
      "status": "under_review",
      "timestamp": "2026-11-04T04:28:21+00:00"
    }
  ]
}
```

The original decision remains in the log, and the appeal is appended as a separate event. A duplicate appeal for the same content ID was rejected with `already_appealed`.

### Input validation

I tested ten invalid submission cases, including missing or invalid fields, whitespace-only text, malformed JSON, JSON arrays, and oversized text.

The standalone validation test returned the expected HTTP 400 or 413 responses for all ten cases.

For a 10,001-character submission, the response was:

```text
413
{'error': 'text_too_long', 'message': 'The text must not exceed 10000 characters.'}
```

Passing these ten cases does not mean every possible invalid input is handled correctly. The broader attack set exposed additional cases.

---

## How I Used AI

### Moment 1

- **What I asked for:** Help understanding how the starter files and submission pipeline work.
- **What came back:** Explanations of `detector.py`, `stylometry.py`, `scoring.py`, `config.py`, and `audit.py`.
- **What I changed:** I used these explanations to document the pipeline and each signal's limitations.

### Moment 2

- **What I asked for:** Help developing five measurable acceptance criteria and choosing a combining rule.
- **What came back:** Suggested targets for false positives, score separation, label coverage, appeals, and input validation.
- **What I changed:** I selected equal signal weights and thresholds of 0.35 and 0.65, and documented the criteria for later evaluation.

### Implementation and evaluation assistance

I also used ChatGPT to help implement and test the Flask routes, stylometry functions, scoring labels, input validation, and short-text error handling.

During Unit 8, ChatGPT helped compare the individual signals, investigate passage length, interpret attack results, and draft this README. I ran the commands locally and reviewed the returned output.

The HELD/BROKE judgments below are manual interpretations of the recorded responses. They are separate from the attack script's automatic crash checks.

---

## Rate Limiting

**Configured limits:** 10 requests per minute and 200 requests per day.

**Why these limits:**

Ten requests per minute allows occasional submissions and revisions while slowing a script that repeatedly probes the detector. The daily limit restricts sustained use.

These are prototype policy choices. The available flood evidence demonstrates the minute limit; it does not establish that the daily limit was exercised.

**What a caller counts as:**

The limiter uses `creator_id`. This separates writers sharing a network, but an attacker can potentially bypass the limit by changing IDs. Authenticated identities would be needed for stronger enforcement.

**Flood test:**

```bat
python run_attacks.py --flood 15
```

Recorded status sequence:

```text
200, 200, 200, 200, 200,
200, 200, 200, 200, 200,
429, 429, 429, 429, 429
```

The evidence was saved in:

```text
results/flood_2026-11-10_1410.md
```

The full attack run also recorded ten accepted flood requests followed by two HTTP 429 responses. Its description mentions 20 submissions, but the actual report contains 12 flood rows. I report the 12 observed requests rather than claiming 20 were executed.

Rate-limit rejections are recorded in the audit log.

---

## Attack Run — Before

Command:

```bat
python run_attacks.py --set attack_set\attack_set --label before
```

Report:

```text
results/attack_run_2026-11-10_1424_before.md
```

Produced by `run_attacks.py::main`, targeting `app.py::submit`.

The report recorded 56 requests:

| Family | Requests |
|---|---:|
| Evasion | 10 |
| False positives | 8 |
| Prompt injection | 6 |
| Malformed requests | 20 |
| Flood | 12 |
| Total | 56 |

The script automatically marked one case BROKE because MF02 returned HTTP 500. It left 55 cases for manual judgment.

### Manual verdict rules

- **Evasion:** HELD means the known AI attack received `ai`; BROKE means it avoided that label. An unsure result is an evasion of positive detection, not a claim that the system verified human authorship.
- **False positives:** HELD means the human sample was not accused of AI use. BROKE means it received `ai`. An unsure result still leaves the writer without a definitive answer.
- **Malformed input:** HELD means an invalid or unscorable request was rejected with a controlled response. BROKE includes crashes and confident authorship classifications of non-prose inputs.
- **Prompt injection:** HELD refers only to the observed application-control boundary. A human classification by itself does not prove an instruction was followed.
- **Flood:** The first ten requests are permitted by the policy. HELD for later requests means the limit returned HTTP 429.

Right-to-left script is valid text, not inherently malformed. MF07 is judged as a language-support problem: the system should not make a strong authorship claim where its analysis is unsuitable.

### Every attack: before and after

The table records each observed response and my manual verdict. “Before” and “After” contain HTTP status and classification, not the report's confidence field.

| ID | Target | Before | After | Manual verdict, before → after |
|---|---|---|---|---|
| EV01 | Typos and vocabulary variety | 200 unsure | 200 unsure | BROKE → BROKE |
| EV02 | Split sentences | 200 unsure | 200 unsure | BROKE → BROKE |
| EV03 | Added quotation | 200 unsure | 200 unsure | BROKE → BROKE |
| EV04 | Unusual vocabulary | 200 unsure | 200 unsure | BROKE → BROKE |
| EV05 | Heavy editing | 200 unsure | 200 unsure | BROKE → BROKE |
| EV06 | Uneven sentence lengths | 200 unsure | 200 unsure | BROKE → BROKE |
| EV07 | Punctuation padding | 200 unsure | 200 unsure | BROKE → BROKE |
| EV08 | Token-window limitation | 200 unsure | 200 unsure | BROKE → BROKE |
| EV09 | Human opening added to AI text | 200 unsure | 200 unsure | BROKE → BROKE |
| EV10 | Repeated stanza structure | 200 ai | 200 ai | HELD → HELD |
| FP01 | Plain human writing | 200 unsure | 200 unsure | HELD → HELD |
| FP02 | Formal human writing | 200 ai | 200 ai | BROKE → BROKE |
| FP03 | Careful second-language writing | 200 ai | 200 ai | BROKE → BROKE |
| FP04 | Student essay following a rubric | 200 ai | 200 ai | BROKE → BROKE |
| FP05 | Human technical documentation | 200 ai | 200 ai | BROKE → BROKE |
| FP06 | Human template imitation | 200 ai | 200 ai | BROKE → BROKE |
| FP07 | Deliberate repetition | 200 ai | 200 ai | BROKE → BROKE |
| FP08 | Short human submission | 200 human | 200 human | HELD → HELD |
| PI01 | Ignore-the-check instruction | 200 unsure | 200 unsure | HELD → HELD, observed boundary |
| PI02 | Fake system message | 200 human | 200 human | HELD → HELD, observed boundary |
| PI03 | Instruction in writer's voice | 200 unsure | 200 unsure | HELD → HELD, observed boundary |
| PI04 | Hostile-label instruction | 200 unsure | 200 unsure | HELD → HELD, observed boundary |
| PI05 | Audit-log injection attempt | 200 unsure | 200 unsure | HELD → HELD, observed boundary |
| PI06 | Instruction plus human text | 200 unsure | 200 unsure | HELD → HELD, observed boundary |
| MF01 | Whitespace only | 400 | 400 | HELD → HELD |
| MF02 | Single character | 500 | 400 | BROKE → HELD |
| MF03 | Control characters | 200 human | 200 human | BROKE → BROKE |
| MF04 | Punctuation only | 200 human | 200 human | BROKE → BROKE |
| MF05 | Very long single word | 200 ai | 200 ai | BROKE → BROKE |
| MF06 | Emoji only | 200 ai | 200 ai | BROKE → BROKE |
| MF07 | Right-to-left script | 200 ai | 200 ai | BROKE → BROKE, unsupported-language handling |
| MF08 | 60,000 characters | 413 | 413 | HELD → HELD |
| RQ01 | Missing text | 400 | 400 | HELD → HELD |
| RQ02 | Missing creator ID | 400 | 400 | HELD → HELD |
| RQ03 | Numeric text | 400 | 400 | HELD → HELD |
| RQ04 | List as text | 400 | 400 | HELD → HELD |
| RQ05 | Null text | 400 | 400 | HELD → HELD |
| RQ06 | Object as creator ID | 400 | 400 | HELD → HELD |
| RQ07 | Array as request body | 400 | 400 | HELD → HELD |
| RQ08 | Unparseable JSON | 400 | 400 | HELD → HELD |
| RQ09 | Empty body | 400 | 400 | HELD → HELD |
| RQ10 | Form-encoded body | 400 | 400 | HELD → HELD |
| RQ11 | Incorrect content type | 400 | 400 | HELD → HELD |
| RQ12 | Nested invalid request structure | 400 | 400 | HELD → HELD |
| FL01_01 | Flood request 1 | 200 human | 200 human | HELD → HELD, permitted |
| FL01_02 | Flood request 2 | 200 human | 200 human | HELD → HELD, permitted |
| FL01_03 | Flood request 3 | 200 human | 200 human | HELD → HELD, permitted |
| FL01_04 | Flood request 4 | 200 human | 200 human | HELD → HELD, permitted |
| FL01_05 | Flood request 5 | 200 human | 200 human | HELD → HELD, permitted |
| FL01_06 | Flood request 6 | 200 human | 200 human | HELD → HELD, permitted |
| FL01_07 | Flood request 7 | 200 human | 200 human | HELD → HELD, permitted |
| FL01_08 | Flood request 8 | 200 human | 200 human | HELD → HELD, permitted |
| FL01_09 | Flood request 9 | 200 human | 200 human | HELD → HELD, permitted |
| FL01_10 | Flood request 10 | 200 human | 200 human | HELD → HELD, permitted |
| FL01_11 | Flood request 11 | 429 | 429 | HELD → HELD |
| FL01_12 | Flood request 12 | 429 | 429 | HELD → HELD |

The malformed family contains 20 requests: MF01–MF08 and RQ01–RQ12. After the fix, 15 were rejected and five were accepted. The five accepted cases were MF03–MF07.

The prompt-injection results do not establish complete resistance to every injection attack. They show no demonstrated instruction takeover in these recorded cases. In particular, PI02's human label alone cannot distinguish score manipulation from ordinary scoring behavior.

### The single worst outcome

The most concerning outcome was accusing human writers of AI use. Six of the eight false-positive attack samples received `ai`.

These eight attack samples are separate from the ten human samples used for acceptance Criterion 1.

The server error was a clear implementation defect, but a false accusation could have more serious consequences for a writer if a reviewer treated the result as proof.

---

## Ten Actual Audit Entries

The audit log was exported with:

```bat
curl.exe "http://127.0.0.1:5000/log?limit=200" > results\audit_extract.json
```

The following ten entries are copied from the export. They include evasion, false positives, prompt injection, unusual inputs, and a rate-limit rejection.

Decision entries contain nine fields. Rejection events currently use a smaller schema; I have preserved that difference rather than inventing missing values.

```json
[
  {
    "combined_score": 0.3821,
    "content_id": "d07914a1-5ab9-4cbe-be00-ac17f81734b4",
    "creator_id": "attacker_EV01",
    "guess": "unsure",
    "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
    "model_score": 0.1635,
    "status": "decided",
    "style_score": 0.6006,
    "timestamp": "2026-11-10T20:05:12+00:00"
  },
  {
    "combined_score": 0.4783,
    "content_id": "6f096ce9-020e-46ce-a910-aa722ce53f9f",
    "creator_id": "attacker_EV02",
    "guess": "unsure",
    "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
    "model_score": 0.5943,
    "status": "decided",
    "style_score": 0.3622,
    "timestamp": "2026-11-10T20:05:13+00:00"
  },
  {
    "combined_score": 0.6829,
    "content_id": "cc66d7fd-d06b-4624-8d6b-01316553ce52",
    "creator_id": "attacker_FP02",
    "guess": "ai",
    "label": "This writing shows patterns associated with AI-generated text, but this result is not proof of AI use.",
    "model_score": 0.7387,
    "status": "decided",
    "style_score": 0.6271,
    "timestamp": "2026-11-10T20:05:14+00:00"
  },
  {
    "combined_score": 0.6996,
    "content_id": "4a030aff-a0ed-4239-94f1-b18b789c73c7",
    "creator_id": "attacker_FP03",
    "guess": "ai",
    "label": "This writing shows patterns associated with AI-generated text, but this result is not proof of AI use.",
    "model_score": 0.8051,
    "status": "decided",
    "style_score": 0.594,
    "timestamp": "2026-11-10T20:05:14+00:00"
  },
  {
    "combined_score": 0.4317,
    "content_id": "412987d8-0504-4b1b-ad5f-d3d1f4a7418f",
    "creator_id": "attacker_PI05",
    "guess": "unsure",
    "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
    "model_score": 0.6401,
    "status": "decided",
    "style_score": 0.2233,
    "timestamp": "2026-11-10T20:05:15+00:00"
  },
  {
    "creator_id": "attacker_MF02",
    "event": "rejected",
    "limit": "Text is too short to score \u2014 a few sentences at least.",
    "reason": "detector_invalid_text",
    "status": "rejected",
    "timestamp": "2026-11-10T20:05:15+00:00"
  },
  {
    "combined_score": 0.25,
    "content_id": "2a6d55ad-f837-4902-b3fd-f408cac2cc4d",
    "creator_id": "attacker_MF03",
    "guess": "human",
    "label": "This writing appears more consistent with human-written text, but we cannot verify its authorship.",
    "model_score": 0.0,
    "status": "decided",
    "style_score": 0.5,
    "timestamp": "2026-11-10T20:05:15+00:00"
  },
  {
    "combined_score": 0.7485,
    "content_id": "4e0338ce-1432-4441-b249-ca2c29747f74",
    "creator_id": "attacker_MF06",
    "guess": "ai",
    "label": "This writing shows patterns associated with AI-generated text, but this result is not proof of AI use.",
    "model_score": 0.9969,
    "status": "decided",
    "style_score": 0.5,
    "timestamp": "2026-11-10T20:05:16+00:00"
  },
  {
    "combined_score": 0.7032,
    "content_id": "e10bea7f-e265-4b4a-8dee-887e7a7f6588",
    "creator_id": "attacker_MF07",
    "guess": "ai",
    "label": "This writing shows patterns associated with AI-generated text, but this result is not proof of AI use.",
    "model_score": 0.9064,
    "status": "decided",
    "style_score": 0.5,
    "timestamp": "2026-11-10T20:05:17+00:00"
  },
  {
    "creator_id": "attacker_flood",
    "event": "rejected",
    "limit": "10 per 1 minute",
    "reason": "rate_limited",
    "status": "rejected",
    "timestamp": "2026-11-10T20:05:17+00:00"
  }
]
```

These entries demonstrate that the short-text and rate-limit rejections were logged. They do not establish that every HTTP 400 or 413 rejection was logged.

---

## Run Log and Verdicts

The evaluation used ten human samples and ten AI samples.

Commands:

```bat
python run_eval.py --trials 3 --label before
python run_eval.py --trials 3 --label after
```

Reports:

```text
results/run_2026-11-10_1459_before.md
results/run_2026-11-10_1513_after.md
```

The updated scenarios and after report were committed in:

```text
ab9ccc6 — Add three-trial evaluation evidence for label coverage
```

The same samples were reused across trials. Repetition demonstrates repeatability on this set, not generalization to new writing.

| Criterion | Target | Trial 1 | Trial 2 | Trial 3 | Verdict |
|---|---|---|---|---|---|
| 1. Human false positives | At most 1 of 10 human samples receives high-confidence AI | 3/10 | 3/10 | 3/10 | FAIL |
| 2. Score separation | AI mean minus human mean at least 0.20 | Approximately +0.0064 | Approximately +0.0064 | Approximately +0.0064 | FAIL |
| 3. Label coverage | All three labels reachable | All three | All three | All three | PASS |
| 4. Appeals | Five successful appeals per trial | 5/5 | 5/5 | 5/5 | PASS in the separate appeal test |
| 5. Invalid inputs | All ten return expected HTTP 400 or 413 | Verify exact statuses in saved report | Verify exact statuses in saved report | Verify exact statuses in saved report | Standalone test passed 10/10; per-trial status evidence needs verification |

An em dash in the evaluation's printed classification list is not sufficient evidence of a correct rejection. HTTP status codes must be checked.

### Real evaluation output

The label-coverage portion of `run_eval.py`, using scenarios in `scenarios.py`, printed:

```text
label coverage  (criterion 3)
  trial 1: unsure, ai, ai, unsure, unsure, unsure, human
  trial 2: unsure, ai, ai, unsure, unsure, unsure, human
  trial 3: unsure, ai, ai, unsure, unsure, unsure, human
```

The precise evaluation function name still needs to be checked in `run_eval.py`; it is not identified by this output.

The additional coverage sample was:

```text
Went for a run. Legs hurt. Worth it.
```

It produced the human label. Adding this sample demonstrated reachability; it did not improve classification accuracy on the original human and AI groups.

### Individual signal results

I scored the existing samples separately with `detector.model_signal()` and `stylometry.style_signal()`.

| Signal | Human mean | AI mean | AI minus human |
|---|---:|---:|---:|
| GPT-2 model | 0.6295 | 0.6480 | +0.0185 |
| Stylometry | 0.6026 | 0.5970 | -0.0056 |
| Combined evaluation | 0.6161 | 0.6225 | +0.0064 |

The means are rounded. Small differences between separately calculated diagnostics and the service evaluation should not be interpreted as improvements.

The model signal provides little separation. The style signal's mean difference is slightly in the wrong direction.

Changing classification thresholds cannot fix Criterion 2 because thresholds affect labels rather than scores. With these unchanged signals, adjusting their nonnegative weights alone cannot produce a mean gap of 0.20.

### Approximate-length diagnostic

Word counts from `stylometry.words()` were:

```text
Human:
[85, 259, 195, 350, 114, 156, 133, 122, 183, 182]

AI:
[95, 88, 85, 86, 90, 91, 89, 90, 90, 94]

Human mean: 177.9 words
AI mean: 89.8 words
```

I then scored approximately the first 90 whitespace-separated words of each passage, retaining the entire passage when shorter.

I did not replace the official samples or modify the scoring formulas.

| Signal | Human mean | AI mean | AI minus human |
|---|---:|---:|---:|
| GPT-2 model | 0.5516 | 0.6442 | +0.0926 |
| Stylometry | 0.5497 | 0.6000 | +0.0503 |
| Combined, approximately calculated from signal means | 0.5507 | 0.6221 | +0.0715 |

The diagnostic increased the combined separation, but it remained below 0.20.

This experiment does not isolate length. Truncation also changes content, punctuation, and sentence boundaries. Some passages remain shorter than 90 words, and the word-count and truncation commands use different splitting rules.

The results support further investigation of length effects. They do not establish improved authorship detection or satisfy Criterion 2.

### Diagnoses: stages and mechanisms

**Criterion 1 and FP02–FP07: false accusations**

The failure involves signal one, signal two, the combining rule, and label mapping.

Predictable human prose receives a high model signal. Structured writing and repeated vocabulary can also receive a high style signal. Their average crosses 0.65, and the label mapper returns AI.

For FP03:

```text
Model signal: 0.8051
Style signal: 0.5940
Combined score: 0.6996
Label: ai
```

The style signal reduces the model score but does not reduce the average below the AI threshold. This is a concrete example of the combining rule failing to protect a human writer.

**Criterion 2: overlapping signals**

Neither signal separates the evaluation groups sufficiently. Equal weighting combines two weak signals and produces a mean difference near zero.

The length imbalance is a plausible contributing factor, especially for type-token ratio. The truncation diagnostic also changes other properties, so it cannot identify length as the only cause.

**EV01, EV02, EV03, EV06, and EV07: style-sensitive evasion**

The targeted mechanisms are vocabulary variation, sentence-length spread, quotations, and punctuation density.

These properties can be changed without changing authorship. Their scores feed into the weighted average, which leaves the final result unsure.

For EV02, the recorded model score was 0.5943 and the style score was 0.3622. Their combined score was 0.4783, producing unsure.

The run establishes the resulting classification. Without paired unmodified versions, it does not measure how much each edit caused the score to move.

**EV04 and EV08: model-signal limitations**

Unusual vocabulary can raise perplexity, reducing the AI-like model signal. A finite token window also limits which text the model evaluates.

EV04 and EV08 received unsure. Their targeted mechanisms are consistent with known implementation limits, but this run alone does not isolate the effect of each modification.

**EV05 and EV09: mixed or edited writing**

Heavy editing and mixed human/AI passages complicate a single authorship label. Both signals evaluate surface patterns without identifying which portions came from which author.

Both attacks received unsure.

**MF02: unhandled short-text exception**

The route accepted a nonempty string, but `detector.perplexity()` requires at least three tokens. A single-character input raised `ValueError`.

Before the fix, the route did not catch that error and returned HTTP 500. The improved route returns HTTP 400 and logs the rejection.

**MF03–MF06: insufficient suitability checks**

The route permits inputs that are strings but do not provide useful prose for authorship analysis.

For control characters, the model score was 0.0 and the style fallback was 0.5. The average became 0.25, producing human.

For emoji-only text, the model score was 0.9969 and the style fallback was 0.5. The average became 0.7485, producing AI.

The neutral style fallback does not prevent a strong model signal from producing an authorship label.

**MF07: language-support mismatch**

The style word extractor does not meaningfully analyze the submitted script. It returns a neutral style score of 0.5, while the model score of 0.9064 drives the average to 0.7032.

The resulting AI label is unsupported as an authorship conclusion. The appropriate response would be an explicit language-support limitation or abstention, rather than treating the script itself as invalid.

**Prompt injection: observed application boundary**

The recorded responses remained within the application's normal classification format. The model is used for perplexity, and label text is chosen by application code.

The audit entry for PI05 remained a structured decision event. No demonstrated instruction takeover is established by these outputs.

This does not prove that every possible injection or logging attack is prevented.

**Rate-limit bypass: caller identity**

The observed per-creator minute limit worked. However, `creator_id` is supplied by the caller, so changing it could evade the intended restriction. The flood test does not evaluate that bypass.

---

## The Improvement

**What I changed:**

I updated the submission route in `app.py` to catch the detector's short-text `ValueError`.

The route now returns a controlled HTTP 400 response and records a rejection event.

**Which diagnosis pointed at it:**

MF02 submitted:

```text
a
```

The detector could not score the input. The uncaught exception produced HTTP 500.

After the change, the response was:

```json
{
  "error": "text_too_short",
  "message": "Text is too short to score — a few sentences at least."
}
```

The audit entry records:

```text
creator_id: attacker_MF02
reason: detector_invalid_text
status: rejected
```

### Attack Run — After

Command:

```bat
python run_attacks.py --set attack_set\attack_set --label after
```

Report:

```text
results/attack_run_2026-11-10_1505_after.md
```

The complete before/after outcomes appear in the attack table above.

The after report recorded:

```text
56 attacks
Auto-marked BROKE (5xx, crash, no response): 0
Left for manual judgment: 56
```

**Did it help, and how do I know?**

Yes. MF02 changed from HTTP 500 to HTTP 400, and the audit export contains the corresponding rejection.

This fixes the reproduced unhandled-error response. It does not prove that all possible server errors are fixed.

The change did not modify either signal or their weights. The false-positive, evasion, and unsuitable-input classifications remained unresolved.

Zero automatically marked BROKE means the script observed no 5xx responses, crashes, or missing responses in that run. It does not mean all attacks were defended successfully.

---

## What's Still Broken

### Human false positives

Criterion 1 remains unmet: three of ten evaluation samples received AI labels. Separately, six of eight false-positive attack samples received AI labels.

A future experiment could raise the AI threshold using a separate calibration set, then evaluate the change on held-out data. This may reduce accusations while producing more unsure results and missed AI text.

I have not claimed that this improvement has been tested.

### Poor score separation

Criterion 2 remains unmet. The original mean difference was approximately 0.0064 against a target of 0.20.

Future work should use independently sourced human and AI passages with comparable topics and lengths, separate calibration and evaluation sets, and investigation of length-aware vocabulary measurements.

I stopped short of changing formulas solely to pass the existing small test set.

### Evasion and mixed authorship

Nine of ten evasion samples avoided the AI label by receiving unsure. This demonstrates limited positive detection on those samples, not verified human authorship.

Additional paired tests would be needed to measure the causal effect of typos, paraphrases, quotations, punctuation, and mixed passages.

### Unsuitable inputs and language support

Control characters, punctuation-only text, a very long single word, emoji-only text, and right-to-left text still received authorship labels.

The route needs a clearer supported-input policy and an abstention response when the signals are not meaningful. Valid non-English writing should not be treated as inherently malformed.

### Rate-limit bypass

A caller can potentially change creator IDs. Authenticated identities and additional abuse controls would be needed before relying on the limiter.

The daily limit has not been demonstrated by the supplied flood test.

### Audit completeness

Decision events contain nine fields, but the recorded rejection events use fewer fields and do not include content IDs or signal fields.

The export demonstrates logging of short-text and rate-limit rejections. It does not demonstrate logging for every validation rejection.

The checklist requirement concerning all nine audit fields and rejected requests should therefore not be marked fully complete without checking and, if necessary, updating the logging implementation.

### Remaining documentation checks

The exact per-trial HTTP statuses for Criterion 5 still need verification from the saved evaluation report.

The precise function responsible for the pasted evaluation output also needs verification in `run_eval.py`.

Repository URL and required commit counts must be checked before submission.

### General reliability

Twenty authorship-labeled evaluation samples and repeated trials on the same inputs do not establish generalization, fairness across writer groups, or reliable performance across languages and genres.

The score and confidence field are heuristic indicators, not verified probabilities of authorship.

### Why I stopped

I prioritized fixing the reproduced HTTP 500 response and documenting the remaining failures. Reliable authorship classification would require more data, independent evaluation, and better-supported signals.

### The trade I'd make if this ran for real

I would favor more unsure results and human review to reduce false accusations against writers, especially those whose plain or second-language writing is penalized by predictability-based scoring. Reviewers would face additional work, and more AI-generated writing could remain undetected.

---

## Submission Checklist

### Unit 7

- [ ] Verify `criteria.md` contains five numbered criteria and reasons.
- [x] Document the submission pipeline.
- [x] Describe both signals and their blind spots.
- [x] Name `scoring.py::combine_signals`.
- [x] Document all three labels and score ranges.
- [x] Include a submission, appeal, and audit output.
- [ ] Verify the required commit count.
- [ ] Include the repository URL in the submission.

### Unit 8

- [x] Explain configured rate limits and caller identity.
- [x] Include a flood status sequence showing HTTP 429.
- [x] Include all 56 observed attack outcomes and manual judgments.
- [x] Paste ten actual audit entries.
- [x] Diagnose failed criteria and broken attack families by stage and mechanism.
- [x] Document the short-text improvement and after run.
- [x] Document remaining failures and the production tradeoff.
- [ ] Verify Criterion 5's exact HTTP results across all three trials.
- [ ] Verify the evaluation output's precise function name.
- [ ] Resolve or document audit-schema and rejection-coverage requirements.
- [ ] Verify the required Unit 8 commit count.
- [ ] Submit the same repository URL used for Unit 7.

Do not delete and recreate the repository.

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**