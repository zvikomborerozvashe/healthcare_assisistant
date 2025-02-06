import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, SpatialDropout1D, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import pad_sequences
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle

# Enhanced dataset with more symptoms and conditions
data = [
    {"symptom": "fever", "condition": "Flu"},
    {"symptom": "headache", "condition": "Migraine"},
    {"symptom": "cough", "condition": "Cold"},
    {"symptom": "chest pain", "condition": "Heart Disease"},
    {"symptom": "shortness of breath", "condition": "COVID-19"},
    {"symptom": "loss of taste", "condition": "COVID-19"},
    {"symptom": "loss of smell", "condition": "COVID-19"},
    {"symptom": "sore throat", "condition": "Strep Throat"},
    {"symptom": "nausea", "condition": "Food Poisoning"},
    {"symptom": "vomiting", "condition": "Food Poisoning"},
    {"symptom": "diarrhea", "condition": "Gastroenteritis"},
    {"symptom": "fatigue", "condition": "Chronic Fatigue Syndrome"},
    {"symptom": "muscle pain", "condition": "Fibromyalgia"},
    {"symptom": "joint pain", "condition": "Arthritis"},
    {"symptom": "rash", "condition": "Allergic Reaction"},
    {"symptom": "itchy eyes", "condition": "Allergic Reaction"},
    {"symptom": "swelling", "condition": "Allergic Reaction"},
    {"symptom": "dizziness", "condition": "Vertigo"},
    {"symptom": "blurred vision", "condition": "Migraine"},
    {"symptom": "high blood pressure", "condition": "Hypertension"},
    {"symptom": "low blood pressure", "condition": "Hypotension"},
    {"symptom": "palpitations", "condition": "Arrhythmia"},
    {"symptom": "confusion", "condition": "Alzheimer's Disease"},
    {"symptom": "memory loss", "condition": "Alzheimer's Disease"},
    {"symptom": "weight loss", "condition": "Hyperthyroidism"},
    {"symptom": "weight gain", "condition": "Hypothyroidism"},
    {"symptom": "excessive thirst", "condition": "Diabetes"},
    {"symptom": "frequent urination", "condition": "Diabetes"},
    {"symptom": "abdominal pain", "condition": "Appendicitis"},
    {"symptom": "constipation", "condition": "Irritable Bowel Syndrome"},
    {"symptom": "blood in stool", "condition": "Colorectal Cancer"},
    {"symptom": "unusual bleeding", "condition": "Hemophilia"},
    {"symptom": "bruising", "condition": "Hemophilia"},
    {"symptom": "swollen lymph nodes", "condition": "Lymphoma"},
    {"symptom": "night sweats", "condition": "Lymphoma"},
    {"symptom": "persistent cough", "condition": "Lung Cancer"},
    {"symptom": "hoarseness", "condition": "Laryngeal Cancer"},
    {"symptom": "difficulty swallowing", "condition": "Esophageal Cancer"},
    {"symptom": "unexplained weight loss", "condition": "Cancer"},
    {"symptom": "persistent fatigue", "condition": "Cancer"},
    {"symptom": "lump", "condition": "Cancer"},
    {"symptom": "changes in bowel habits", "condition": "Colorectal Cancer"},
    {"symptom": "changes in bladder habits", "condition": "Bladder Cancer"},
    {"symptom": "unusual discharge", "condition": "Sexually Transmitted Infection"},
    {"symptom": "pain during intercourse", "condition": "Sexually Transmitted Infection"},
    {"symptom": "pelvic pain", "condition": "Endometriosis"},
    {"symptom": "irregular periods", "condition": "Polycystic Ovary Syndrome"},
    {"symptom": "hot flashes", "condition": "Menopause"},
    {"symptom": "mood swings", "condition": "Premenstrual Syndrome"},
    {"symptom": "insomnia", "condition": "Anxiety"},
    {"symptom": "panic attacks", "condition": "Panic Disorder"},
    {"symptom": "hallucinations", "condition": "Schizophrenia"},
    {"symptom": "delusions", "condition": "Schizophrenia"},
    {"symptom": "paranoia", "condition": "Schizophrenia"},
    {"symptom": "obsessive thoughts", "condition": "Obsessive-Compulsive Disorder"},
    {"symptom": "compulsive behaviors", "condition": "Obsessive-Compulsive Disorder"},
    {"symptom": "social withdrawal", "condition": "Depression"},
    {"symptom": "loss of interest", "condition": "Depression"},
    {"symptom": "suicidal thoughts", "condition": "Depression"},
    {"symptom": "excessive worry", "condition": "Generalized Anxiety Disorder"},
    {"symptom": "restlessness", "condition": "Generalized Anxiety Disorder"},
    {"symptom": "irritability", "condition": "Bipolar Disorder"},
    {"symptom": "mania", "condition": "Bipolar Disorder"},
    {"symptom": "hyperactivity", "condition": "Attention Deficit Hyperactivity Disorder"},
    {"symptom": "impulsivity", "condition": "Attention Deficit Hyperactivity Disorder"},
    {"symptom": "inattention", "condition": "Attention Deficit Hyperactivity Disorder"},
    {"symptom": "tremors", "condition": "Parkinson's Disease"},
    {"symptom": "stiffness", "condition": "Parkinson's Disease"},
    {"symptom": "slow movement", "condition": "Parkinson's Disease"},
    {"symptom": "balance problems", "condition": "Parkinson's Disease"},
    {"symptom": "seizures", "condition": "Epilepsy"},
    {"symptom": "loss of consciousness", "condition": "Epilepsy"},
    {"symptom": "numbness", "condition": "Multiple Sclerosis"},
    {"symptom": "tingling", "condition": "Multiple Sclerosis"},
    {"symptom": "weakness", "condition": "Multiple Sclerosis"},
    {"symptom": "vision problems", "condition": "Multiple Sclerosis"},
    {"symptom": "speech difficulties", "condition": "Stroke"},
    {"symptom": "facial drooping", "condition": "Stroke"},
    {"symptom": "arm weakness", "condition": "Stroke"},
    {"symptom": "difficulty walking", "condition": "Stroke"},
    {"symptom": "sudden confusion", "condition": "Stroke"},
    {"symptom": "severe headache", "condition": "Stroke"},
    {"symptom": "chest tightness", "condition": "Asthma"},
    {"symptom": "wheezing", "condition": "Asthma"},
    {"symptom": "shortness of breath", "condition": "Asthma"},
    {"symptom": "coughing at night", "condition": "Asthma"},
    {"symptom": "chronic cough", "condition": "Chronic Obstructive Pulmonary Disease"},
    {"symptom": "shortness of breath", "condition": "Chronic Obstructive Pulmonary Disease"},
    {"symptom": "wheezing", "condition": "Chronic Obstructive Pulmonary Disease"},
    {"symptom": "chest tightness", "condition": "Chronic Obstructive Pulmonary Disease"},
    {"symptom": "frequent infections", "condition": "Chronic Obstructive Pulmonary Disease"},
    {"symptom": "blue lips", "condition": "Chronic Obstructive Pulmonary Disease"},
    {"symptom": "swelling in legs", "condition": "Heart Failure"},
    {"symptom": "fatigue", "condition": "Heart Failure"},
    {"symptom": "shortness of breath", "condition": "Heart Failure"},
    {"symptom": "rapid heartbeat", "condition": "Heart Failure"},
    {"symptom": "coughing up blood", "condition": "Tuberculosis"},
    {"symptom": "night sweats", "condition": "Tuberculosis"},
    {"symptom": "weight loss", "condition": "Tuberculosis"},
    {"symptom": "fever", "condition": "Tuberculosis"},
    {"symptom": "chills", "condition": "Tuberculosis"},
    {"symptom": "loss of appetite", "condition": "Tuberculosis"},
    {"symptom": "fatigue", "condition": "Tuberculosis"},
    {"symptom": "cough", "condition": "Tuberculosis"},
    {"symptom": "chest pain", "condition": "Tuberculosis"},
    {"symptom": "shortness of breath", "condition": "Tuberculosis"},
    {"symptom": "swollen lymph nodes", "condition": "Tuberculosis"},
    {"symptom": "abdominal swelling", "condition": "Liver Disease"},
    {"symptom": "jaundice", "condition": "Liver Disease"},
    {"symptom": "dark urine", "condition": "Liver Disease"},
    {"symptom": "pale stools", "condition": "Liver Disease"},
    {"symptom": "itchy skin", "condition": "Liver Disease"},
    {"symptom": "nausea", "condition": "Liver Disease"},
    {"symptom": "vomiting", "condition": "Liver Disease"},
    {"symptom": "loss of appetite", "condition": "Liver Disease"},
    {"symptom": "fatigue", "condition": "Liver Disease"},
    {"symptom": "bruising easily", "condition": "Liver Disease"},
    {"symptom": "bleeding easily", "condition": "Liver Disease"},
    {"symptom": "swelling in legs", "condition": "Liver Disease"},
    {"symptom": "swelling in abdomen", "condition": "Liver Disease"},
    {"symptom": "confusion", "condition": "Liver Disease"},
    {"symptom": "sleepiness", "condition": "Liver Disease"},
    {"symptom": "slurred speech", "condition": "Liver Disease"},
    {"symptom": "tremors", "condition": "Liver Disease"},
    {"symptom": "muscle cramps", "condition": "Liver Disease"},
    {"symptom": "muscle weakness", "condition": "Liver Disease"},
    {"symptom": "joint pain", "condition": "Liver Disease"},
    {"symptom": "bone pain", "condition": "Liver Disease"},
    {"symptom": "frequent urination", "condition": "Kidney Disease"},
    {"symptom": "blood in urine", "condition": "Kidney Disease"},
    {"symptom": "foamy urine", "condition": "Kidney Disease"},
    {"symptom": "swelling in legs", "condition": "Kidney Disease"},
    {"symptom": "swelling in face", "condition": "Kidney Disease"},
    {"symptom": "fatigue", "condition": "Kidney Disease"},
    {"symptom": "shortness of breath", "condition": "Kidney Disease"},
    {"symptom": "nausea", "condition": "Kidney Disease"},
    {"symptom": "vomiting", "condition": "Kidney Disease"},
    {"symptom": "loss of appetite", "condition": "Kidney Disease"},
    {"symptom": "itchy skin", "condition": "Kidney Disease"},
    {"symptom": "muscle cramps", "condition": "Kidney Disease"},
    {"symptom": "high blood pressure", "condition": "Kidney Disease"},
    {"symptom": "difficulty concentrating", "condition": "Kidney Disease"},
    {"symptom": "trouble sleeping", "condition": "Kidney Disease"},
    {"symptom": "decreased urine output", "condition": "Kidney Disease"},
    {"symptom": "puffy eyes", "condition": "Kidney Disease"},
    {"symptom": "dry skin", "condition": "Kidney Disease"},
    {"symptom": "increased thirst", "condition": "Kidney Disease"},
    {"symptom": "bad breath", "condition": "Kidney Disease"},
    {"symptom": "metallic taste", "condition": "Kidney Disease"},
    {"symptom": "bone pain", "condition": "Kidney Disease"},
    {"symptom": "frequent fractures", "condition": "Kidney Disease"},
    {"symptom": "stunted growth", "condition": "Kidney Disease"},
    {"symptom": "delayed puberty", "condition": "Kidney Disease"},
    {"symptom": "amenorrhea", "condition": "Kidney Disease"},
    {"symptom": "impotence", "condition": "Kidney Disease"},
    {"symptom": "decreased libido", "condition": "Kidney Disease"},
    {"symptom": "infertility", "condition": "Kidney Disease"},
    {"symptom": "recurrent infections", "condition": "Kidney Disease"},
    {"symptom": "slow healing", "condition": "Kidney Disease"},
    {"symptom": "cold intolerance", "condition": "Kidney Disease"},
    {"symptom": "heat intolerance", "condition": "Kidney Disease"},
    {"symptom": "weight gain", "condition": "Kidney Disease"},
    {"symptom": "weight loss", "condition": "Kidney Disease"},
    {"symptom": "muscle wasting", "condition": "Kidney Disease"},
    {"symptom": "fatigue", "condition": "Kidney Disease"},
    {"symptom": "weakness", "condition": "Kidney Disease"},
    {"symptom": "depression", "condition": "Kidney Disease"},
    {"symptom": "anxiety", "condition": "Kidney Disease"},
    {"symptom": "irritability", "condition": "Kidney Disease"},
    {"symptom": "mood swings", "condition": "Kidney Disease"},
    {"symptom": "confusion", "condition": "Kidney Disease"},
    {"symptom": "memory problems", "condition": "Kidney Disease"},
    {"symptom": "difficulty concentrating", "condition": "Kidney Disease"},
    {"symptom": "sleep disturbances", "condition": "Kidney Disease"},
    {"symptom": "nightmares", "condition": "Kidney Disease"},
    {"symptom": "restless legs", "condition": "Kidney Disease"},
    {"symptom": "insomnia", "condition": "Kidney Disease"},
    {"symptom": "daytime sleepiness", "condition": "Kidney Disease"},
    {"symptom": "snoring", "condition": "Kidney Disease"},
    {"symptom": "sleep apnea", "condition": "Kidney Disease"},
    {"symptom": "excessive daytime sleepiness", "condition": "Kidney Disease"},
    {"symptom": "narcolepsy", "condition": "Kidney Disease"},
    {"symptom": "cataplexy", "condition": "Kidney Disease"},
    {"symptom": "sleep paralysis", "condition": "Kidney Disease"},
    {"symptom": "hypnagogic hallucinations", "condition": "Kidney Disease"},
    {"symptom": "hypnopompic hallucinations", "condition": "Kidney Disease"},
    {"symptom": "automatic behaviors", "condition": "Kidney Disease"},
    {"symptom": "sleep attacks", "condition": "Kidney Disease"},
    {"symptom": "sleep drunkenness", "condition": "Kidney Disease"},
    {"symptom": "sleepwalking", "condition": "Kidney Disease"},
    {"symptom": "sleep talking", "condition": "Kidney Disease"},
    {"symptom": "night terrors", "condition": "Kidney Disease"},
    {"symptom": "bedwetting", "condition": "Kidney Disease"},
    {"symptom": "teeth grinding", "condition": "Kidney Disease"},
    {"symptom": "restless sleep", "condition": "Kidney Disease"},
    {"symptom": "frequent awakenings", "condition": "Kidney Disease"},
    {"symptom": "early morning awakenings", "condition": "Kidney Disease"},
    {"symptom": "difficulty falling asleep", "condition": "Kidney Disease"},
    {"symptom": "difficulty staying asleep", "condition": "Kidney Disease"},
    {"symptom": "non-restorative sleep", "condition": "Kidney Disease"},
    {"symptom": "excessive sleep", "condition": "Kidney Disease"},
    {"symptom": "insufficient sleep", "condition": "Kidney Disease"},
    {"symptom": "irregular sleep", "condition": "Kidney Disease"},
    {"symptom": "shift work sleep disorder", "condition": "Kidney Disease"},
    {"symptom": "jet lag", "condition": "Kidney Disease"},
    {"symptom": "circadian rhythm disorder", "condition": "Kidney Disease"},
    {"symptom": "delayed sleep phase syndrome", "condition": "Kidney Disease"},
    {"symptom": "advanced sleep phase syndrome", "condition": "Kidney Disease"},
    {"symptom": "non-24-hour sleep-wake disorder", "condition": "Kidney Disease"},
    {"symptom": "irregular sleep-wake rhythm", "condition": "Kidney Disease"},
    
]

