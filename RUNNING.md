# Running Provenance Guard

Everything about how the starter works.

This is a **web service**. It runs on your machine and you talk to it with
`curl` from another terminal. If you've not built a backend before, that's
assumed — the starter ships one that already answers.

---

## Before your first class

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python test.py
```

**You're ready when `python test.py` passes.**

You'll see `[WARN] Detector model — not downloaded yet`:

```bash
python detector.py
```

That downloads about 550 MB and scores a sample.

> **No API key for this pair.** Nothing here calls a hosted service. The model
> that reads your text runs on your own laptop.

---

## Your first five minutes

Two terminals. In the first:

```bash
python app.py
```

In the second:

```bash
curl -X POST http://127.0.0.1:5000/ping \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

You should get JSON back. That's the whole idea of a web service — something
sent it data, it sent something back.

> **On Windows, use `curl.exe` and keep it on one line.**
>
> In PowerShell, `curl` is an alias for a different tool and the command above
> fails with `Cannot bind parameter 'Headers'` before it ever reaches your
> service. The `\` line breaks don't work there either. This does:
>
> ```powershell
> curl.exe -X POST http://127.0.0.1:5000/ping -H "Content-Type: application/json" -d '{\"message\": \"hello\"}'
> ```
>
> Every `curl` command in this file and in the brief works the same way: swap
> `curl` for `curl.exe` and put it on one line. Git Bash needs no change.

**Leave `/ping` alone.** It's your control. When something breaks later, check
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself, and that's a help-channel question.

Then try the route you're going to build:

```bash
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "some writing", "creator_id": "me"}'
```

It returns a `501` saying it isn't built yet. **That's the correct starting
position.**

---

## The routes

| Route | State | What it does |
|---|---|---|
| `POST /ping` | **works** | The example. Don't edit it |
| `GET /health` | **works** | Is the service up, is the model loaded |
| `GET /log` | **works** | The audit log, as JSON |
| `POST /submit` | **you build it** | Milestones 3, 4, 5 |
| `POST /appeal` | **you build it** | Milestone 5 |

---

## Every command

| Command | What it does |
|---|---|
| `python test.py` | Checks your environment |
| `python app.py` | Runs the service |
| `python detector.py` | Downloads the model and scores a sample — **run before class** |
| `python detector.py "some text"` | Score one piece of text from the terminal |
| `python stylometry.py "some text"` | Your style measures, on one piece of text |
| `python run_attacks.py --set <folder>` | The attack set — **unit 8** |
| `python run_attacks.py --flood 15` | Push past your rate limit and print the status codes — **unit 8** |
| `python run_eval.py --label before` | Your five criteria, three trials — **unit 8** |

---

## Which piece goes with which milestone

### Unit 7 — the build

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Trace a submission on paper | Nothing to run |
| 2 | Write your criteria | `criteria.md` — all five are yours |
| 3 | The route, one signal, the log | `app.py::submit`, `detector.py`, `audit.py` |
| 4 | Second signal, combine, score | `stylometry.py`, `scoring.py::combine_signals` |
| 5 | Labels and the appeal path | `scoring.py::score_to_label`, `app.py::appeal` |
| 6 | Write it up | `README.md` |

### Unit 8 — the test

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Rate limiting and the full log | `config.py`, the decorator in `app.py` |
| 2 | Run the attack set | `run_attacks.py` |
| 3 | Run your own criteria | `scenarios.py`, `run_eval.py` |
| 4 | Verdicts and diagnoses | `README.md` |
| 5 | Fix one thing, re-run | `run_attacks.py --label after` |
| 6 | What's still broken | `README.md` |

---

## Building `/submit` in three passes

The ordering is deliberate. It's how you tell a broken route from a broken
signal.

**Milestone 3.** Return a hardcoded response. Confirm `curl` gets it back
**before** you add any logic. Then pull `text` and `creator_id` out. Then call
one signal. Then log it.

**Milestone 4.** Add the second signal. Combine them. Log both scores.

**Milestone 5.** Turn the score into a label.

> Test each signal from a terminal on its own before wiring it in. If you skip
> that you'll spend an hour not knowing whether the route or the signal is
> lying to you.

---

## Turning on rate limiting (unit 8)

Three steps:

1. In `config.py`, set `RATE_LIMITING_ENABLED = True` — or run with
   `AI201_RATE_LIMITS=1`.
2. Choose your numbers there.
3. In `app.py`, uncomment the `@limiter.limit(...)` line above `submit`.

Then push past your limit and watch for `429`:

```bash
python run_attacks.py --flood 15
```

That sends 15 submissions from one `creator_id` and prints the run of status
codes — `200 200 200 ... 429 429` — which is exactly what your README's **Rate
Limiting** section asks you to paste. It also writes `results/flood_<date>.md`.

The attack set can't do this for you. Every attack row submits under its own
`creator_id`, so a full attack run looks like forty-odd different callers and
never trips a limit however long it is.

No `429` at all? Either your limit is above 15 a minute, or rate limiting is
still off. `GET /health` reports which.

Rejections are logged for you. **An attack that shows up only as an absence is
one you'll never find** — a thousand requests that got a `429` and left no
trace look exactly like a quiet afternoon.

---

## Running it somewhere else (unit 9)

Unit 9 asks you to deploy one of your systems. **Read this before you pick
which one** — for this project the answer is already decided, and it isn't the
hosted one.

Flask's built-in server says "development server" on startup because that's
what it is. A real one comes from `gunicorn`, which is in
`requirements.txt` and unused until now:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

Two settings do the work, and both read the environment:

| Variable | Default | What it does |
|---|---|---|
| `HOST` | `127.0.0.1` | Loopback — your machine only. A host needs `0.0.0.0`, or nothing outside the box can reach the service and it looks like the app is down |
| `PORT` | `5000` | Most hosts hand you a port in `PORT` and expect you to bind exactly that one |
| `AI201_DEBUG` | `1` | Debug mode. Off automatically whenever `HOST` isn't loopback — an interactive debugger on a public address is a stranger's Python prompt inside your process |

Nothing about your local workflow changes. With no variables set you get
`http://127.0.0.1:5000` and every `curl` above still works.

