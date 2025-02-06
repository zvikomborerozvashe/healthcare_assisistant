from flask import Flask, request, jsonify

app = Flask(__name__)

# Extended list of doctor recommendations based on diseases
doctor_recommendations = {
    "Flu": {"doctor": "Dr. John Smith", "specialty": "General Physician"},
    "Migraine": {"doctor": "Dr. Alice Brown", "specialty": "Neurologist"},
    "Cold": {"doctor": "Dr. Emily White", "specialty": "General Physician"},
    "Heart Disease": {"doctor": "Dr. Michael Davis", "specialty": "Cardiologist"},
    "Kidney Disease": {"doctor": "Dr. Sarah Lee", "specialty": "Nephrologist"},
    "Hypertension": {"doctor": "Dr. Robert Clark", "specialty": "Cardiologist"},
    "Diabetes": {"doctor": "Dr. Emma Wilson", "specialty": "Endocrinologist"},
    "Asthma": {"doctor": "Dr. Lily Taylor", "specialty": "Pulmonologist"},
    "Pneumonia": {"doctor": "Dr. James Anderson", "specialty": "Pulmonologist"},
    "Anemia": {"doctor": "Dr. Olivia Martinez", "specialty": "Hematologist"},
    "Cancer": {"doctor": "Dr. William Thomas", "specialty": "Oncologist"},
    "Chronic Obstructive Pulmonary Disease (COPD)": {"doctor": "Dr. George Harris", "specialty": "Pulmonologist"},
    "Gastritis": {"doctor": "Dr. Rachel Scott", "specialty": "Gastroenterologist"},
    "Peptic Ulcer": {"doctor": "Dr. Linda King", "specialty": "Gastroenterologist"},
    "Liver Disease": {"doctor": "Dr. Paul Lewis", "specialty": "Gastroenterologist"},
    "Kidney Stones": {"doctor": "Dr. Nora Adams", "specialty": "Urologist"},
    "Osteoporosis": {"doctor": "Dr. Henry Walker", "specialty": "Orthopedic Specialist"},
    "Rheumatoid Arthritis": {"doctor": "Dr. David Carter", "specialty": "Rheumatologist"},
    "Depression": {"doctor": "Dr. Maria Rodriguez", "specialty": "Psychiatrist"},
    "Anxiety Disorder": {"doctor": "Dr. Susan Hall", "specialty": "Psychiatrist"},
    "Parkinson's Disease": {"doctor": "Dr. Thomas Garcia", "specialty": "Neurologist"},
    "Alzheimer's Disease": {"doctor": "Dr. Patricia Lewis", "specialty": "Neurologist"},
    "Stroke": {"doctor": "Dr. Kenneth Young", "specialty": "Neurologist"},
    "Epilepsy": {"doctor": "Dr. Brian Nelson", "specialty": "Neurologist"},
    "HIV/AIDS": {"doctor": "Dr. Sophia King", "specialty": "Infectious Disease Specialist"},
    "Tuberculosis": {"doctor": "Dr. Daniel White", "specialty": "Infectious Disease Specialist"},
    "Malaria": {"doctor": "Dr. Grace Walker", "specialty": "Infectious Disease Specialist"},
    "Dengue Fever": {"doctor": "Dr. Andrew Scott", "specialty": "Infectious Disease Specialist"},
    "Eczema": {"doctor": "Dr. Amanda Turner", "specialty": "Dermatologist"},
    "Psoriasis": {"doctor": "Dr. Nathan Perez", "specialty": "Dermatologist"},
    "Acne": {"doctor": "Dr. Sophia Miller", "specialty": "Dermatologist"},
    "Allergic Reactions": {"doctor": "Dr. Eric Robinson", "specialty": "Allergist"},
    "Urinary Tract Infection (UTI)": {"doctor": "Dr. Lauren Harris", "specialty": "Urologist"},
    "Chronic Fatigue Syndrome": {"doctor": "Dr. Olivia Mitchell", "specialty": "Rheumatologist"},
    "Gallbladder Disease": {"doctor": "Dr. Charles Walker", "specialty": "Gastroenterologist"},
    "Appendicitis": {"doctor": "Dr. William Hall", "specialty": "General Surgeon"},
    "Celiac Disease": {"doctor": "Dr. Samuel Green", "specialty": "Gastroenterologist"},
    "Crohn's Disease": {"doctor": "Dr. Kimberly Adams", "specialty": "Gastroenterologist"},
    "Irritable Bowel Syndrome (IBS)": {"doctor": "Dr. Jonathan Clark", "specialty": "Gastroenterologist"},
    "Gallstones": {"doctor": "Dr. Anna Turner", "specialty": "Gastroenterologist"},
    "Sickle Cell Anemia": {"doctor": "Dr. James Mitchell", "specialty": "Hematologist"},
    "Cystic Fibrosis": {"doctor": "Dr. Evelyn Brown", "specialty": "Pulmonologist"},
    "Tuberculosis": {"doctor": "Dr. Michael Harris", "specialty": "Infectious Disease Specialist"},
    "Hepatitis": {"doctor": "Dr. Amy Lewis", "specialty": "Gastroenterologist"},
    "Chronic Kidney Disease": {"doctor": "Dr. Steven Perez", "specialty": "Nephrologist"},
    "Multiple Sclerosis": {"doctor": "Dr. Richard Carter", "specialty": "Neurologist"},
    "Lung Cancer": {"doctor": "Dr. Kevin Young", "specialty": "Oncologist"},
    "Skin Cancer": {"doctor": "Dr. Margaret Walker", "specialty": "Dermatologist"}
}


