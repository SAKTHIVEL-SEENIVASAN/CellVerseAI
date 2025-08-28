from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import json

app = Flask(__name__)

# --- Tab 1: Recipe Generator (Fake NLP) ---
# We'll just use a dictionary to fake an AI model
recipe_database = {
    "neuron": ["Day 0: Plate neural progenitor cells on poly-ornithine coated plates.",
               "Day 1: Add BDNF (50ng/ml) and ascorbic acid (200uM) to medium.",
               "Day 3: Replace 50% of medium with fresh differentiation cocktail.",
               "Day 7: Cells should express MAP2 and beta-tubulin III. Passage if necessary."],
    "heart cell": ["Day 0: Start with iPSCs at 80% confluency.",
                   "Day 1: Add Activin A (100ng/ml) for primitive streak induction.",
                   "Day 3: Switch to BMP4 (50ng/ml) and FGF2 (20ng/ml) for cardiac mesoderm specification.",
                   "Day 5: Begin serum-free differentiation. Monitor for spontaneous beating.",
                   "Day 10: >30% of cells should be cTnT positive."],
    "retinal cell": ["Day 0: Aggregate pluripotent stem cells into embryoid bodies.",
                     "Day 3: Add BMP4 (10ng/ml) and suppress FGF signaling.",
                     "Day 6: Plate aggregates on Matrigel. Add Retinoic Acid (1uM).",
                     "Day 12: Isolate RX+/PAX6+ retinal progenitor cells.",
                     "Day 20: Mature cells should express Rhodopsin and Recoverin."]
}

@app.route('/get_recipe', methods=['POST'])
def get_recipe():
    cell_type = request.json.get('cell_type', '').lower()
    recipe = recipe_database.get(cell_type, ["Protocol not found in database. Try 'neuron', 'heart cell', or 'retinal cell'."])
    return jsonify({"recipe": recipe})

# --- Tab 2: Aging Clock (Fake Model) ---
# Let's create a FAKE "model" that predicts age based on random numbers
# In a real hack, you'd train this on data. Here we just make a rule.
def predict_age(features):
    # Let's pretend the first feature is a key aging marker
    # Simple logic: if sum of features is high, cell is old.
    total = sum(features)
    if total < 150:
        return "Young", 25
    elif 150 <= total <= 300:
        return "Mid", 45
    else:
        return "Old", 70

@app.route('/predict_age', methods=['POST'])
def predict_age_route():
    # Get data from the uploaded CSV or form
    data = request.json
    # We expect a list of 5 numbers for our demo
    features = data.get('features', [])
    # Our "AI" prediction
    age_label, age_value = predict_age(features)
    return jsonify({
        "age_label": age_label,
        "age_value": age_value,
        "features_received": features # Just for demo display
    })

# --- Tab 3: Donor Match Predictor (String Similarity) ---
def calculate_similarity(donor_dna, patient_dna):
    # A simple similarity score based on longest common substring
    # This is a placeholder for a real HLA matching algorithm
    max_match = 0
    for i in range(len(donor_dna)):
        for j in range(len(patient_dna)):
            match = 0
            k = 0
            while (i + k < len(donor_dna) and j + k < len(patient_dna) and donor_dna[i + k] == patient_dna[j + k]):
                match += 1
                k += 1
            if match > max_match:
                max_match = match
    # Calculate a percentage score
    max_possible = max(len(donor_dna), len(patient_dna))
    score = (max_match / max_possible) * 100
    return round(score, 2)

@app.route('/check_match', methods=['POST'])
def check_match():
    donor_dna = request.json.get('donor_dna', 'ATCG')
    patient_dna = request.json.get('patient_dna', 'ATCG')
    score = calculate_similarity(donor_dna, patient_dna)
    return jsonify({"match_score": score})

# --- Main Route ---
@app.route('/')
def index():
    return render_template('index.html') # This will serve your HTML page

if __name__ == '__main__':
    app.run(debug=True)