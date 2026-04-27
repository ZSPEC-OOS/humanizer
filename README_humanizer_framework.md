# Humanizer Framework: Local File System

## Purpose

This folder contains a lightweight, editable framework for learning how a specific humanizer transforms AI-generated text into humanized prose.

The method is based on paired examples:

```text
Paste 1 = AI version
Paste 2 = Humanized version
```

The Python file compares the two versions, extracts candidate transformation rules, and updates a reference JSON file.

---

## Files

| File | Purpose |
|---|---|
| `humanizer_framework.py` | Core Python module for analysis, rule extraction, and prompt generation |
| `humanizer_reference.json` | Seeded reference knowledge base containing direct examples and rules |
| `README_humanizer_framework.md` | This usage guide |

---

## Basic Use

```python
from humanizer_framework import add_example, build_humanizer_prompt, diagnostic_report

result = add_example(
    reference_path="humanizer_reference.json",
    example_id="new_example_001",
    domain="Physics",
    ai_text="""PASTE 1 AI TEXT HERE""",
    human_text="""PASTE 2 HUMANIZED TEXT HERE""",
    notes="Optional notes about the transformation."
)

print(diagnostic_report(result))
print(build_humanizer_prompt("humanizer_reference.json"))
```

---

## Input Format

Use this structure when adding new examples:

```text
ANALYZE PAIR

Paste 1: AI
...

Paste 2: Humanized
...

Task:
1. Compare Paste 1 and Paste 2.
2. Identify new humanization rules.
3. Update the framework.
4. Produce revised Humanizer Framework.
```

---

## What the Framework Tracks

The current implementation measures:

1. Word count
2. Sentence count
3. Average sentence length
4. Paragraph count
5. Parenthetical clarifications
6. Definition markers
7. Transition markers
8. Technical vocabulary markers

It then infers candidate rules, such as:

- Break dense AI passages into smaller instructional paragraphs.
- Define technical terms immediately after first use.
- Replace rhetorical polish with direct classroom-style explanation.
- Preserve domain vocabulary but surround it with explanation.
- Add mild redundancy where it improves comprehension.

---

## Seeded Example Pattern

The reference file is seeded with three examples:

1. Quantum Physics
2. Chemistry
3. Biology

These examples show the current humanizer tendencies:

### Observed Humanization Moves

| Move | Description |
|---|---|
| Concept segmentation | One dense AI paragraph becomes multiple teaching paragraphs |
| Parenthetical clarification | Technical or ambiguous terms are explained in parentheses |
| Direct definitions | Concepts are defined immediately after introduction |
| Reduced rhetorical polish | Elegant AI phrasing becomes explicit explanation |
| Preserved vocabulary | Technical words remain, but are explained |
| Instructional transitions | The prose uses explicit guideposts |
| Controlled redundancy | Key ideas are restated for comprehension |

---

## Recommended Revision Process

After each new pair:

1. Run `add_example(...)`.
2. Read the diagnostic report.
3. Inspect candidate rules.
4. Edit `humanizer_reference.json` manually if a rule is too broad or incorrect.
5. Regenerate the prompt with `build_humanizer_prompt(...)`.

This keeps the system transparent and prevents hidden, unexplained changes.

---

## Boundary Conditions

The framework does **not** guarantee scientific correctness. It learns rewrite behavior only.

For technical text, humanization should be checked separately for:

- factual accuracy
- terminology accuracy
- equation integrity
- omitted caveats
- unsupported claims
- excessive simplification