### This project will not fit a free host

Say it plainly, because the arithmetic is the point:

| What has to be in memory | Roughly |
|---|---|
| `torch` | ~200–800 MB depending on the build |
| the `gpt2` weights | ~550 MB on disk, loaded into RAM to score |
| Flask, gunicorn, your code | the rest |
| **A free tier gives you** | **512 MB** |

That's over budget before a single request arrives — and a free host has no
persistent disk, so the 550 MB download starts again after every idle
spin-down. There is no configuration that fixes this. The model is the size it
is.

**So pair 4 extensions take Path B — local, with logs.** That is the expected
answer for this project, not a fallback and not a failure. Working out that a
system doesn't fit its host *before* you spend an evening watching it get
killed is the skill unit 9 is actually testing. Write the arithmetic above in
your write-up; that's the deliverable.

---

## Where everything lives

| File | What it does |
|---|---|
| `config.py` | Every setting: thresholds, weights, rate limits, the model |
| `app.py` | The service. `/ping` and `/log` work; `/submit` and `/appeal` are yours |
| `detector.py` | Signal one — the local model. Given to you |
| `stylometry.py` | Signal two. **Stubs — you build these** |
| `scoring.py` | Combining and labelling. **Stubs — you build these** |
| `audit.py` | The audit log writer. Given to you |
| `run_attacks.py` | Runs the attack set — **unit 8** |
| `run_eval.py` | Runs your criteria three times — **unit 8** |
| `scenarios.py` | What your test runs. **You fill this in** |
| `criteria.md` | Your five criteria. **You write all five** |
| `logs/audit.jsonl` | Your audit log. **Commit it** |
| `results/` | Attack runs and run logs. **Commit them** |

