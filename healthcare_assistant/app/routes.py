from flask import Blueprint, Flask, request, jsonify
from app.models.predict import predict_condition
from app.doctor_recommendation import predict_condition_and_recommend_doctor  # Import prediction functions

# Define Blueprint
main = Blueprint("main", __name__)

@main.route("/predict", methods=["POST"])
def predict():
    # Get symptom from POST request
    data = request.get_json()
    symptom = data.get('symptom')

    if not symptom:
        return jsonify({'error': 'No symptom provided'}), 400

    # Get the prediction
    condition = predict_condition(symptom)

    # Return the prediction as a JSON response
    return jsonify({'symptom': symptom, 'predicted_condition': condition})


@main.route('/doctor_recommendation', methods=['POST'])
def doctor_recommendation():
    data = request.get_json()
    symptom = data.get('symptom', '')
    
    # Call the function to predict the condition and recommend a doctor
    predicted_condition, doctor_info = predict_condition_and_recommend_doctor(symptom)
    
    # Prepare the response
    response = {
        "predicted_condition": predicted_condition,
        "doctor": doctor_info["doctor"],
        "specialty": doctor_info["specialty"]
    }
    
    return jsonify(response)


@main.route('/chat', methods=['POST'])  # <--- FIXED this line to use `main`
def chat():
    """
    Chatbot route that processes user messages, detects symptoms, and suggests doctors.
    """
    data = request.get_json()
    user_message = data.get("message", "").lower().strip()

    if not user_message:
        return jsonify({"response": "I'm sorry, I didn't understand that. Can you describe your symptoms?"}), 400

    # Check for any symptom in user message
    detected_symptom = None
    for symptom in predict_condition_and_recommend_doctor.__globals__['symptoms_disease_map'].keys():
        if symptom in user_message:
            detected_symptom = symptom
            break

    if detected_symptom:
        # Predict the condition and recommend a doctor
        predicted_condition, doctor_info = predict_condition_and_recommend_doctor(detected_symptom)

        chatbot_response = (
            f"It looks like you might have {predicted_condition}. "
            f"I recommend visiting {doctor_info['doctor']}, a specialist in {doctor_info['specialty']}."
        )
    else:
        chatbot_response = "I'm not sure about your symptoms. Can you describe them in more detail?"

    return jsonify({"response": chatbot_response})
