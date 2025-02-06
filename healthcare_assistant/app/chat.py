from flask import Flask, request, jsonify
from flask_cors import CORS
from doctor_recommendation import predict_condition_and_recommend_doctor  # Import function

app = Flask(__name__)
CORS(app)   #to avoid blocks


@app.route('/chat', methods=['GET','POST'])
def chat():
    """
    Chatbot that responds to user messages, detects symptoms, and suggests doctors.
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

if __name__ == '__main__':
    app.run(debug=True)