---

## The two blind spots, up front

Both signals have one, and unit 8's attack set is built out of them. You have
to name them yourself in Milestone 1 — but knowing they exist now saves you
from being surprised.

**Signal one** measures how *predictable* your text is. Predictability isn't
authorship. What it really rewards is common words in short, ordinary
sentences — someone writing in a second language and staying with vocabulary
they're sure of, a younger writer, anyone writing plainly on purpose. Writing
like that scores about as machine-like as machine writing does. (Dense, ornate
prose often goes the other way and reads as human, because rare words are what
a language model fails to predict.) So the writers this signal is most likely
to accuse are the ones with the least room to argue back. That is the false
positive the whole project is about, and it's structural rather than a bug.

**Signal two** cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — typos, broken-up
sentences, a pasted quotation. That is very cheap to do on purpose.

---

## When something goes wrong

| What you see | What it means |
|---|---|
| `501 not_implemented` | Correct at the start — that's the TODO in `app.py` |
| `404` from curl | Is the server running? Is the path exactly what you typed? |
| `Cannot bind parameter 'Headers'` | You're in PowerShell, where `curl` is a different tool. Use `curl.exe`, on one line |
| Request body arrives empty | curl needs `-H "Content-Type: application/json"` |
| `Address already in use` | A server left running from an earlier attempt. Kill it, don't debug it |
| The first submission takes 10+ seconds | Signal one is loading the model into memory. Later ones take a second or two |
| *Every* submission takes 10+ seconds | Something is reloading the model each call. `GET /health` shows `detector_loaded` — if it goes back to `false`, look for a reload in your handler |
| `DetectorUnavailable` | Run `python detector.py` once to download the model |
| `/appeal` seems to do nothing | Does the `content_id` you sent actually exist in the log? A typo there fails silently |
| Every request gets through, no `429` ever | The decorator is uncommented but limiting is still off. Set `RATE_LIMITING_ENABLED` in `config.py` |
| Flask-Limiter warns about storage | Shouldn't happen — `storage_uri` is preconfigured. If you changed it, put it back |
| All three of your labels never appear | Your ranges have a gap. `scoring.label_ranges()` prints them |

If the route won't respond, go back to `/ping`. If that answers, the problem is
in your handler.

---

## A note on committing

At least four new commits in unit 7, four more in unit 8.

`logs/` and `results/` are deliberately **not** in `.gitignore`. Your audit log
is evidence, and the entries you paste into your README are what unit 8 grades.

**Do not delete and recreate this repository.** You submit the same URL both
units.


## Capstone — Local with Logs (Unit 9)

### Overview

The capstone extends Provenance Guard using **Shape B: Harden Against Failure** and **Path B: Local with Logs**.

The Flask service retains its original classification, appeal, audit, and rate-limiting functionality while adding controlled HTTP 503 responses for unexpected analysis failures and structured request monitoring.

The original extension catches unexpected exceptions in `detector.model_signal()`. The Milestone 6 improvement also catches unexpected exceptions from `stylometry.style_signal()`, `scoring.combine_signals()`, and `scoring.score_to_label()`.

Invalid requests continue to receive their existing validation responses.

### Local Setup and Startup

Use Python 3.13 in the activated virtual environment.

In Windows Command Prompt, from the repository root:

```cmd
.venv\Scripts\activate.bat
pip install -r requirements.txt
python test.py
```

To run the live service, open **Terminal 1**:

```cmd
python app.py
```

In **Terminal 2**, check the health endpoint:

```cmd
curl.exe http://127.0.0.1:5000/health
```

The local URL is `http://127.0.0.1:5000` with the default configuration.

A first real classification may need to load the GPT-2 model. The model runs locally; no hosted inference API is required.

### HTTP Failure Behavior

