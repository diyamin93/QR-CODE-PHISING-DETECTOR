import re
from urllib.parse import urlparse


def extract_features(url):

    features = []

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    path = parsed.path.lower()

    full_url = url.lower()

    # =========================================
    # 1. HAVING IP ADDRESS
    # =========================================

    ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'

    if re.search(ip_pattern, domain):

        features.append(-1)

    else:

        features.append(1)

    # =========================================
    # 2. URL LENGTH
    # =========================================

    if len(url) < 54:

        features.append(1)

    elif len(url) <= 75:

        features.append(0)

    else:

        features.append(-1)

    # =========================================
    # 3. SHORTENED URL
    # =========================================

    shortening_services = (
        r"bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co|"
        r"is\.gd|buff\.ly|adf\.ly|cutt\.ly"
    )

    if re.search(shortening_services, full_url):

        features.append(-1)

    else:

        features.append(1)

    # =========================================
    # 4. @ SYMBOL
    # =========================================

    if "@" in full_url:

        features.append(-1)

    else:

        features.append(1)

    # =========================================
    # 5. DOUBLE SLASH REDIRECTING
    # =========================================

    if full_url.rfind('//') > 7:

        features.append(-1)

    else:

        features.append(1)

    # =========================================
    # 6. PREFIX SUFFIX (-)
    # =========================================

    if '-' in domain:

        features.append(-1)

    else:

        features.append(1)

    # =========================================
    # 7. SUBDOMAIN COUNT
    # =========================================

    dots = domain.count('.')

    if dots == 1:

        features.append(1)

    elif dots == 2:

        features.append(0)

    else:

        features.append(-1)

    # =========================================
    # 8. HTTPS
    # =========================================

    if parsed.scheme == "https":

        features.append(1)

    else:

        features.append(-1)

    # =========================================
    # 9. HTTPS TOKEN MISUSE
    # =========================================

    if 'https' in domain:

        features.append(-1)

    else:

        features.append(1)

    # =========================================
    # 10. SUSPICIOUS WORDS
    # =========================================

    suspicious_words = [

        "login",
        "verify",
        "update",
        "secure",
        "bank",
        "paypal",
        "confirm",
        "account",
        "payment",
        "wallet",
        "signin",
        "bonus",
        "gift",
        "free",
        "claim",
        "crypto",
        "upi",
        "otp"

    ]

    if any(word in full_url for word in suspicious_words):

        features.append(-1)

    else:

        features.append(1)

    # =========================================
    # 11. URL OF ANCHOR
    # =========================================

    if "#" in full_url:

        features.append(-1)

    else:

        features.append(1)

    # =========================================
    # 12. SUSPICIOUS FILE EXTENSIONS
    # =========================================

    suspicious_extensions = [

        ".exe",
        ".zip",
        ".rar",
        ".scr",
        ".bat",
        ".cmd",
        ".php"

    ]

    if any(ext in path for ext in suspicious_extensions):

        features.append(-1)

    else:

        features.append(1)

    # =========================================
    # 13. FORM SUBMISSION KEYWORDS
    # =========================================

    if "submit" in full_url or "form" in full_url:

        features.append(-1)

    else:

        features.append(1)

    # =========================================
    # 14. SUBMITTING TO EMAIL
    # =========================================

    if "mailto:" in full_url:

        features.append(-1)

    else:

        features.append(1)

    # =========================================
    # 15. ABNORMAL URL
    # =========================================

    if len(domain) == 0:

        features.append(-1)

    else:

        features.append(1)

    # =========================================
    # 16. TOO MANY REDIRECTS
    # =========================================

    if full_url.count("//") > 1:

        features.append(-1)

    else:

        features.append(1)

    # =========================================
    # 17. MOUSEOVER KEYWORD
    # =========================================

    if "mouseover" in full_url:

        features.append(-1)

    else:

        features.append(1)

    # =========================================
    # 18. RIGHT CLICK DISABLED
    # =========================================

    if "rightclick" in full_url:

        features.append(-1)

    else:

        features.append(1)

    # =========================================
    # 19. IFRAME
    # =========================================

    if "iframe" in full_url:

        features.append(-1)

    else:

        features.append(1)

    return features
    