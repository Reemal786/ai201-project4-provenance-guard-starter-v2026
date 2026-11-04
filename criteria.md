
# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---

## 1. Minimize false accusations against human writers

Of 10 pieces of human-written text, no more than 1 should receive a high-confidence AI label in each trial.

**Why this target:**

A false accusation can damage a writer's credibility and unfairly question the originality of their work. I chose a maximum false-positive rate of 10% because protecting human writers should take priority over detecting every instance of AI-generated writing.

---

## 2. Distinguish between clearly AI-generated and human-written text

Across 10 clearly AI-generated and 10 clearly human-written samples, the average combined score for AI-generated text should be at least 0.20 higher than the average score for human-written text in each trial.

**Why this target:**

The detector should demonstrate a measurable difference between AI-generated and human-written text. A minimum average score difference of 0.20 provides a meaningful separation without expecting perfect detection, which is unrealistic given the limitations of both signals.

---

## 3. Make all three classification labels reachable

The system must successfully produce all three classifications—high-confidence human, unsure, and high-confidence AI—using at least one test input for each label in every trial.

**Why this target:**

Each classification serves a different purpose. The unsure label is particularly important because the system should acknowledge uncertainty instead of forcing every submission into a human or AI category.

---

## 4. Record and process every valid appeal

For 5 valid appeals associated with existing content IDs, all 5 must return a successful response, create an audit log entry, and record the submission's status as `under_review` in every trial.

**Why this target:**

Writers should have a reliable way to challenge potentially incorrect classifications. A 100% success target is appropriate because the appeal process is essential for accountability and should not depend on the detector's accuracy.

---

## 5. Handle invalid submissions without crashing

For 10 invalid submissions, including missing text, empty text, incorrect data types, and excessively long inputs, all 10 must return an appropriate client-error response (HTTP 400 or 413) without causing an unhandled exception or stopping the service in every trial.

**Why this target:**

A reliable service must handle unexpected or malformed input safely. I chose a 100% target because input validation is a basic requirement for a functional API, and invalid submissions should never cause the application to crash.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
           of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
