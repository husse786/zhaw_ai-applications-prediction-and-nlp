# Documentation
## Week 2: Apartment Predictor (Saved Regression Model + LLM Workflow)

Use this file to document what you built, tested, and learned in this exercise.

Do not rename this file to `README.md`, because `README.md` is needed by Hugging Face Spaces.

This file is part of the submission. Complete it after you have tested and deployed your app.

---

## 1. Project Summary

**Short description of your app:**  
_Write 2-4 sentences explaining what the app does._

Example topics:
- What kind of user input does the app accept?
- What does the regression model predict?
- What is the role of the LLM in your app?

---

## 2. Files Used

List the main files you worked with.

| File | Purpose |
|------|---------|
| `ai_applications_exercise2.ipynb` | Notebook work and testing |
| `app_student.py` | Student implementation |
| `app.py` | Final deployable app |
| `random_forest_regression.pkl` | Saved regression model |
| `bfs_municipality_and_tax_data.csv` | Municipality features used for prediction |
| `requirements.txt` | Python dependencies |
| `documentation.md` | Written documentation for the submission |

Add or remove rows if needed.

---

## 3. Numeric Prediction Part

### 3.1 Reused Model

**Which saved model did you use?**  
`random_forest_regression.pkl`

**What does the model predict?**  
_Describe the target in 1-2 sentences._

**Which input features are used for prediction?**  
_List the seven features in the correct order._

Example format:
1. `rooms`
2. `area_m2`
3. `pop`
4. `pop_dens`
5. `frg_pct`
6. `emp`
7. `tax_income`

### 3.2 Prediction Logic

_Explain briefly how you built the model input from user data and municipality data._

---

## 4. LLM Extraction Part

### 4.1 Goal

_Explain what the LLM had to extract from the user text._

### 4.2 Prompt Design

Paste or summarize the prompt idea you used.

Helpful points to mention:
- Did you use a system/developer instruction?
- Did you require strict JSON?
- Which keys did you require?
- Did you tell the model to respond in German?

### 4.3 Expected Output Format

Document the ideal extraction output.

Example:

```json
{"rooms": 3.5, "area_m2": 85, "town": "Winterthur"}
```

### 4.4 Validation

_Explain how you checked that the extracted values were usable in Python._

---

## 5. LLM Explanation Part

### 5.1 Goal

_Explain what the second LLM step should do._

Important:
- The LLM should explain the prediction.
- The LLM should not calculate a new price.

### 5.2 Prompt Design

_Describe how you prompted the LLM to produce the explanation._

Helpful points:
- structured preferences included?
- prediction value included?
- German output required?
- uncertainty note required?
- JSON output required?

### 5.3 Expected Output Format

Example:

```json
{"answer": "Für eine 3.5-Zimmer-Wohnung in Winterthur schätzt das Modell rund 2800 CHF pro Monat. Eine Unsicherheit ist, dass Zustand und Mikrolage nicht direkt im Modell enthalten sind."}
```

---

## 6. End-to-End Pipeline

Describe the full pipeline in your own words.

Suggested order:
1. User enters a German apartment request.
2. LLM extracts `rooms`, `area_m2`, and `town`.
3. Python validates the extracted values.
4. The regression model predicts the monthly rent.
5. The LLM generates a short explanation.
6. The app returns structured input, prediction, and final answer.

---

## 7. Test Cases

Document at least 3 test inputs.

| Test Input | Extracted Output Correct? | Prediction Returned? | Explanation Returned? | Notes |
|------------|----------------------------|----------------------|-----------------------|-------|
| _Example:_ `Ich suche eine 3.5-Zimmer-Wohnung mit 85 m2 in Winterthur.` | Yes / No | Yes / No | Yes / No | _What happened?_ |
|  |  |  |  |  |
|  |  |  |  |  |

Use German test prompts.

---

## 8. Errors and Problems

Describe problems you encountered.

Possible topics:
- invalid town names
- wrong JSON from the LLM
- missing API key
- model file not found
- deployment issues on Hugging Face

For each issue, write:
- **Problem**
- **Cause**
- **Fix**

---

## 9. Deployment Notes

Document your Hugging Face deployment here.

### 9.1 Files included

_List the files that were uploaded._

### 9.2 Secrets / Environment Variables

_List which secret names were required._

Example:
- `OPENAI_API_KEY`
- `OPENAI_MODEL` (optional)

### 9.3 Deployment Result

_Did the Space run successfully? What worked? What failed?_

### 9.4 Screenshots

Add **2 screenshots** from your running app here.

Requirements for the screenshots:
- use 2 different German example prompts
- show the extracted JSON
- show the predicted rent
- show the final explanation

You can insert them like this:

```md
![Example 1](screenshot1.png)
![Example 2](screenshot2.png)
```

Write 1-2 short sentences below each screenshot explaining what happened in the example.

---

## 10. Reflection

Write 3-5 sentences about the exercise.

Possible reflection questions:
- What worked well in the combination of regression model + LLM?
- Where is the system fragile?
- Why is German input important in this exercise?
- What important apartment information is still missing from the model?
- What would you improve next?

---

## 11. Responsible Use Note

Write 2-4 sentences about limitations and responsible use.

Possible topics:
- The prediction is only an estimate.
- The model uses limited structured features.
- The LLM may extract values incorrectly.
- Real rental prices depend on additional factors not included here.