| Situation | HTTP Status | Response Error | Audit Reason |
|---|---|---|---|
| Invalid or missing text | 400 | `invalid_text` | Validation rejection behavior |
| Missing creator ID | 400 | `invalid_creator_id` | Validation rejection behavior |
| Text exceeds configured length | 413 | `text_too_long` | Validation rejection behavior |
| Detector rejects text as too short | 400 | `text_too_short` | `detector_invalid_text` |
| Unexpected detector exception | 503 | `detector_unavailable` | `detector_unavailable` |
| Unexpected stylometry/scoring exception | 503 | `analysis_unavailable` | `analysis_pipeline_error` |

For unexpected analysis exceptions, the API returns a generic message without exposing internal exception text.

Audit records store the exception type, not the exception message or submitted text.

Downstream failures are currently recorded using the existing `event: detector_failure` event name, but are distinguished by `reason: analysis_pipeline_error`.

### Running the Regression Tests

No Flask server is required for these tests. They use Flask's in-process test client and mocked model behavior.

Run:

```cmd
python -m unittest test_capstone.py -v
```

The seven tests verify:

1. Unexpected detector failures return HTTP 503.
2. Internal detector exception messages are not exposed.
3. Detector failures are recorded in the audit log.
4. Existing invalid-text handling returns HTTP 400.
5. Unexpected stylometry failures return HTTP 503.
6. Unexpected scoring failures return HTTP 503.
7. Downstream failures do not expose internal details and are categorized correctly in the audit log.

**Observed final result:**

```text
Ran 7 tests in 0.060s

OK
```

All seven regression tests passed.

Save reproducible test output using:

```cmd
python -m unittest test_capstone.py -v > results\capstone_regression_after.txt 2>&1
```

The `results/capstone_regression_before.txt` file captures the pre-improvement regression test run.

The final `after` file captures the passing regression test run.

The initial regression failures and subsequent audit-reason mismatch are part of the diagnosis history.

### Running the Formal Acceptance-Criteria Evaluation

The original CodePath `run_eval.py` and `scenarios.py` remain available for the earlier Project 4 evaluation.

The capstone uses a separate evaluation runner, `run_capstone_eval.py`, to test the five capstone acceptance criteria.

Run:

```cmd
python run_capstone_eval.py --label before
python run_capstone_eval.py --label after
```

These are separate evaluation runs.

Each evaluation executes three trials for each of the five acceptance criteria, totaling **51 test cases per run**.

The runner uses simulated detector exceptions and Flask's test client.

It does not require a running Flask server or a downloaded model.

The evaluation also isolates formal test logs in temporary files rather than clearing existing application audit logs.

#### Capstone Acceptance Criteria

| Criterion | Target Per Trial | Baseline | Final |
|---|---|---|---|
| Controlled detector failure responses | 3/3 HTTP 503 with `detector_unavailable` | MET | MET |
| Internal exception privacy | 0/3 expose internal details | MET | MET |
| Detector failure audit logging | 3/3 complete audit records | MET | MET |
| Existing input validation | 5/5 invalid requests rejected without detector invocation | MET | MET |
| Structured request logging | 3/3 complete request records | MET | MET |

**Observed evaluation results:**

- Baseline: 5/5 criteria MET.
- Final: 5/5 criteria MET.
- Baseline: 51/51 test cases passed.
- Final: 51/51 test cases passed.
- Three trials were completed for every criterion.

The five formal criteria specifically evaluate the detector-failure extension.

The seven regression tests separately verify the downstream analysis improvement.

#### Evaluation Evidence

Baseline evaluation:

- `results/capstone_2026-11-17_194340_before.json`
- `results/capstone_2026-11-17_194340_before.md`

Final evaluation:

- `results/capstone_2026-11-17_194903_after.json`
- `results/capstone_2026-11-17_194903_after.md`

Regression evidence:

- `results/capstone_regression_before.txt`
- `results/capstone_regression_after.txt`

The JSON files contain individual test observations.

The Markdown reports provide readable criterion-level verdicts and trial details.

The original baseline evidence should remain unchanged.

### Structured Logs and Request Timing

The capstone maintains two separate logs.

**1. Audit log**

