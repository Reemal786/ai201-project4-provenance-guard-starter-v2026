# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 15:05
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `d07914a1-5ab9-4cbe-be00-ac17f81734b4` | unsure | 0.236 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `6f096ce9-020e-46ce-a910-aa722ce53f9f` | unsure | 0.043 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `f789cc6c-e4b6-4765-a32d-02294b2b3fc5` | unsure | 0.153 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `9764923b-e71e-4e8d-8230-5f33e9a94002` | unsure | 0.202 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `8a9fbdfc-7e9d-406e-872d-1f80f73914bf` | unsure | 0.261 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `21c35165-d007-4e34-82f4-cad013d05530` | unsure | 0.052 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `b06ed606-cad4-49f9-a005-5241a6aed69e` | unsure | 0.060 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `bc22f970-9c17-4ab0-ab68-fb3d99c3af80` | unsure | 0.285 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `bfd40e20-91ce-4d5c-a2c3-ff293f0892e3` | unsure | 0.187 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `a58d497b-6442-4fb3-a26c-aa6187e6cee8` | ai | 0.723 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `4f0e4dd1-8a4e-4a20-80ea-3a94fba38d33` | unsure | 0.165 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `cc66d7fd-d06b-4624-8d6b-01316553ce52` | ai | 0.366 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `4a030aff-a0ed-4239-94f1-b18b789c73c7` | ai | 0.399 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `458ad37f-acb0-454f-acfe-a33ed3910b67` | ai | 0.373 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `474139df-03d0-4f75-99bc-29842d303484` | ai | 0.437 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `70276c81-f869-4070-8c80-630994fa272a` | ai | 0.397 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `7ef02e50-c2a2-456b-91ba-f0d1425e8924` | ai | 0.396 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `ea6ef38c-30b0-42ac-9a25-ac88d8f18f01` | human | 0.433 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `98f2ef79-04cc-4ed3-b1c5-81c939ea9b88` | unsure | 0.121 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `cc5b0616-203f-43e3-a50a-e5809c980427` | human | 0.414 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `7f114126-b1a2-4a91-80d0-5313dd9ef970` | unsure | 0.115 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `0a18ddef-db8c-4718-98c4-7496ce516a37` | unsure | 0.029 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `412987d8-0504-4b1b-ad5f-d3d1f4a7418f` | unsure | 0.137 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `13964bd3-4de5-4fdc-aa06-0b4692d60f92` | unsure | 0.112 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `2a6d55ad-f837-4902-b3fd-f408cac2cc4d` | human | 0.500 |  |
| MF04 | malformed | text is only punctuation | 200 | `b9ef3259-3b28-47e0-8dcb-00e3020c5d63` | human | 0.489 |  |
| MF05 | malformed | text is a very long single word | 200 | `9b8c5300-0d21-415f-9fe0-64265513347a` | ai | 0.498 |  |
| MF06 | malformed | text is emoji only | 200 | `4e0338ce-1432-4441-b249-ca2c29747f74` | ai | 0.497 |  |
| MF07 | malformed | text is right-to-left script | 200 | `e10bea7f-e265-4b4a-8dee-887e7a7f6588` | ai | 0.406 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5ee650b6-eab5-492b-aad3-064cfdd721b9` | human | 0.532 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1efa4862-49e1-494a-b734-9f9bd9d98619` | human | 0.532 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b91bc17a-f02c-4c90-b890-633376b096d4` | human | 0.532 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1c29cdee-53cc-497d-b2f8-05e4c0df50f2` | human | 0.532 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5d8f6fb9-ffbc-4847-9cd0-80bdbfa3945e` | human | 0.532 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `da5e01a7-bf0c-4e0c-9d39-dbaa1b323e21` | human | 0.532 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `afc683ff-1e9b-49a2-987b-ed0e16dcaa38` | human | 0.532 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `bfc4d7d2-e30f-44d4-9311-991b2f33996b` | human | 0.532 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f2795e6f-7275-40b8-b167-4215f4fb7fb2` | human | 0.532 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ffdabb95-700b-45f6-8a02-40518c5e7a6d` | human | 0.532 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
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
  "content_id": "d07914a1-5ab9-4cbe-be00-ac17f81734b4",
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
  "content_id": "6f096ce9-020e-46ce-a910-aa722ce53f9f",
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
  "content_id": "f789cc6c-e4b6-4765-a32d-02294b2b3fc5",
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
  "content_id": "9764923b-e71e-4e8d-8230-5f33e9a94002",
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
  "content_id": "8a9fbdfc-7e9d-406e-872d-1f80f73914bf",
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
  "content_id": "21c35165-d007-4e34-82f4-cad013d05530",
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
  "content_id": "b06ed606-cad4-49f9-a005-5241a6aed69e",
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
  "content_id": "bc22f970-9c17-4ab0-ab68-fb3d99c3af80",
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
  "content_id": "bfd40e20-91ce-4d5c-a2c3-ff293f0892e3",
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
  "content_id": "a58d497b-6442-4fb3-a26c-aa6187e6cee8",
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
  "content_id": "4f0e4dd1-8a4e-4a20-80ea-3a94fba38d33",
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
  "content_id": "cc66d7fd-d06b-4624-8d6b-01316553ce52",
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
  "content_id": "4a030aff-a0ed-4239-94f1-b18b789c73c7",
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
  "content_id": "458ad37f-acb0-454f-acfe-a33ed3910b67",
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
  "content_id": "474139df-03d0-4f75-99bc-29842d303484",
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
  "content_id": "70276c81-f869-4070-8c80-630994fa272a",
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
  "content_id": "7ef02e50-c2a2-456b-91ba-f0d1425e8924",
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
  "content_id": "ea6ef38c-30b0-42ac-9a25-ac88d8f18f01",
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
  "content_id": "98f2ef79-04cc-4ed3-b1c5-81c939ea9b88",
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
  "content_id": "cc5b0616-203f-43e3-a50a-e5809c980427",
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
  "content_id": "7f114126-b1a2-4a91-80d0-5313dd9ef970",
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
  "content_id": "0a18ddef-db8c-4718-98c4-7496ce516a37",
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
  "content_id": "412987d8-0504-4b1b-ad5f-d3d1f4a7418f",
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
  "content_id": "13964bd3-4de5-4fdc-aa06-0b4692d60f92",
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
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "2a6d55ad-f837-4902-b3fd-f408cac2cc4d",
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
  "content_id": "b9ef3259-3b28-47e0-8dcb-00e3020c5d63",
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
  "content_id": "9b8c5300-0d21-415f-9fe0-64265513347a",
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
  "content_id": "4e0338ce-1432-4441-b249-ca2c29747f74",
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
  "content_id": "e10bea7f-e265-4b4a-8dee-887e7a7f6588",
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
  "content_id": "5ee650b6-eab5-492b-aad3-064cfdd721b9",
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
  "content_id": "1efa4862-49e1-494a-b734-9f9bd9d98619",
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
  "content_id": "b91bc17a-f02c-4c90-b890-633376b096d4",
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
  "content_id": "1c29cdee-53cc-497d-b2f8-05e4c0df50f2",
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
  "content_id": "5d8f6fb9-ffbc-4847-9cd0-80bdbfa3945e",
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
  "content_id": "da5e01a7-bf0c-4e0c-9d39-dbaa1b323e21",
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
  "content_id": "afc683ff-1e9b-49a2-987b-ed0e16dcaa38",
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
  "content_id": "bfc4d7d2-e30f-44d4-9311-991b2f33996b",
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
  "content_id": "f2795e6f-7275-40b8-b167-4215f4fb7fb2",
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
  "content_id": "ffdabb95-700b-45f6-8a02-40518c5e7a6d",
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
