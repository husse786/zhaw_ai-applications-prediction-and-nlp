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
    """Return the canonical town name from the dataset, or None."""
    # TODO
    # 1) handle empty input
    if not user_town or not user_town.strip():
        return None
    # 2) exact lower-case match
    lower = user_town.strip().lower()
    if lower in town_to_row:
        return lower
    # 3) relaxed contains-match over valid_towns
    for name in valid_towns:
        if lower in name.lower() or name.lower() in lower:
            return name.lower()


# TODO 2 (LLM REQUIRED):
# Implement one helper to call your chosen LLM and return JSON text.
# Requirement: raise an error if API key/model is missing instead of using fallback logic.
# Hint: the Week 1 OpenAI example uses `client.responses.create(...)`.
def call_llm_json(system_prompt: str, user_prompt: str) -> str:
    """Call OpenAI and return raw JSON text."""
    if not LLM_API_KEY or not LLM_MODEL:
        raise ValueError("LLM_API_KEY or LLM_MODEL not set.")

    openai_client = OpenAI(api_key=LLM_API_KEY)

    response = openai_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content


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
    """Extract rooms, area_m2, and town from free text."""

    system_prompt = """Du bist ein spezialisierter Assistent für Schweizer Wohnungssuche.

Deine Aufgabe: Extrahiere aus dem Benutzertext genau drei Informationen:
1. rooms – Anzahl Zimmer als Zahl (z.B. 3.5)
2. area_m2 – Wohnfläche in Quadratmetern als Zahl (z.B. 85)
3. town – Name der Schweizer Gemeinde als String (z.B. "Winterthur")

Regeln:
- Antworte ausschliesslich mit validem JSON, kein zusätzlicher Text.
- Verwende exakt diese drei Keys: rooms, area_m2, town
- rooms und area_m2 müssen numerische Werte sein, keine Strings.
- town muss ein Schweizer Ortsname sein, korrekt geschrieben.
- Falls eine Information im Text fehlt, setze den Wert auf null.

Beispiel-Input: "Ich suche eine 3.5-Zimmer-Wohnung mit etwa 85 m2 in Winterthur."
Beispiel-Output: {"rooms": 3.5, "area_m2": 85, "town": "Winterthur"}"""

    raw = call_llm_json(system_prompt, user_text)
    parsed = parse_json_response(raw, ("rooms", "area_m2", "town"))

    matched = match_town(parsed["town"])
    if matched is None:
        raise ValueError(f"Town not found in dataset: {parsed['town']}")
    parsed["town"] = matched

    return parsed


# TODO 4:
# Implement numeric model prediction with exactly these features:
# [rooms, area_m2, pop, pop_dens, frg_pct, emp, tax_income]
# The provided model is a pickled scikit-learn regressor loaded above.
def predict_apartment_price(rooms: float, area_m2: float, town: str) -> float:
    """Predict monthly rent using the loaded random forest model."""

    matched = match_town(town)
    if matched is None:
        raise ValueError(f"Town not found in dataset: {town}")

    row = town_to_row[matched]

    features = np.array([[
        rooms,
        area_m2,
        row["pop"],
        row["pop_dens"],
        row["frg_pct"],
        row["emp"],
        row["tax_income"]
    ]])

    prediction = model.predict(features)[0]
    return round(prediction, 2)
# TODO 5 (LLM REQUIRED):
# Use your LLM to generate a concise explanation with one uncertainty note.
def generate_explanation(preferences: dict, prediction: float) -> str:
    """Generate a user-friendly German explanation of the prediction."""

    system_prompt = """Du bist ein hilfreicher Wohnungsberater in der Schweiz.

Deine Aufgabe: Erkläre dem Benutzer die Mietpreis-Schätzung in einfachem Deutsch.

Regeln:
- Du bekommst die Wohnungswünsche und eine bereits berechnete Schätzung in CHF.
- Erkläre das Ergebnis in 2-3 Sätzen auf Deutsch.
- Erfinde keinen neuen Preis – verwende ausschliesslich den übergebenen Wert.
- Erwähne eine Unsicherheit oder Limitation des Modells (z.B. Zustand, Lage, Ausstattung fehlen).
- Antworte ausschliesslich mit validem JSON mit dem Key: answer

Beispiel-Output:
{"answer": "Für eine 3.5-Zimmer-Wohnung in Winterthur schätzt das Modell rund 2100 CHF pro Monat. Die Schätzung basiert auf Wohnfläche und Gemeindemerkmalen. Eine Unsicherheit ist, dass Zustand, Mikrolage und Ausstattung nicht im Modell enthalten sind."}"""

    user_prompt = (
        f"Wohnungswünsche: {json.dumps(preferences, ensure_ascii=False)}\n"
        f"Geschätzte Monatsmiete: {prediction} CHF"
    )

    raw = call_llm_json(system_prompt, user_prompt)
    parsed = parse_json_response(raw, ("answer",))

    return parsed["answer"]

# TODO 6:
# Implement the end-to-end pipeline.
def run_pipeline(user_text: str):
    # Return: (preferences_dict, prediction_float, final_answer_text)
    # Add friendly error handling for invalid input and API errors.
    """End-to-end pipeline: extract → predict → explain."""
    try:
        preferences = extract_preferences(user_text)
        prediction = predict_apartment_price(
            preferences["rooms"],
            preferences["area_m2"],
            preferences["town"]
        )
        explanation = generate_explanation(preferences, prediction)

        return preferences, prediction, explanation

    except Exception as e:
        return {"error": str(e)}, 0, f"Fehler: {str(e)}"


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
