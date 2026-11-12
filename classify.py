"""
Route log messages through the local prototype classification functions.
Use keyword rules for LegacyCRM and regex rules with a placeholder fallback
for other sources. Export CSV labels and return the saved output path.
"""

# classify.py
import pandas as pd


def classify_with_regex(log_message):
    import re

    if re.search(r"(blocked|attack|access escalation|unauthorized|threat)", log_message, re.IGNORECASE):
        return "Security Alert"
    elif re.search(r"(logged in|login|user\s+\d+)", log_message, re.IGNORECASE):
        return "User Action"
    elif re.search(r"(uploaded|backup completed|saved successfully)", log_message, re.IGNORECASE):
        return "System Notification"
    elif re.search(r"(deprecated|no longer supported|retired)", log_message, re.IGNORECASE):
        return "Deprecation Warning"
    elif re.search(r"(failed|aborted|error|invalid)", log_message, re.IGNORECASE):
        return "Workflow Error"
    return None  # Fallback to BERT or LLM


def classify_with_bert(log_message):
    # Dummy placeholder for BERT logic
    return "Other"  # fallback simulation


def classify_with_llm(log_message):
    lower_msg = log_message.lower()
    if any(term in lower_msg for term in ["deprecated", "retired", "no longer supported"]):
        return "Deprecation Warning"
    elif any(term in lower_msg for term in ["failed", "aborted", "error", "invalid"]):
        return "Workflow Error"
    elif any(term in lower_msg for term in ["unauthorized", "attack", "blocked", "access escalation"]):
        return "Security Alert"
    return "Other"



def classify_log(source, log_message):
    if source == "LegacyCRM":
        label = classify_with_llm(log_message)
    else:
        label = classify_with_regex(log_message)
        if label is None:
            label = classify_with_bert(log_message)
        if label is None:
            label = "Unclassified"
    return label


def classify(logs):
    labels = []
    for source, log_msg in logs:
        label = classify_log(source, log_msg)
        labels.append((source, label, log_msg))
    return labels
def classify_csv(input_file, output_file="resources/output.csv"):
    from pathlib import Path

    df = pd.read_csv(input_file)
    df["target_label"] = [
        classify_log(source, message)
        for source, message in zip(df["source"], df["log_message"])
    ]

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return str(output_path)


if __name__ == "__main__":
    classify_csv("resources/test.csv")

    # # logs = [
    # #
    # #     ("BillingSystem", "User 12345 logged in."),
    # #     ("ModernCRM", "IP 192.168.133.114 blocked due to potential attack"),
    # #     ("AnalyticsEngine", "File data_6957.csv uploaded successfully by user User265."),
    # #     ("AnalyticsEngine", "Backup completed successfully."),
    # #     ("ModernHR", "GET /v2/5dfadb412dc4e0c8daed9335de435a0e/servers/detail HTTP/1.1 RCODE 200 Len: 1583 time: 0.187840"),
    # #     ("ModernHR", "Admin access escalation detected for user 9429"),
    # #     ("LegacyCRM", "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."),
    # #     ("LegacyCRM", "Invoice generation process aborted for order ID 8910 due to invalid tax calculation."),
    # #     ("LegacyCRM", "The 'BulkEmailSender' feature is no longer supported. Use 'EmailCampaignManager' instead."),
    # #     ("LegacyCRM", "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the new ReportAdvanced module."),
    # # ]
    #
    # classified_logs = classify(logs)
    # for source, label, msg in classified_logs:
    #     print(f"[{source}] {label}: {msg}")
