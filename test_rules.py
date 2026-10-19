from rule_based import apply_rules

sample = "URGENT: Your account will be suspended. Click here to verify your account and confirm your password within 24 hours: http://192.168.1.5/login"
print(apply_rules(sample))