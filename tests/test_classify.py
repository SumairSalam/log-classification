import os

import pandas as pd

from classify import classify, classify_csv


def test_classify_simple():
    logs = [
        ("BillingSystem", "User 12345 logged in."),
        ("LegacyCRM", "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."),
    ]
    res = classify(logs)
    assert isinstance(res, list)
    assert res[0][1]  # label exists


def test_classify_csv(tmp_path):
    input_csv = tmp_path / "input.csv"
    df = pd.DataFrame({"source": ["BillingSystem"], "log_message": ["User 12345 logged in."]})
    df.to_csv(input_csv, index=False)
    out = classify_csv(str(input_csv))
    assert os.path.exists(out)
    odf = pd.read_csv(out)
    assert "target_label" in odf.columns
