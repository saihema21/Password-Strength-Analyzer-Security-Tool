import streamlit as st
import secrets
import string
from utils.analyzer import analyze_password

st.set_page_config(
    page_title="Password Strength Analyzer",
    page_icon="🔐",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: white;
    color: black;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

h1, h2, h3, p, label {
    color: black !important;
}

section[data-testid="stSidebar"] {
    background-color: #f5f5f5;
}

section[data-testid="stSidebar"] * {
    color: black !important;
}

.card {
    background-color: #f8f9fa;
    border: 1px solid #dddddd;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 10px;
}

.finding {
    background-color: #fff4e5;
    border: 1px solid #ffcc80;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 8px;
}

.recommendation {
    background-color: #eef9f0;
    border: 1px solid #b7dfba;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 8px;
}

.pattern {
    background-color: #f8f9fa;
    border: 1px solid #dddddd;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
}

.footer {
    text-align: center;
    color: #666666;
    font-size: 13px;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🔐 SentinelPass")
    st.caption("Password Security Intelligence")

    st.markdown("---")

    st.subheader("Analysis Settings")

    show_entropy = st.checkbox(
        "Show entropy estimate",
        value=True
    )

    show_metrics = st.checkbox(
        "Show detailed metrics",
        value=True
    )

    st.markdown("---")

    st.subheader("Security Checks")

    st.write("✓ Password length")
    st.write("✓ Character diversity")
    st.write("✓ Common passwords")
    st.write("✓ Sequential patterns")
    st.write("✓ Keyboard patterns")
    st.write("✓ Repeated patterns")
    st.write("✓ Predictable structures")
    st.write("✓ Personal information")

st.title("🔐 Password Strength Analyzer")

st.write(
    "Analyze password security using length, character diversity, "
    "common-password detection, pattern analysis and entropy concepts."
)

st.info(
    "🔒 Privacy-first analysis: Passwords are analyzed locally "
    "and are not stored, logged, or transmitted."
)

st.header("Password Analysis")

password = st.text_input(
    "Enter password",
    type="password",
    placeholder="Enter a password for analysis..."
)

with st.expander("Optional: Personal Information Check"):

    st.write(
        "Enter information such as a name, college, company "
        "or birth year for a local comparison."
    )

    personal_info_text = st.text_input(
        "Personal information",
        placeholder="Example: Alex, 2004, ABC College"
    )

    personal_info = [
        item.strip()
        for item in personal_info_text.split(",")
        if item.strip()
    ]

if password:

    result = analyze_password(
        password,
        personal_info=personal_info
    )

    score = result["score"]
    classification = result["classification"]
    findings = result["findings"]
    suggestions = result["suggestions"]
    metrics = result["metrics"]

    st.markdown("---")
    st.header("Security Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Security Score",
            f"{score}/100"
        )

    with col2:
        st.metric(
            "Classification",
            classification
        )

    with col3:
        st.metric(
            "Password Length",
            f"{metrics['length']} characters"
        )

    st.progress(score / 100)

    if classification == "VERY WEAK":
        st.error(
            "🔴 VERY WEAK — Immediate improvement recommended."
        )

    elif classification == "WEAK":
        st.warning(
            "🟠 WEAK — Significant security improvements recommended."
        )

    elif classification == "MODERATE":
        st.warning(
            "🟡 MODERATE — Consider strengthening this password."
        )

    elif classification == "STRONG":
        st.success(
            "🟢 STRONG — Good password characteristics detected."
        )

    else:
        st.success(
            "🟢 VERY STRONG — Strong security characteristics detected."
        )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("⚠️ Security Findings")

        if findings:

            for finding in findings:
                st.markdown(
                    f'<div class="finding">⚠️ {finding}</div>',
                    unsafe_allow_html=True
                )

        else:
            st.success(
                "✅ No major security weaknesses detected."
            )

    with col2:

        st.subheader("🛡️ Security Recommendations")

        for suggestion in suggestions:
            st.markdown(
                f'<div class="recommendation">→ {suggestion}</div>',
                unsafe_allow_html=True
            )

    if show_metrics:

        st.markdown("---")
        st.header("Detailed Security Metrics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Character Types",
                f"{metrics['character_types']}/4"
            )

        with col2:
            st.metric(
                "Unique Ratio",
                f"{metrics['unique_ratio'] * 100:.0f}%"
            )

        with col3:
            st.metric(
                "Common Password",
                "Yes" if metrics["common_password"] else "No"
            )

        with col4:
            st.metric(
                "Entropy",
                f"{metrics['entropy_estimate']} bits"
            )

    st.markdown("---")
    st.header("🔍 Pattern Intelligence")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<div class="pattern">'
            '<b>Repeated Characters</b><br><br>'
            + (
                "⚠️ DETECTED"
                if metrics["repeated_characters"]
                else "✅ NOT DETECTED"
            )
            + "</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="pattern">'
            '<b>Repeated Substring</b><br><br>'
            + (
                "⚠️ DETECTED"
                if metrics["repeated_substring"]
                else "✅ NOT DETECTED"
            )
            + "</div>",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="pattern">'
            '<b>Keyboard Pattern</b><br><br>'
            + (
                "⚠️ DETECTED"
                if metrics["keyboard_pattern"]
                else "✅ NOT DETECTED"
            )
            + "</div>",
            unsafe_allow_html=True
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<div class="pattern">'
            '<b>Sequential Pattern</b><br><br>'
            + (
                "⚠️ DETECTED"
                if metrics["sequence_detected"]
                else "✅ NOT DETECTED"
            )
            + "</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="pattern">'
            '<b>Predictable Structure</b><br><br>'
            + (
                "⚠️ DETECTED"
                if metrics["predictable_structure"]
                else "✅ NOT DETECTED"
            )
            + "</div>",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="pattern">'
            '<b>Personal Information</b><br><br>'
            + (
                "⚠️ DETECTED"
                if metrics["personal_information_detected"]
                else "✅ NOT DETECTED"
            )
            + "</div>",
            unsafe_allow_html=True
        )

    if show_entropy:

        st.markdown("---")
        st.header("🧮 Entropy-Style Estimate")

        st.metric(
            "Estimated Entropy",
            f"{metrics['entropy_estimate']} bits"
        )

        st.caption(
            "This is an entropy-style estimate based on password "
            "length and estimated character pool. It does not "
            "guarantee real-world password security."
        )

else:

    st.info(
        "👆 Enter a password above to begin the security analysis."
    )

st.markdown("---")

st.header("🔑 Secure Password Generator")

st.write(
    "Generate a strong random password using Python's "
    "cryptographically secure secrets module."
)

col1, col2 = st.columns(2)

with col1:

    generator_length = st.slider(
        "Password Length",
        min_value=16,
        max_value=32,
        value=20
    )

with col2:

    include_symbols = st.checkbox(
        "Include Symbols",
        value=True
    )

if st.button(
    "⚡ Generate Secure Password",
    use_container_width=True
):

    characters = string.ascii_letters + string.digits

    if include_symbols:
        characters += string.punctuation

    generated_password = "".join(
        secrets.choice(characters)
        for _ in range(generator_length)
    )

    st.code(generated_password)

    st.success(
        "Secure password generated successfully."
    )

    st.caption(
        "Generated passwords are not stored by this application."
    )

st.markdown("---")

st.markdown(
    '<div class="footer">'
    'SentinelPass • Defensive Cybersecurity Project<br>'
    'Privacy-focused local password analysis'
    '</div>',
    unsafe_allow_html=True
)