# Mapping of symptoms to diseases
symptoms_disease_map = {
    "chest pain": "Heart Disease",
    "headache": "Migraine",
    "fever": "Flu",
    "cough": "Cold",
    "fatigue": "Chronic Fatigue Syndrome",
    "painful urination": "Urinary Tract Infection (UTI)",
    "shortness of breath": "Asthma",
    "nausea": "Gastritis",
    "dizziness": "Vertigo",
    "joint pain": "Arthritis",
    "sore throat": "Strep Throat",
    "rash": "Skin Infection",
    "weight loss": "Thyroid Disorders",
    "sweating": "Hyperthyroidism",
    "swelling": "Edema",
    "frequent urination": "Diabetes",
    "blood in urine": "Kidney Stones",
    "memory loss": "Alzheimer's Disease",
    "persistent cough": "Chronic Obstructive Pulmonary Disease (COPD)",
    "yellowing of skin": "Jaundice",
    "dark urine": "Hepatitis",
    "diarrhea": "Gastroenteritis",
    "constipation": "Irritable Bowel Syndrome (IBS)",
    "abdominal pain": "Peptic Ulcer",
    "loss of appetite": "Cancer",
    "night sweats": "Tuberculosis",
    "cold extremities": "Raynaud's Disease",
    "bloody stools": "Hemorrhoids",
    "frequent headaches": "Tension Headaches",
    "numbness in limbs": "Multiple Sclerosis",
    "muscle weakness": "Muscular Dystrophy",
    "itchy skin": "Eczema",
    "blurred vision": "Glaucoma",
    "chronic pain": "Fibromyalgia",
    "back pain": "Herniated Disc",
    "ringing in ears": "Tinnitus",
    "vision loss": "Cataracts",
    "difficulty swallowing": "Dysphagia",
    "vomiting": "Food Poisoning",
    "painful joints": "Rheumatoid Arthritis",
    "shivering": "Hypothermia",
    "difficulty breathing": "Pneumonia",
    "swollen lymph nodes": "Lymphoma",
    "persistent sore throat": "Mononucleosis",
    "hiccups": "Gastric Reflux Disease (GERD)",
    "chronic thirst": "Diabetes Insipidus",
    "dry skin": "Hypothyroidism",
    "pale skin": "Anemia",
    "feeling faint": "Low Blood Pressure",
    "high blood pressure": "Hypertension",
    "red eyes": "Conjunctivitis",
    "loss of balance": "Meniere’s Disease",
    "coughing up blood": "Lung Cancer",
    "nausea and vomiting after eating": "Gastroesophageal Reflux Disease (GERD)",
    "dehydration": "Heatstroke",
    "constantly feeling cold": "Hypothyroidism",
    "increased heart rate": "Arrhythmia",
    "extreme hunger": "Hyperglycemia",
    "painful bowel movements": "Anal Fissures",
    "sensitivity to light": "Migraine",
    "feeling anxious": "Anxiety Disorder",
    "low energy": "Vitamin D Deficiency",
    "severe headache": "Cluster Headache",
    "wheezing": "Bronchitis",
    "bloody cough": "Tuberculosis",
    "frequent infections": "Immunodeficiency Disorders",
    "yellow nails": "Fungal Infection",
    "unexplained bruising": "Vitamin C Deficiency",
    "hearing loss": "Sensorineural Hearing Loss",
    "excessive thirst": "Diabetes Mellitus",
    "painful breathing": "Pleuritis",
    "difficult urination": "Benign Prostatic Hyperplasia",
    "sore gums": "Gingivitis",
    "shortness of breath when lying down": "Congestive Heart Failure",
    "skin peeling": "Psoriasis",
    "difficulty concentrating": "Attention Deficit Hyperactivity Disorder (ADHD)",
    "muscle cramps": "Electrolyte Imbalance",
    "chronic cough and mucus production": "Chronic Bronchitis",
    "frequent dizziness": "Low Blood Sugar (Hypoglycemia)",
    "increased body temperature": "Infection",
    "abnormal bruising": "Leukemia",
    "hiccups after eating": "Gastroesophageal Reflux Disease (GERD)"
}



