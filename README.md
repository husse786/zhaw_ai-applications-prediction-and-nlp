---
title: Apartment
emoji: 🏠
colorFrom: red
colorTo: gray
sdk: gradio
sdk_version: 6.13.0
app_file: app.py
pinned: false
---

# Apartment Predictor (Numeric Model + LLM)

This Space demonstrates the Week 2 AI Applications pattern:

- natural language apartment wishes
- structured extraction (`rooms`, `area_m2`, `town`)
- reuse of an existing pickled random forest model
- LLM explanation of the result

Because the data is Swiss, students should write prompts in German so town names like `Zürich` match the dataset more reliably.

## Student workflow

- Build logic in notebook (`ai_applications_exercise2.ipynb`)
- Reuse the provided saved model file `random_forest_regression.pkl`
- Implement TODOs in `app_student.py` (any LLM provider is allowed)
- Promote finished code to `app.py` for deployment
- Deploy the app to Hugging Face Spaces
- Complete `documentation.md`

## What To Submit

Your submission for this exercise should include:

- a working deployed app on Hugging Face Spaces
- your finished code files
- a completed `documentation.md`

In `documentation.md`, document what you built, how your prompts work, how you tested the app, and what happened during deployment.

You must also include **2 screenshots** from your app:

- 2 different example inputs
- visible extracted JSON
- visible prediction
- visible final explanation text

## LLM policy in this exercise

- LLM usage is mandatory.
- No fallback path is allowed for extraction/explanation.
- Errors should stay visible so issues can be debugged.

## Reference solution details

- `app.py` is an OpenAI-based reference implementation.
- It expects `OPENAI_API_KEY` (and optional `OPENAI_MODEL`).

## Required files

- `app.py`
- `app_student.py`
- `requirements.txt`
- `random_forest_regression.pkl`
- `bfs_municipality_and_tax_data.csv`

See `NOTEBOOK_TO_APP.md` for the transfer checklist.