# Preprocessing function
def preprocess_data(data):
    symptoms = [entry['symptom'] for entry in data]
    conditions = [entry['condition'] for entry in data]

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(symptoms)
    sequences = tokenizer.texts_to_sequences(symptoms)
    padded_sequences = pad_sequences(sequences, padding='post')

    label_encoder = LabelEncoder()
    encoded_conditions = label_encoder.fit_transform(conditions)

    return padded_sequences, encoded_conditions, tokenizer, label_encoder

X, y, tokenizer, label_encoder = preprocess_data(data)

# Save tokenizer and label encoder
with open('app/models/tokenizer.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)
with open('app/models/label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

# Create model
def create_model(input_length, output_classes):
    model = Sequential([
        Embedding(input_dim=5000, output_dim=64, input_length=input_length),
        SpatialDropout1D(0.2),
        LSTM(100, dropout=0.2, recurrent_dropout=0.2),
        Dense(100, activation='relu'),
        Dense(output_classes, activation='softmax')
    ])

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

input_length = X.shape[1]
output_classes = len(set(y))

model = create_model(input_length, output_classes)

# Train model
model.fit(X, y, epochs=10, batch_size=2, validation_split=0.2)

# Save model
model.save('app/models/model.h5')

print("✅ Model training complete and saved as model.h5")
