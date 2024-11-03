# custom_nlg_server.py

from flask import Flask, request, jsonify
import requests
from config import tts_config
app = Flask(__name__)
"""
used for custom responses text  generation knowing the response name from rasa 

"""
# Define the REST endpoint URL to forward messages
REST_ENDPOINT_URL = tts_config["TTS_API_URL"]

@app.route("/nlg", methods=["POST"])
def nlg():
    data = request.json
    print(data)

    # Extract the message text that Rasa wants to send to the user
    message_text = data["response"]

    # Forward the message to the external REST endpoint
    payload = {
        "voice":"English-US.Female-1",
        "text": message_text 
    }
    try:
        response = requests.post(REST_ENDPOINT_URL, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        print(f"Failed to send message to endpoint: {e}")

    # Send the message back to Rasa for delivery to the user
    return jsonify({"text": message_text})

if __name__ == "__main__":
    app.run(port=5056)
