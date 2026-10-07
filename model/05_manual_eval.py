from predictor import predict_email

test_cases = [
    {"text": "Dear user, your PayPal account has been limited. Click here to restore access: http://paypa1-secure.com/login", "label": "Phishing"},
    {"text": "Hi team, attached is the agenda for tomorrow's 10am standup. See you there.", "label": "Legitimate"},
    # add more...
]

correct = 0
for case in test_cases:
    result = predict_email(case["text"])
    match = result["final_label"] == case["label"]
    correct += match
    print(f"Expected: {case['label']:10} | Got: {result['final_label']:10} | {'✓' if match else '✗'}")

print(f"\nAccuracy on manual test set: {correct}/{len(test_cases)}")