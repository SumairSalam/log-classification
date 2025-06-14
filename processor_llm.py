from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# Initialize Groq client with API key
groq = Groq(api_key=api_key)

def classify_with_llm(log_msg):
    prompt = f'''Classify the log message into one of these categories:
(1) Workflow Error, (2) Deprecation Warning.
If you can't figure out a category, return "Unclassified".
Only return the category name. No preamble.
Log message: {log_msg}'''

    # Make the API call
    chat_completion = groq.chat.completions.create(
        model="llama3-70b-8192",  # Groq model
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    # Return the model's reply
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    print(classify_with_llm(
        "Case escalation for ticket ID 7324 failed because the assigned support agent was unavailable."))

    print(classify_with_llm(
        "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the new ReportAdvanced module."))

    print(classify_with_llm("System reboot initiated by user 12345."))
