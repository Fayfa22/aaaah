
# Disease patterns derived from user provided template
DISEASE_PATTERNS = {
    'Fungal infection': ['itching', 'skin_rash', 'nodal_skin_eruptions'],
    'Allergy': ['continuous_sneezing', 'shivering', 'chills'],
    'GERD': ['stomach_pain', 'acidity', 'ulcers_on_tongue', 'vomiting', 'cough'],
    'Chronic cholestasis': ['itching', 'vomiting', 'yellowish_skin', 'nausea', 'loss_of_appetite', 'abdominal_pain'],
    'Drug Reaction': ['skin_rash', 'stomach_pain', 'burning_micturition', 'spotting_ urination'],
    'Peptic ulcer diseae': ['vomiting', 'dehydration', 'indigestion', 'abdominal_pain', 'passage_of_gases'],
    'AIDS': ['ulcers_on_tongue', 'patches_in_throat', 'high_fever', 'extra_marital_contacts'],
    'Diabetes ': ['fatigue', 'weight_loss', 'restlessness', 'lethargy', 'irregular_sugar_level', 'polyuria', 'family_history'],
    'Gastroenteritis': ['vomiting', 'sunken_eyes', 'dehydration', 'diarrhoea'],
    'Bronchial Asthma': ['fatigue', 'cough', 'high_fever', 'breathlessness', 'mucoid_sputum', 'rusty_sputum'],
    'Hypertension ': ['indigestion', 'chest_pain', 'fast_heart_rate', 'palpitations'],
    'Migraine': ['acidity', 'indigestion', 'headache', 'blurred_and_distorted_vision', 'depression', 'irritability'],
    'Cervical spondylosis': ['back_pain', 'neck_pain', 'dizziness', 'loss_of_balance'],
    'Paralysis (brain hemorrhage)': ['vomiting', 'headache', 'weakness_of_one_body_side'],
    'Jaundice': ['itching', 'vomiting', 'fatigue', 'high_fever', 'yellowish_skin', 'dark_urine', 'weight_loss', 'abdominal_pain'],
    'Malaria': ['chills', 'vomiting', 'high_fever', 'headache', 'nausea', 'sweating'],
    'Chicken pox': ['skin_rash', 'fatigue', 'lethargy', 'high_fever', 'headache', 'mild_fever', 'swelled_lymph_nodes', 'malaise', 'redness_of_eyes'],
    'Dengue': ['skin_rash', 'chills', 'fatigue', 'high_fever', 'headache', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'malaise', 'redness_of_eyes'],
    'Typhoid': ['chills', 'vomiting', 'fatigue', 'high_fever', 'headache', 'nausea', 'abdominal_pain', 'diarrhoea'],
    'hepatitis A': ['chills', 'vomiting', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellowing_of_eyes'],
    'Hepatitis B': ['itching', 'fatigue', 'lethargy', 'yellowish_skin', 'dark_urine', 'loss_of_appetite', 'abdominal_pain', 'yellow_urine', 'yellowing_of_eyes', 'receiving_blood_transfusion', 'receiving_unsterile_injections'],
    'Hepatitis C': ['fatigue', 'yellowish_skin', 'nausea', 'loss_of_appetite', 'yellowing_of_eyes', 'receiving_unsterile_injections'],
    'Hepatitis D': ['chills', 'vomiting', 'fatigue', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'abdominal_pain', 'yellowing_of_eyes'],
    'Hepatitis E': ['chills', 'vomiting', 'fatigue', 'high_fever', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'abdominal_pain', 'yellowing_of_eyes', 'receiving_blood_transfusion'],
    'Alcoholic hepatitis': ['vomiting', 'yellowish_skin', 'swelling_of_stomach', 'history_of_alcohol_consumption', 'fluid_overload'],
    'Tuberculosis': ['chills', 'vomiting', 'fatigue', 'weight_loss', 'cough', 'high_fever', 'breathlessness', 'sweating', 'mucoid_sputum', 'rusty_sputum', 'blood_in_sputum'],
    'Common Cold': ['continuous_sneezing', 'chills', 'fatigue', 'cough', 'high_fever', 'headache', 'runny_nose', 'congestion', 'sinus_pressure', 'throat_irritation', 'mucoid_sputum'],
    'Pneumonia': ['chills', 'fatigue', 'cough', 'high_fever', 'breathlessness', 'sweating', 'mucoid_sputum', 'rusty_sputum', 'blood_in_sputum'],
    'Dimorphic hemmorhoids(piles)': ['constipation', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus'],
    'Heart attack': ['vomiting', 'chest_pain', 'sweating'],
    'Varicose veins': ['fatigue', 'swollen_legs', 'swollen_blood_vessels', 'painful_walking'],
    'Hypothyroidism': ['fatigue', 'weight_gain', 'cold_hands_and_feets', 'mood_swings', 'lethargy', 'dizziness', 'obesity', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'depression', 'irritability'],
    'Hyperthyroidism': ['fatigue', 'mood_swings', 'sweating', 'dizziness', 'excessive_hunger', 'increased_appetite', 'irritability'],
    'Hypoglycemia': ['vomiting', 'fatigue', 'sweating', 'headache', 'dizziness', 'excessive_hunger', 'increased_appetite', 'irregular_sugar_level'],
    'Osteoarthristis': ['chills', 'joint_pain', 'knee_pain', 'hip_joint_pain'],
    'Arthritis': ['swelling_joints', 'movement_stiffness', 'painful_walking'],
    '(vertigo) Paroymsal  Positional Vertigo': ['vomiting', 'headache', 'dizziness', 'spinning_movements', 'loss_of_balance', 'unsteadiness'],
    'Acne': ['skin_rash', 'pus_filled_pimples', 'blackheads'],
    'Urinary tract infection': ['burning_micturition', 'bladder_discomfort', 'foul_smell_of urine'],
    'Psoriasis': ['skin_rash', 'joint_pain', 'skin_peeling'],
    'Impetigo': ['skin_rash', 'high_fever', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']
}

def predict_disease(symptoms_list):
    """
    Predict disease based on list of symptoms.
    Returns a list of dictionaries: [{'disease': name, 'probability': score, 'matched_symptoms': []}, ...]
    """
    if not symptoms_list:
        return []
    
    predictions = []
    
    for disease, pattern in DISEASE_PATTERNS.items():
        matched = [s for s in pattern if s in symptoms_list]
        match_count = len(matched)
        pattern_length = len(pattern)
        
        if match_count > 0:
            # Base probability
            base_prob = (match_count / pattern_length) * 100
            
            # Adjustment factor (penalize if too many symptoms selected that are not in pattern)
            # This is a simple heuristic to mimic the user's JS logic
            adjustment = min(1, pattern_length / (len(symptoms_list) + 1))
            final_prob = min(95, base_prob * (1 + adjustment * 0.2))
            
            predictions.append({
                'disease': disease,
                'probability': round(final_prob),
                'matched_symptoms': matched,
                'total_pattern_symptoms': pattern_length
            })
            
    # Sort by probability desc
    predictions.sort(key=lambda x: x['probability'], reverse=True)
    return predictions[:5]