File: `logs/audit.jsonl`

Records:

- Classification decisions
- Appeals
- Rejected requests
- Detector failures
- Downstream analysis failures

**2. Request log**

File: `logs/requests.jsonl`

Each request record includes:

- `timestamp`
- `request_id`
- `endpoint`
- `method`
- `status_code`
- `duration_ms`
- `error_category`

The HTTP response also includes an `X-Request-ID` header, allowing responses to be correlated with their corresponding request log records.

Request duration is measured using Python's `time.perf_counter()` and recorded in milliseconds.

This measures local request-processing elapsed time, not CPU utilization, end-to-end network latency, or monetary cost.

The request-level logging system does not store submitted text or request bodies.

### Milestone 6 — Diagnosis and Improvement

#### Baseline Observation

All five formal detector-failure acceptance criteria were MET during the baseline evaluation.

However, these criteria did not evaluate unexpected failures in stylometry or scoring.

Additional regression tests identified a weakness: unexpected exceptions in downstream analysis components could escape without controlled error handling, producing HTTP 500 responses.

#### Improvement Implemented

A separate exception handler was added around the downstream analysis pipeline in `app.py`.

The handler protects:

- `stylometry.style_signal()`
- `scoring.combine_signals()`
- `scoring.score_to_label()`
- Confidence calculation

Unexpected downstream exceptions now return:

```json
{
  "error": "analysis_unavailable",
  "message": "The analysis service is temporarily unavailable. Please try again later."
}
```

HTTP status: `503 Service Unavailable`

The audit log records the failure using:

- `event: detector_failure`
- `status: failed`
- `reason: analysis_pipeline_error`
- `error_type`: the exception class name

Internal exception messages are not returned to the caller.

The original detector failure handling and input validation remain unchanged.

#### Verification

After implementing the improvement:

- All seven regression tests passed.
- All five formal acceptance criteria remained MET.
- All 51 formal test cases passed.
- No regression was detected in the original capstone criteria.

The results demonstrate that the identified failure paths are handled under the tested conditions.

They do not establish production-wide fault tolerance.

### Cost, Feasibility, and Limitations

#### Hosting Feasibility

The GPT-2 model weights occupy approximately 550 MB on disk, before accounting for PyTorch, Flask, and runtime memory.

The original starter documentation notes that a 512 MB free hosting tier cannot accommodate the complete service.

For this reason, the capstone uses **Path B: Local with Logs** rather than deploying the full application to that constrained hosting environment.

#### Direct Inference Cost

The detector runs locally rather than through a paid hosted inference API.

There is no per-request API charge in this workflow.

However, local computing resources, electricity, and storage still have costs.

#### Performance Limitations

The first real submission may take longer because the model must load into memory.

Execution time depends on the computer running the application.

The formal evaluation uses mocked failures and does not benchmark real model inference or network latency.

#### Remaining Failure Risks

The application now handles unexpected exceptions in the detector, stylometry, and scoring components.

However, failures in other components, including disk-full conditions or exceptions during audit and request logging, are not guaranteed to produce controlled responses.

#### Evaluation Limitations

The regression and formal evaluations use simulated exceptions and Flask's in-process test client.

They do not measure:

- Real production outage frequency
- Concurrent request performance
- Reliability under sustained traffic
- Real-world network latency
- Production deployment behavior

#### Detection Limitations

Text predictability is not proof of authorship.

Plain language, writing style, and deliberate formatting changes may influence the detector or stylometry signals.

False positives remain possible, and classification results should not be treated as definitive proof that text was generated by AI.

### Final Verification Commands

From the repository root, with the virtual environment activated:

```cmd
python test.py
python -m unittest test_capstone.py -v
python run_capstone_eval.py --label after
```

To test the live service separately, start the application in Terminal 1:

```cmd
python app.py
```

Then use `curl.exe` from Terminal 2 to interact with the endpoints.

The final README summary and evidence discussion should be completed after implementation and evaluation are finalized.

