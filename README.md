
# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> And in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

1. A writer submits their text and creator ID through the `POST /submit` endpoint, where the Flask application receives the request as JSON.

2. The service extracts the submitted text and passes it to `detector.model_signal()`, which uses GPT-2 to calculate perplexity and convert it into a score between 0 and 1. Higher scores indicate more AI-like writing.

3. The text is also passed to `stylometry.style_signal()`, which examines sentence length variation, vocabulary diversity, and punctuation density to produce a second score.

4. Both scores are passed to `scoring.combine_signals()`, which combines them using a weighted average to calculate an overall AI-likeness score.

5. The combined score is passed to `scoring.score_to_label()`, which assigns one of three classifications: high-confidence human, unsure, or high-confidence AI.

6. The service generates a unique content ID and records the decision using `audit.log_decision()`. The audit log stores the creator ID, individual signal scores, combined score, classification, and decision status.

7. Finally, the service returns a JSON response containing the content ID, prediction, classification-strength score, reader-facing label, and both signal scores. If the writer disagrees with the result, they can submit an appeal through `POST /appeal`, which records their reasoning and appends an `under_review` event to the audit log.

The system also validates submitted data before running the detector. Requests with missing or invalid fields return HTTP 400, while text exceeding 10,000 characters returns HTTP 413.

The classifications are heuristic estimates based on writing patterns. They are not proof of whether a person or AI wrote the text.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**

The model signal uses GPT-2 to calculate perplexity, which measures how predictable a piece of writing is to a language model. The perplexity is converted into a score between 0 and 1, where higher scores indicate more AI-like writing.

**Why that might differ between human and AI writing:**

AI-generated writing often follows predictable word patterns because language models generate text by selecting likely next tokens. Human writing may contain unexpected vocabulary, unusual sentence structures, or personal expressions that are harder for a language model to predict.

**What it can't see:**

The model cannot determine who actually wrote the text. Human writing that uses simple vocabulary and straightforward sentences may receive a high AI score, particularly for writers using a second language or deliberately writing plainly. Similarly, AI-generated text containing unusual vocabulary may appear more human-like. Therefore, predictability alone is not reliable evidence of authorship.

### Signal two — the style signal

**What it measures:**

The style signal examines the structure of writing using three measurements: sentence length variation, type-token ratio, and punctuation density. These measurements evaluate how much sentence lengths vary, how frequently vocabulary repeats, and how punctuation is distributed throughout the text.

**Why that might differ between human and AI writing:**

AI-generated writing may contain more consistent sentence lengths, repetitive vocabulary, and predictable punctuation patterns. Human writing can have greater variation in sentence structure, word choice, and punctuation. By examining these characteristics, the style signal attempts to identify patterns associated with AI-generated writing.

**What it can't see:**

The style signal cannot understand the meaning or context of the writing. Simple changes, such as adding typos, adjusting punctuation, or splitting sentences, can influence its score without changing the content. It may also misinterpret human writing that naturally follows consistent patterns. Therefore, writing style alone cannot reliably determine authorship.

### The combining rule

**The rule:**

The system combines the model signal and style signal using a weighted average. Both signals contribute equally to the final score because they measure different characteristics of writing, and neither can reliably determine authorship on its own.

When the signals disagree, the weighted average produces a score between their individual predictions. This allows conflicting evidence to result in an unsure classification rather than automatically labeling the writing as human or AI-generated. I chose this approach because incorrectly accusing a human writer of using AI is more harmful than failing to identify some AI-generated text.

**The numbers:**

- Model signal weight: 0.50 (50%)
- Style signal weight: 0.50 (50%)
- Human threshold: 0.35
- AI threshold: 0.65

The combined score is calculated as:

`combined_score = (0.50 * model_score) + (0.50 * style_score)`

A score of 0.35 or lower receives a high-confidence human label, a score greater than 0.35 but lower than 0.65 receives an unsure label, and a score of 0.65 or higher receives a high-confidence AI label.

The API also returns a field named `confidence`, calculated as:

`confidence = 2 * abs(combined_score - 0.50)`

This measures how far the combined score is from the uncertain midpoint. It is a classification-strength indicator, not a calibrated probability of authorship.

These are the initial settings. They may be adjusted after evaluating the system's behavior.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

For example, if the model signal produces 0.90 and the style signal produces 0.10, the combined score is:

`(0.50 * 0.90) + (0.50 * 0.10) = 0.50`

This falls within the unsure range. Instead of making a confident classification based on one signal, the system acknowledges that the evidence is conflicting.

During actual testing, I submitted the following text:

"I spent the afternoon walking through the park and watching the birds near the pond."

The detector returned:

- Model signal: 0.6568
- Style signal: 0.5270
- Combined score: 0.5919
- Classification: unsure

The combined score was calculated as:

`(0.50 * 0.6568) + (0.50 * 0.5270) = 0.5919`

Although the model signal was above the AI threshold, the style signal was lower. Combining both signals produced an unsure classification instead of labeling the writing as AI-generated.

This example demonstrates why I chose to combine different signals rather than rely entirely on one measurement.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00–0.35 (inclusive) | This writing appears more consistent with human-written text, but we cannot verify its authorship. |
| unsure | Greater than 0.35 and less than 0.65 | We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation. |
| high-confidence AI | 0.65–1.00 (inclusive) | This writing shows patterns associated with AI-generated text, but this result is not proof of AI use. |

