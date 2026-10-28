import re


SCAM_PATTERNS = {
    "Urgent language": {
        "patterns": [
            "urgent",
            "immediately",
            "act now",
            "within 24 hours",
            "last warning",
            "final warning",
            "do not delay"
        ],
        "score": 15
    },

    "Money request": {
        "patterns": [
            "send money",
            "transfer money",
            "pay now",
            "payment required",
            "pay immediately",
            "registration fee",
            "delivery fee",
            "processing fee",
            "pay a fee",
            "make a payment"
        ],
        "score": 20
    },

    "Banking information": {
        "patterns": [
            "bank account",
            "account number",
            "card number",
            "cvv",
            "pin",
            "otp",
            "one time password",
            "bank details"
        ],
        "score": 25
    },

    "Prize/lottery scam": {
        "patterns": [
            "you won",
            "winner",
            "lottery",
            "prize",
            "claim your reward",
            "lucky winner",
            "cash prize"
        ],
        "score": 20
    },

    "Suspicious links": {
        "patterns": [
            "click here",
            "verify your account",
            "login here",
            "verify your identity",
            "http://",
            "https://"
        ],
        "score": 20
    },

    "Threatening language": {
        "patterns": [
            "legal action",
            "police complaint",
            "arrest",
            "account suspended",
            "account blocked",
            "police case",
            "legal notice"
        ],
        "score": 20
    },

    "Suspicious job offer": {
        "patterns": [
            "selected for a job",
            "job opportunity",
            "registration fee",
            "pay to confirm",
            "work from home"
        ],
        "score": 15
    },

    "Fake delivery": {
        "patterns": [
            "parcel delivery",
            "delivery is on hold",
            "delivery failed",
            "verify delivery",
            "package is on hold"
        ],
        "score": 15
    },

    "Fake support": {
        "patterns": [
            "customer support",
            "support team",
            "payment could not be processed",
            "contact support"
        ],
        "score": 10
    }
}


def detect_scam(message):

    text = message.lower()

    score = 0
    warnings = []

    for category, details in SCAM_PATTERNS.items():

        category_found = False

        for pattern in details["patterns"]:

            if pattern in text:

                if not category_found:

                    warnings.append(category)
                    score += details["score"]
                    category_found = True

    # Detect phone numbers
    phone_pattern = r"\b\d{10}\b"

    if re.search(phone_pattern, text):

        warnings.append("Phone number detected")
        score += 5

    # Detect excessive exclamation marks
    exclamation_count = text.count("!")

    if exclamation_count >= 3:

        warnings.append("Excessive urgency/exclamation marks")
        score += 5

    # Keep score between 0 and 100
    score = min(score, 100)

    # Determine risk level
    if score >= 60:

        risk = "HIGH RISK"

        recommendation = (
            "Do not click links, make payments, "
            "or share personal information."
        )

    elif score >= 30:

        risk = "MEDIUM RISK"

        recommendation = (
            "Verify the sender through an official source "
            "before taking any action."
        )

    else:

        risk = "LOW RISK"

        recommendation = (
            "No major scam indicators detected. "
            "Continue to stay alert."
        )

    return {
        "score": score,
        "risk": risk,
        "warnings": warnings,
        "recommendation": recommendation
    }