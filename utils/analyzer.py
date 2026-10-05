import math
import re
import string
from pathlib import Path


# ---------------------------------------------------------
# Load common passwords
# ---------------------------------------------------------

COMMON_PASSWORD_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "common_passwords.txt"
)


def load_common_passwords():
    if not COMMON_PASSWORD_FILE.exists():
        return set()

    with open(COMMON_PASSWORD_FILE, "r", encoding="utf-8") as file:
        return {
            line.strip().lower()
            for line in file
            if line.strip()
        }


# ---------------------------------------------------------
# Character analysis
# ---------------------------------------------------------

def analyze_characters(password):
    return {
        "has_lowercase": bool(re.search(r"[a-z]", password)),
        "has_uppercase": bool(re.search(r"[A-Z]", password)),
        "has_digits": bool(re.search(r"\d", password)),
        "has_symbols": bool(re.search(r"[^A-Za-z0-9]", password)),
    }


# ---------------------------------------------------------
# Repeated character detection
# ---------------------------------------------------------

def has_repeated_characters(password):
    return bool(re.search(r"(.)\1{2,}", password))


# ---------------------------------------------------------
# Repeated substring detection
# ---------------------------------------------------------

def has_repeated_substring(password):
    length = len(password)

    for size in range(2, length // 2 + 1):
        for i in range(length - size * 2 + 1):
            part = password[i:i + size]

            if password[i + size:i + size * 2] == part:
                return True

    return False


# ---------------------------------------------------------
# Sequence detection
# ---------------------------------------------------------

def has_sequence(password):
    password_lower = password.lower()

    sequences = [
        "0123",
        "1234",
        "2345",
        "3456",
        "4567",
        "5678",
        "6789",
        "9876",
        "8765",
        "7654",
        "6543",
        "5432",
        "4321",
        "3210",
        "abcd",
        "bcde",
        "cdef",
        "defg",
        "efgh",
        "hgfe",
        "gfed",
        "fedc",
        "dcba",
    ]

    return any(sequence in password_lower for sequence in sequences)


# ---------------------------------------------------------
# Keyboard pattern detection
# ---------------------------------------------------------

def has_keyboard_pattern(password):
    password_lower = password.lower()

    keyboard_patterns = [
        "qwerty",
        "asdf",
        "zxcv",
        "qwerty123",
        "asdf123",
        "qaz",
        "wsx",
        "edc",
    ]

    return any(pattern in password_lower for pattern in keyboard_patterns)


# ---------------------------------------------------------
# Predictable word + number/year detection
# ---------------------------------------------------------

def has_predictable_structure(password):
    password_lower = password.lower()

    common_words = [
        "password",
        "welcome",
        "admin",
        "hello",
        "user",
        "login",
        "letmein",
    ]

    for word in common_words:
        if word in password_lower:
            return True

    if re.search(r"(19|20)\d{2}", password):
        return True

    return bool(re.search(r"[A-Za-z]+\d{2,}$", password))


# ---------------------------------------------------------
# Character pool and entropy-style estimate
# ---------------------------------------------------------

def calculate_entropy(password):
    if not password:
        return 0.0

    pool_size = 0

    if re.search(r"[a-z]", password):
        pool_size += 26

    if re.search(r"[A-Z]", password):
        pool_size += 26

    if re.search(r"\d", password):
        pool_size += 10

    if re.search(r"[^A-Za-z0-9]", password):
        pool_size += 32

    if pool_size == 0:
        return 0.0

    return round(len(password) * math.log2(pool_size), 2)


# ---------------------------------------------------------
# Main password analyzer
# ---------------------------------------------------------

def analyze_password(password, personal_info=None):
    if password is None:
        password = ""

    findings = []
    suggestions = []

    length = len(password)

    # Character analysis
    character_info = analyze_characters(password)

    character_types = sum(character_info.values())

    unique_ratio = (
        len(set(password)) / length
        if length > 0
        else 0
    )

    # Common password
    common_passwords = load_common_passwords()

    is_common = password.lower() in common_passwords

    # Patterns
    repeated_characters = has_repeated_characters(password)
    repeated_substring = has_repeated_substring(password)
    sequence = has_sequence(password)
    keyboard = has_keyboard_pattern(password)
    predictable = has_predictable_structure(password)

    # Personal information
    personal_match = False

    if personal_info:
        for value in personal_info:
            if value and value.lower() in password.lower():
                personal_match = True
                break

    # -----------------------------------------------------
    # Findings
    # -----------------------------------------------------

    if length == 0:
        findings.append("Password is empty.")

    elif length < 8:
        findings.append("Password is very short.")

    elif length < 12:
        findings.append("Password is shorter than recommended.")

    elif length >= 16:
        findings.append("Password has strong length.")

    if character_types < 2 and length > 0:
        findings.append("Password uses very limited character diversity.")

    if repeated_characters:
        findings.append("Repeated characters detected.")

    if repeated_substring:
        findings.append("Repeated substring pattern detected.")

    if sequence:
        findings.append("Sequential characters detected.")

    if keyboard:
        findings.append("Keyboard pattern detected.")

    if is_common:
        findings.append("Password matches a common password.")

    if predictable:
        findings.append("Predictable word or number pattern detected.")

    if personal_match:
        findings.append("Password contains supplied personal information.")

    # -----------------------------------------------------
    # Score calculation
    # -----------------------------------------------------

    score = 0

    # Length: maximum 35
    if length >= 16:
        score += 35
    elif length >= 12:
        score += 27
    elif length >= 8:
        score += 18
    elif length >= 4:
        score += 8

    # Character diversity: maximum 15
    score += min(character_types * 3, 15)

    # Unique ratio: maximum 10
    score += round(unique_ratio * 10)

    # Pattern resistance: maximum 20
    pattern_penalty = 0

    if repeated_characters:
        pattern_penalty += 6

    if repeated_substring:
        pattern_penalty += 5

    if sequence:
        pattern_penalty += 5

    if keyboard:
        pattern_penalty += 5

    score += max(20 - pattern_penalty, 0)

    # Non-common password: maximum 10
    if not is_common:
        score += 10

    # Additional unpredictability: maximum 10
    if not predictable:
        score += 5

    if not personal_match:
        score += 5

    # -----------------------------------------------------
    # Major penalties
    # -----------------------------------------------------

    if is_common:
        score -= 25

    if keyboard:
        score -= 10

    if sequence:
        score -= 8

    if repeated_characters:
        score -= 8

    if repeated_substring:
        score -= 6

    if predictable:
        score -= 8

    if personal_match:
        score -= 10

    score = max(0, min(score, 100))

    # -----------------------------------------------------
    # Classification
    # -----------------------------------------------------

    if score <= 20:
        classification = "VERY WEAK"
    elif score <= 40:
        classification = "WEAK"
    elif score <= 60:
        classification = "MODERATE"
    elif score <= 80:
        classification = "STRONG"
    else:
        classification = "VERY STRONG"

    # -----------------------------------------------------
    # Suggestions
    # -----------------------------------------------------

    if length < 12:
        suggestions.append(
            "Use a longer password or passphrase with at least 12 characters."
        )

    if length < 16:
        suggestions.append(
            "Consider using 16 or more characters for stronger protection."
        )

    if character_types < 3:
        suggestions.append(
            "Increase character diversity by combining different character types."
        )

    if repeated_characters or repeated_substring:
        suggestions.append(
            "Avoid repeated characters or repeated patterns."
        )

    if sequence:
        suggestions.append(
            "Avoid predictable sequences such as 1234 or abcd."
        )

    if keyboard:
        suggestions.append(
            "Avoid keyboard patterns such as qwerty or asdf."
        )

    if is_common:
        suggestions.append(
            "Avoid commonly used passwords."
        )

    if predictable:
        suggestions.append(
            "Avoid predictable words, years, and word-plus-number patterns."
        )

    if personal_match:
        suggestions.append(
            "Avoid using personal information such as names, college names, or birth years."
        )

    suggestions.extend([
        "Use a unique password for every important account.",
        "Consider using a password manager.",
        "Enable multi-factor authentication (MFA) whenever available.",
    ])

    # Remove duplicate suggestions
    suggestions = list(dict.fromkeys(suggestions))

    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    metrics = {
        "length": length,
        "character_types": character_types,
        "unique_ratio": round(unique_ratio, 2),
        "entropy_estimate": calculate_entropy(password),
        "common_password": is_common,
        "repeated_characters": repeated_characters,
        "repeated_substring": repeated_substring,
        "sequence_detected": sequence,
        "keyboard_pattern": keyboard,
        "predictable_structure": predictable,
        "personal_information_detected": personal_match,
    }

    return {
        "score": score,
        "classification": classification,
        "findings": findings,
        "suggestions": suggestions,
        "metrics": metrics,
    }