**Why I worded the "unsure" one this way:**

I wanted the unsure classification to communicate uncertainty without implying that the writer had done anything wrong. AI detection systems cannot reliably establish authorship from writing patterns alone, and a human writer could receive an uncertain result even when they wrote every word themselves.

By explicitly stating that the result is not an accusation, I hope to prevent readers from treating an inconclusive prediction as evidence of misconduct. I also wanted the message to be understandable to someone unfamiliar with AI detection or technical scoring systems.

The high-confidence labels similarly avoid claiming that the system can prove authorship. The word "confidence" refers to the detector's scoring rules, not verified certainty about who wrote the text.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

I submitted a short sample of writing using the `/submit` endpoint.

Request (Windows Command Prompt):

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

The system returned an unsure classification because the combined score was 0.5919, which falls between the human and AI thresholds.

**An appeal**

I then submitted an appeal using the content ID from the original submission.

Request (Windows Command Prompt):

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

The appeal was accepted, and the system recorded the writer's reasoning for requesting a review.

**What the log shows afterwards**

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

The audit log preserves the original classification with `status: "decided"` and appends a separate appeal event with `status: "under_review"`.

This append-only approach preserves the history of the original decision rather than replacing it. It allows someone reviewing the log to see what was originally decided, when the appeal was submitted, and why the writer challenged the classification.

I also tested submitting another appeal for the same content ID. The system rejected the duplicate with an `already_appealed` error, preventing multiple appeal events for the same submission.

**Input validation**

I tested 10 invalid submission cases, including missing text, numeric text, whitespace-only text, missing or invalid creator IDs, missing JSON, malformed JSON, JSON arrays, and oversized submissions.

All 10 cases returned the expected HTTP 400 or 413 response.

For example, submitting 10,001 characters produced:

```text
413
{'error': 'text_too_long', 'message': 'The text must not exceed 10000 characters.'}
```

This confirms that excessively long text is rejected before running the detector.

---

## How I Used AI

**Moment 1**

- **What I asked for:** I asked ChatGPT to help me understand the starter code and how the model signal, style signal, scoring system, and audit log work together.
- **What came back:** ChatGPT explained the responsibilities of `detector.py`, `stylometry.py`, `scoring.py`, `config.py`, and `audit.py`, and helped me organize the submission process into seven steps.
- **What I changed:** I used these explanations to document the intended submission pipeline and the limitations of both detection signals in my README.

**Moment 2**

- **What I asked for:** I asked ChatGPT to help me develop five measurable acceptance criteria and choose an initial combining rule that considers false accusations against human writers.
- **What came back:** ChatGPT suggested measurable targets for false positives, score separation, label coverage, appeals, and invalid input handling. It also recommended keeping equal signal weights until calibration.
- **What I changed:** I chose an initial 50/50 weighted average with human and AI thresholds of 0.35 and 0.65, prioritizing an unsure classification when the signals disagree. I documented these decisions and the acceptance criteria for later evaluation.

**Additional implementation assistance**

I also used ChatGPT to help implement and test the Flask submission and appeal endpoints, stylometry calculations, scoring labels, and input validation. I reviewed the proposed changes, ran the commands in my local environment, inspected the responses, and committed the working implementation to Git.

---

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**

<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:**

<!-- per address, or per creator_id? They fail differently — one script can
     look like a thousand callers, and one household can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
```

**The single worst outcome** — the one I'd least want to explain to a writer whose work got caught by it:

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. | | | | | |
| 2. | | | | | |
| 3. | | | | | |
| 4. | | | | | |
| 5. | | | | | |

**Real output from one trial**, pasted as text, naming the file and function that produced it:

```json
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis: "The evasion attacks got through."

     A diagnosis: "Four evasion inputs got through. All four had typos
     added to AI-generated text. My second signal measures word variety,
     and typos raise word variety — so it read them as more human. My
     combining rule weights that signal at 0.6, so it dragged the whole
     score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

<!-- ═════════════════════════════════════════════════════════════════════
     SUBMISSION CHECKLIST — unit 7

     [ ] criteria.md has five numbered criteria, each naming a target
     [ ] Each has a reason underneath
     [ ] POST /submit returns content_id, guess, confidence, label,
         model_score and style_score
     [ ] Two signals that measure DIFFERENT things, each with a named blind spot
     [ ] Three label variants, all reachable, written out in full
     [ ] POST /appeal changes status and writes to the log
     [ ] Signals and Scoring names scoring.py::combine_signals
     [ ] Sample Run: a submission AND an appeal, as pasted text
     [ ] At least four new commits
     [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

     [ ] Rate limiting on /submit, with your numbers justified
     [ ] The pasted run of status codes showing 429
     [ ] Audit log with all nine fields, recording rejections too
     [ ] The attack set run IN FULL, every input with an outcome
     [ ] Ten audit log entries pasted as text
     [ ] Five criteria across three trials
     [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
     [ ] One improvement, with Attack Run — After
     [ ] What's Still Broken, including the production trade
     [ ] At least four new commits
     [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
