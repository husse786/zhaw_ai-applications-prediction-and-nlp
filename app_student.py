import json
import os

import pickle

import gradio as gr
import numpy as np
import pandas as pd
from openai import OpenAI

MODEL_PATH = "random_forest_regression.pkl"

# Students may choose any LLM provider. Store credentials in env vars.
# Example names (choose your own):
# - OPENAI_API_KEY
# - ANTHROPIC_API_KEY
# - GOOGLE_API_KEY
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "")

with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)

df_bfs_data = pd.read_csv("bfs_municipality_and_tax_data.csv", sep=",", encoding="utf-8")
df_bfs_data["tax_income"] = (
    df_bfs_data["tax_income"].astype(str).str.replace("'", "", regex=False).astype(float)
)

town_to_row = {
    str(row["bfs_name"]).lower(): row
    for _, row in df_bfs_data.iterrows()
}
valid_towns = list(df_bfs_data["bfs_name"].sort_values().unique())


# TODO 1:
# Implement town matching from user text to canonical bfs_name.
def match_town(user_town: str):
    # Hints:
    # - return None on empty input
    # - try exact lower-case match first
    # - then relaxed contains matching over valid_towns
    raise NotImplementedError


# TODO 2 (LLM REQUIRED):
# Implement one helper to call your chosen LLM and return JSON text.
# Requirement: raise an error if API key/model is missing instead of using fallback logic.
# Hint: the Week 1 OpenAI example uses `client.responses.create(...)`.
def call_llm_json(system_prompt: str, user_prompt: str) -> str:
    raise NotImplementedError


# Validate the LLM response before the rest of the app depends on it.
# Why this helps:
# - LLMs sometimes return empty text, Markdown, or incomplete JSON.
# - Early validation makes the app more stable and easier to debug.
# - This is a strong general design habit: check external input before using it.
def parse_json_response(raw: str, required_keys: tuple[str, ...]) -> dict:
    cleaned = (raw or "").strip()

    if not cleaned:
        raise ValueError("LLM returned an empty response instead of JSON.")

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM did not return valid JSON. Received: {cleaned[:300]}"
        ) from exc

    missing_keys = [key for key in required_keys if key not in parsed]
    if missing_keys:
        raise ValueError(
            f"LLM JSON is missing required keys: {', '.join(missing_keys)}."
        )

    return parsed


# TODO 3 (LLM REQUIRED):
# Use your LLM to extract: rooms, area_m2, town from free text.
def extract_preferences(user_text: str) -> dict:
    # Requirement: no regex fallback path. Fail loudly when extraction fails.
    # Tip: validate the JSON response before reading rooms / area_m2 / town.
    raise NotImplementedError


# TODO 4:
# Implement numeric model prediction with exactly these features:
# [rooms, area_m2, pop, pop_dens, frg_pct, emp, tax_income]
# The provided model is a pickled scikit-learn regressor loaded above.
def predict_apartment_price(rooms: float, area_m2: float, town: str) -> float:
    raise NotImplementedError


# TODO 5 (LLM REQUIRED):
# Use your LLM to generate a concise explanation with one uncertainty note.
def generate_explanation(preferences: dict, prediction: float) -> str:
    # Requirement: no template fallback path.
    # Tip: validate the response here too, for example with required_keys=("answer",).
    raise NotImplementedError


# TODO 6:
# Implement the end-to-end pipeline.
def run_pipeline(user_text: str):
    # Return: (preferences_dict, prediction_float, final_answer_text)
    # Add friendly error handling for invalid input and API errors.
    raise NotImplementedError


with gr.Blocks(title="Apartment Wishes -> Prediction") as demo:
    gr.Markdown(
        """
        # Apartment Predictor (Student Template)
        Beschreibe den Wohnungswunsch bitte auf Deutsch.
        Beispiel: "Ich suche eine 3.5-Zimmer-Wohnung mit etwa 85 m2 in Winterthur."
        """
    )

    user_text = gr.Textbox(
        label="Wohnungswunsch",
        lines=4,
        placeholder="Beschreibe Zimmer, Fläche in m2 und Ort auf Deutsch...",
    )
    submit = gr.Button("Schätzen")

    extracted = gr.JSON(label="Extrahierte Eingaben")
    price = gr.Number(label="Geschätzte Monatsmiete (CHF)")
    response = gr.Textbox(label="Antwort", lines=6)

    submit.click(
        fn=run_pipeline,
        inputs=[user_text],
        outputs=[extracted, price, response],
    )

demo.launch()
