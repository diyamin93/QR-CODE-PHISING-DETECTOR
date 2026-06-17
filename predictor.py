
import warnings
warnings.filterwarnings("ignore")

import pickle
import numpy as np
import pandas as pd
import re

from utils.feature_extractor import extract_features


# =========================
# LOAD MODEL
# =========================

with open("models/model.pkl", "rb") as file:

    model = pickle.load(file)


class URLPredictor:

    @staticmethod
    def predict(url):

        # =========================
        # EXTRACT FEATURES
        # =========================

        features = extract_features(url)

        # =========================
        # FEATURE NAMES
        # =========================

        feature_names = [

            "having_IP_Address",
            "URL_Length",
            "Shortining_Service",
            "having_At_Symbol",
            "double_slash_redirecting",
            "Prefix_Suffix",
            "having_Sub_Domain",
            "SSLfinal_State",
            "HTTPS_token",
            "Request_URL",

            "URL_of_Anchor",
            "Links_in_tags",
            "SFH",
            "Submitting_to_email",
            "Abnormal_URL",

            "Redirect",
            "on_mouseover",
            "RightClick",
            "Iframe"

        ]

        # =========================
        # CONVERT TO DATAFRAME
        # =========================

        features_array = pd.DataFrame(
            [features],
            columns=feature_names
        )

        # =========================
        # ML PREDICTION
        # =========================

        ml_prediction = model.predict(features_array)[0]

        probabilities = model.predict_proba(features_array)[0]

        confidence = round(max(probabilities) * 100, 2)

        # =========================
        # CUSTOM RISK ANALYSIS
        # =========================

        risk_score = 0

        suspicious_words = [

            "login",
            "verify",
            "secure",
            "update",
            "bank",
            "paypal",
            "account",
            "signin",
            "wallet",
            "bonus",
            "free",
            "gift",
            "crypto",
            "otp",
            "confirm",
            "unlock",
            "recover",
            "reward",
            "win",
            "prize",
            "limited",
            "offer"

        ]

        suspicious_tlds = [

            ".tk",
            ".ru",
            ".ml",
            ".ga",
            ".cf",
            ".gq",
            ".xyz"

        ]

        # =========================
        # KEYWORD CHECK
        # =========================

        if any(word in url.lower() for word in suspicious_words):

            risk_score += 2

        # =========================
        # TLD CHECK
        # =========================

        if any(tld in url.lower() for tld in suspicious_tlds):

            risk_score += 2

        # =========================
        # @ SYMBOL CHECK
        # =========================

        if "@" in url:

            risk_score += 2

        # =========================
        # IP ADDRESS CHECK
        # =========================

        ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'

        if re.search(ip_pattern, url):

            risk_score += 2

        # =========================
        # HYPHEN CHECK
        # =========================

        if url.count("-") >= 2:

            risk_score += 2

        # =========================
        # LONG URL CHECK
        # =========================

        if len(url) > 75:

            risk_score += 1

        # =========================
        # TOO MANY DIGITS
        # =========================

        digit_count = sum(c.isdigit() for c in url)

        if digit_count >= 5:

            risk_score += 2

        # =========================
        # FINAL DECISION
        # =========================

        if risk_score >= 3:

            final_prediction = -1
            risk = "Phishing"

        else:

            final_prediction = ml_prediction

            if final_prediction == -1:

                risk = "Phishing"

            else:

                risk = "Safe"

        # =========================
        # EXPLAINABLE AI REASONS
        # =========================

        reasons = []

        # Suspicious keyword

        if any(word in url.lower() for word in suspicious_words):

            reasons.append(
                "Suspicious phishing keywords detected in URL"
            )

        # Suspicious TLD

        if any(tld in url.lower() for tld in suspicious_tlds):

            reasons.append(
                "Suspicious domain extension detected"
            )

        # @ symbol

        if "@" in url:

            reasons.append(
                "@ symbol found in URL"
            )

        # IP Address

        if re.search(ip_pattern, url):

            reasons.append(
                "IP address used instead of domain name"
            )

        # Too many hyphens

        if url.count("-") >= 2:

            reasons.append(
                "Too many hyphens found in URL"
            )

        # Long URL

        if len(url) > 75:

            reasons.append(
                "URL length unusually long"
            )

        # Too many digits

        if digit_count >= 5:

            reasons.append(
                "Too many numeric characters detected"
            )

        # ML Feature-based reasoning

        for i in range(min(len(features), len(feature_names))):

            if features[i] == -1:

                reasons.append(
                    f"Suspicious feature triggered: {feature_names[i]}"
                )

        # If no reasons

        if len(reasons) == 0:

            reasons.append(
                "No major phishing indicators detected"
            )

        # =========================
        # RETURN RESULT
        # =========================

        return {

            'prediction': final_prediction,
            'risk': risk,
            'probability': confidence,
            'features': features,
            'risk_score': risk_score,
            'reasons': reasons

        }