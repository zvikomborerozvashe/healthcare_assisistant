import tensorflow as tf
from tensorflow.keras.models import load_model
import pickle
from tensorflow.keras.utils import pad_sequences
import numpy as np

# Load model and dependencies
model = load_model('app/models/model.h5')
with open('app/models/tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)
with open('app/models/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

def predict_condition(symptom_input):
    sequence = tokenizer.texts_to_sequences([symptom_input])
    padded_sequence = pad_sequences(sequence, padding='post', maxlen=10)
    prediction = model.predict(padded_sequence)
    predicted_class = np.argmax(prediction, axis=1)
    condition = label_encoder.inverse_transform(predicted_class)
    return condition[0]

if __name__ == '__main__':
    symptom = input("Enter a symptom: ")
    print(f"Predicted Condition: {predict_condition(symptom)}")
