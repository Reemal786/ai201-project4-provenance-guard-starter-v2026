# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 14:24
- Auto-marked BROKE (5xx, crash, no response): **1**
- Left for you to judge: **55**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `3a24be1c-6749-42c2-b0b7-591f1597e81a` | unsure | 0.236 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `e31232f7-f220-4699-b691-fb832eaecbd8` | unsure | 0.043 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `cd28234e-3f3b-4733-b88f-802926ec02a9` | unsure | 0.153 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `47b71f68-2434-4754-a74f-e78fee14dd4a` | unsure | 0.202 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `d3fde957-4178-4b4e-981f-815294bdcc97` | unsure | 0.261 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `2d1f6bec-09e6-458c-b0b9-e1de68b55c65` | unsure | 0.052 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `adbf7ec4-6969-4042-9eec-733151b57e06` | unsure | 0.060 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `1952d114-5759-4e2f-b42a-28475cf6b3e8` | unsure | 0.285 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `4991f5e8-1dee-47b9-bf16-d5bc5772d96b` | unsure | 0.187 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `f86f3d21-66df-4611-be22-59b51178c1fa` | ai | 0.723 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `34c2f0a0-b2db-4e77-869f-e79cdb0f77ba` | unsure | 0.165 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `7353fc21-7c6b-40da-a0cd-badc9a4364bf` | ai | 0.366 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `715e1d90-0a1b-4737-b3c4-3b3c4994069c` | ai | 0.399 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `52b74889-d13e-465b-aa75-acff16ede12b` | ai | 0.373 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `37da3384-61c6-4884-8760-bfc28d12c697` | ai | 0.437 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `a591d585-19d0-4ede-94df-596892a17d0c` | ai | 0.397 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `d0f2cfd8-09b9-49a1-8753-365fbc53ccdc` | ai | 0.396 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `69000120-7546-4d61-acb3-25000e1f613f` | human | 0.433 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `006e7c1b-f5e7-4487-84f6-1c4ff0f74dec` | unsure | 0.121 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c90e524d-bd96-44d4-838b-38e58a65fe62` | human | 0.414 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `578fe5c3-01fa-4874-9f02-a6fb912ec529` | unsure | 0.115 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `e0c0ba65-a76e-44a2-9aaf-8ea6b6289c22` | unsure | 0.029 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `fbfefaab-5884-4867-bd8c-6296146eb030` | unsure | 0.137 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `4c04f52e-9849-44cd-b7c6-ae23d9adb070` | unsure | 0.112 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `2a670d52-2d99-4edd-9819-e1106d81b2e7` | human | 0.500 |  |
| MF04 | malformed | text is only punctuation | 200 | `b1b7d2a8-86af-40ae-9331-7e58f1e2c819` | human | 0.489 |  |
| MF05 | malformed | text is a very long single word | 200 | `141ec8df-e08c-4d7d-ad92-b254ea16241d` | ai | 0.498 |  |
| MF06 | malformed | text is emoji only | 200 | `44390f3b-f014-4186-a185-5441b34acce4` | ai | 0.497 |  |
| MF07 | malformed | text is right-to-left script | 200 | `7dfc28ff-7cd7-4138-80b4-33c7ee1149b8` | ai | 0.406 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `27e61c16-058c-4458-af3a-63f78db4fbac` | human | 0.532 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9af0195a-3b19-4695-b8a1-b60f5ca9a4cb` | human | 0.532 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `20e4dc9e-fda5-4251-997b-8be27ee11cc4` | human | 0.532 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9fb067ac-fd1a-44b3-b8c4-9adb919390a1` | human | 0.532 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2edf236f-158b-4b57-bc36-e387bcc389a8` | human | 0.532 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `eb38ee90-62f4-47b5-ab71-7de9f4162597` | human | 0.532 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3fe09107-13cf-4155-a36a-58dd9b58f125` | human | 0.532 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a5578097-25bf-4a15-993d-ec2256d2abcd` | human | 0.532 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e7b0ddb0-cb7e-4494-965e-f14618622eb4` | human | 0.532 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9ef9312c-8418-41f4-87a3-a9ca9a235c05` | human | 0.532 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 1 | 19 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "3a24be1c-6749-42c2-b0b7-591f1597e81a",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.2358,
  "model_score": 0.1635,
  "style_score": 0.6006,
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "e31232f7-f220-4699-b691-fb832eaecbd8",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.0434,
  "model_score": 0.5943,
  "style_score": 0.3622,
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "cd28234e-3f3b-4733-b88f-802926ec02a9",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.1526,
  "model_score": 0.6662,
  "style_score": 0.4863,
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "47b71f68-2434-4754-a74f-e78fee14dd4a",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.202,
  "model_score": 0.6114,
  "style_score": 0.5906,
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "d3fde957-4178-4b4e-981f-815294bdcc97",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.2614,
  "model_score": 0.3212,
  "style_score": 0.4175,
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "2d1f6bec-09e6-458c-b0b9-e1de68b55c65",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.0524,
  "model_score": 0.5727,
  "style_score": 0.375,
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "adbf7ec4-6969-4042-9eec-733151b57e06",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.0596,
  "model_score": 0.5862,
  "style_score": 0.4733,
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "1952d114-5759-4e2f-b42a-28475cf6b3e8",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.2852,
  "model_score": 0.2452,
  "style_score": 0.4697,
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "4991f5e8-1dee-47b9-bf16-d5bc5772d96b",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.1874,
  "model_score": 0.7042,
  "style_score": 0.4832,
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "f86f3d21-66df-4611-be22-59b51178c1fa",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.7228,
  "model_score": 0.9792,
  "style_score": 0.7435,
  "label": "This writing shows patterns associated with AI-generated text, but this result is not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "34c2f0a0-b2db-4e77-869f-e79cdb0f77ba",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.1652,
  "model_score": 0.6175,
  "style_score": 0.5476,
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "7353fc21-7c6b-40da-a0cd-badc9a4364bf",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.3658,
  "model_score": 0.7387,
  "style_score": 0.6271,
  "label": "This writing shows patterns associated with AI-generated text, but this result is not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "715e1d90-0a1b-4737-b3c4-3b3c4994069c",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.3992,
  "model_score": 0.8051,
  "style_score": 0.594,
  "label": "This writing shows patterns associated with AI-generated text, but this result is not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "52b74889-d13e-465b-aa75-acff16ede12b",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.3734,
  "model_score": 0.8329,
  "style_score": 0.5405,
  "label": "This writing shows patterns associated with AI-generated text, but this result is not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "37da3384-61c6-4884-8760-bfc28d12c697",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.4366,
  "model_score": 0.8005,
  "style_score": 0.6361,
  "label": "This writing shows patterns associated with AI-generated text, but this result is not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "a591d585-19d0-4ede-94df-596892a17d0c",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.3974,
  "model_score": 0.8814,
  "style_score": 0.5161,
  "label": "This writing shows patterns associated with AI-generated text, but this result is not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "d0f2cfd8-09b9-49a1-8753-365fbc53ccdc",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.3958,
  "model_score": 0.8816,
  "style_score": 0.5142,
  "label": "This writing shows patterns associated with AI-generated text, but this result is not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "69000120-7546-4d61-acb3-25000e1f613f",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.433,
  "model_score": 0.3223,
  "style_score": 0.2447,
  "label": "This writing appears more consistent with human-written text, but we cannot verify its authorship.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "006e7c1b-f5e7-4487-84f6-1c4ff0f74dec",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.1214,
  "model_score": 0.4625,
  "style_score": 0.416,
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "c90e524d-bd96-44d4-838b-38e58a65fe62",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.4142,
  "model_score": 0.2044,
  "style_score": 0.3815,
  "label": "This writing appears more consistent with human-written text, but we cannot verify its authorship.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "578fe5c3-01fa-4874-9f02-a6fb912ec529",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.115,
  "model_score": 0.5943,
  "style_score": 0.5206,
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "e0c0ba65-a76e-44a2-9aaf-8ea6b6289c22",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.029,
  "model_score": 0.4998,
  "style_score": 0.4712,
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "fbfefaab-5884-4867-bd8c-6296146eb030",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.1366,
  "model_score": 0.6401,
  "style_score": 0.2233,
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "4c04f52e-9849-44cd-b7c6-ae23d9adb070",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.1122,
  "model_score": 0.5583,
  "style_score": 0.5539,
  "label": "We cannot confidently determine whether this writing was created by a person or AI. This result is not an accusation.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "2a670d52-2d99-4edd-9819-e1106d81b2e7",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "This writing appears more consistent with human-written text, but we cannot verify its authorship.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "b1b7d2a8-86af-40ae-9331-7e58f1e2c819",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.4888,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "This writing appears more consistent with human-written text, but we cannot verify its authorship.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "141ec8df-e08c-4d7d-ad92-b254ea16241d",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.4976,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "This writing shows patterns associated with AI-generated text, but this result is not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "44390f3b-f014-4186-a185-5441b34acce4",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.497,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "This writing shows patterns associated with AI-generated text, but this result is not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "7dfc28ff-7cd7-4138-80b4-33c7ee1149b8",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.4064,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "This writing shows patterns associated with AI-generated text, but this result is not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "27e61c16-058c-4458-af3a-63f78db4fbac",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.532,
  "model_score": 0.0287,
  "style_score": 0.4393,
  "label": "This writing appears more consistent with human-written text, but we cannot verify its authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "9af0195a-3b19-4695-b8a1-b60f5ca9a4cb",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.532,
  "model_score": 0.0287,
  "style_score": 0.4393,
  "label": "This writing appears more consistent with human-written text, but we cannot verify its authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "20e4dc9e-fda5-4251-997b-8be27ee11cc4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.532,
  "model_score": 0.0287,
  "style_score": 0.4393,
  "label": "This writing appears more consistent with human-written text, but we cannot verify its authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "9fb067ac-fd1a-44b3-b8c4-9adb919390a1",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.532,
  "model_score": 0.0287,
  "style_score": 0.4393,
  "label": "This writing appears more consistent with human-written text, but we cannot verify its authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "2edf236f-158b-4b57-bc36-e387bcc389a8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.532,
  "model_score": 0.0287,
  "style_score": 0.4393,
  "label": "This writing appears more consistent with human-written text, but we cannot verify its authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "eb38ee90-62f4-47b5-ab71-7de9f4162597",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.532,
  "model_score": 0.0287,
  "style_score": 0.4393,
  "label": "This writing appears more consistent with human-written text, but we cannot verify its authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "3fe09107-13cf-4155-a36a-58dd9b58f125",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.532,
  "model_score": 0.0287,
  "style_score": 0.4393,
  "label": "This writing appears more consistent with human-written text, but we cannot verify its authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "a5578097-25bf-4a15-993d-ec2256d2abcd",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.532,
  "model_score": 0.0287,
  "style_score": 0.4393,
  "label": "This writing appears more consistent with human-written text, but we cannot verify its authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "e7b0ddb0-cb7e-4494-965e-f14618622eb4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.532,
  "model_score": 0.0287,
  "style_score": 0.4393,
  "label": "This writing appears more consistent with human-written text, but we cannot verify its authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "9ef9312c-8418-41f4-87a3-a9ca9a235c05",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.532,
  "model_score": 0.0287,
  "style_score": 0.4393,
  "label": "This writing appears more consistent with human-written text, but we cannot verify its authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
