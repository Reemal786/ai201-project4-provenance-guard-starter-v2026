
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
> and in another:
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

4. Both scores are passed to `scoring.combine_signals()`, which combines them using a weighted average to calculate an overall AI-likelihood score.

5. The combined score is passed to `scoring.score_to_label()`, which assigns one of three classifications: high-confidence human, unsure, or high-confidence AI.

6. The service generates a unique content ID and records the decision using `audit.log_decision()`. The audit log stores the creator ID, individual signal scores, combined score, classification, and decision status.

7. Finally, the service returns a JSON response containing the content ID, prediction, confidence score, classification label, and both signal scores. If the writer disagrees with the result, they can submit an appeal through `POST /appeal`, which records their reasoning and changes the item's status to `under_review`.

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

These are the initial settings. They may be adjusted after evaluating the system's behavior.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

For example, if the model signal produces 0.90 and the style signal produces 0.10, the combined score is:

`(0.50 * 0.90) + (0.50 * 0.10) = 0.50`

This falls within the unsure range. Instead of making a confident classification based on one signal, the system acknowledges that the evidence is conflicting.

This is an illustrative example. An actual disagreement observed during calibration will be documented after Milestone 4.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | | |
| unsure | | |
| high-confidence AI | | |

**Why I worded the "unsure" one this way:**

<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

To be completed in Milestone 5 after implementing the three label messages.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
```

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

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

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
