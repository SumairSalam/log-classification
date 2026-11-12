"""
Classify logs using MiniLM sentence embeddings and a saved classifier.
Load the classifier from the configured Joblib path and return unclassified
when the highest predicted probability is below 0.5.
"""

import os

import joblib
from sentence_transformers import SentenceTransformer

# Correct absolute path to the model file
model_path = r'D:\projects\Log-Classification\models\log_classifier.joblib'

# Check if the file exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

# Load transformer and model
transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
classifier_model = joblib.load(model_path)

def classify_with_bert(log_message):
    message_embedding = transformer_model.encode([log_message])  # wrap in list
    probabilities = classifier_model.predict_proba(message_embedding)[0]
    if max(probabilities) < 0.5:
        return "unclassified"


    predicted_label = classifier_model.predict(message_embedding)[0]

    return predicted_label

if __name__ == "__main__":
    logs = [
         "alpha.osapi_compute.wsgi.server - 12.10.11.1 - API returned 404 not found error",
         "GET /v2/3454/servers/detail HTTP/1.1 RCODE 404 len: 1583 time: 0.1878400",
         "System crashed due to drivers errors when restarting the server",
        "Hey bro, chill ya!",
         "Multiple login failures occurred on user 6454 account",
         "Server A790 was restarted unexpectedly during the process of data transfer"
    ]


    for log in logs:
        label = classify_with_bert(log)
        print(log, "->", label)

