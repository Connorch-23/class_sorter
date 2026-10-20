---
name: Project overview
alwaysApply: true
---

# Class Sorter — repo overview

This repo assigns summer-camp campers to classes (4 slots: A-D) by ranked
preference. It contains TWO independent implementations of the same problem:

- `java_logic/` — legacy Java/JavaFX app. **Read-only reference. Never modify.**
  - `java_logic/main/java/org/class_sorter/{model,controller,view}/`
  - `java_logic/test/java/org/class_sorter/AppTest.java`
- `src/class_sorter/` — the Python CLI being built.
  - `models/`, `services/`, `main.py`
- `tests/` — pytest tests for the Python code.
- `inputs/` — input CSVs (e.g. `inputs/classes_input.csv`).

## How to answer questions

- The status notes in these rules can go stale as the Python code is written.
  **Before answering anything about current implementation status, read the
  actual files** under `src/class_sorter/` and `tests/` rather than trusting
  the notes.
- For questions that span the codebase, first list the directory tree, then
  read the relevant files in full before giving an answer. Name the files you
  relied on.
- If something is not in the files you read, say so instead of guessing.
- When proposing a design, give the decision, the reasoning, and which files
  it touches. Do not write code unless asked.
- The Java and Python implementations are deliberately independent. Do not
  suggest mirroring Java names, indexing, or return-code conventions in Python.