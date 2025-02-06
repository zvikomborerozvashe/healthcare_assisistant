import numpy as np
import tensorflow as tf
from flask import jsonify

# Load trained model (Replace 'model.h5' with your actual trained model)
model = tf.keras.models.load_model("model.h5")

# Define symptom labels (example)
SYMPTOMS = ["fever", "cough", "fatigue", "headache"]

# Predict disease from symptoms
def predict_disease(symptoms):
    # Convert symptoms into input vector
    input_vector = np.array([1 if s in symptoms else 0 for s in SYMPTOMS]).reshape(1, -1)
    prediction = model.predict(input_vector)

    # Get the disease with the highest probability
    predicted_disease = np.argmax(prediction)
    
    return jsonify({"disease": predicted_disease})