def predict_condition_and_recommend_doctor(symptom):
    """
    Predicts the condition based on the symptom and recommends a doctor.
    """
    # Normalize the symptom input
    symptom = symptom.lower().strip()

    # Predict the condition
    predicted_condition = symptoms_disease_map.get(symptom, "Unknown Condition")

    # Get the doctor recommendation
    doctor_info = doctor_recommendations.get(predicted_condition, {"doctor": "General Physician", "specialty": "General Medicine"})

    return predicted_condition, doctor_info



@app.route('/doctor_recommendation', methods=['POST'])
def doctor_recommendation():
    """
    Flask route to handle doctor recommendations based on symptoms.
    """
    data = request.get_json()
    symptom = data.get('symptom', '')

    if not symptom:
        return jsonify({"error": "Symptom not provided"}), 400

    # Predict the condition and recommend a doctor
    predicted_condition, doctor_info = predict_condition_and_recommend_doctor(symptom)

    # Prepare the response
    response = {
        "predicted_condition": predicted_condition,
        "doctor": doctor_info["doctor"],
        "specialty": doctor_info["specialty"]
    }

    return jsonify(response)


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_id = data.get('user_id')  # Unique ID to track user session
    user_input = data.get('message', '').strip().lower()

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    if user_id not in user_sessions:
        user_sessions[user_id] = {"state": "ask_symptom"}

    session = user_sessions[user_id]

    if session["state"] == "ask_symptom":
        session["state"] = "symptom_received"
        session["symptom"] = user_input
        return jsonify({"response": f"I see. You mentioned '{user_input}'. Can you describe any other symptoms?"})

    elif session["state"] == "symptom_received":
        condition, doctor = predict_condition_and_recommend_doctor(session["symptom"])
        session["state"] = "done"

        return jsonify({
            "response": f"Based on your symptoms, you might have {condition}. I recommend visiting {doctor['doctor']}, a {doctor['specialty']}."
        })

    return jsonify({"response": "I didn't understand. Can you please describe your symptoms?"})



if __name__ == '__main__':
    app.run(debug=True)