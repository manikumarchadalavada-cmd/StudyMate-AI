import os
import streamlit as st
from google import genai


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

css = """
<style>

.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 1.1rem;
    color: #666;
    margin-bottom: 25px;
}

.result-box {
    padding: 20px;
    border: 1px solid #dddddd;
    border-radius: 15px;
    background-color: #fafafa;
    margin-top: 10px;
}

</style>
"""

st.markdown(css, unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎓 StudyMate AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your AI-powered study companion for notes, quizzes, '
    'answer improvement, and concept explanations.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# GEMINI API KEY
# ============================================================

gemini_api_key = None

try:
    gemini_api_key = st.secrets.get("GEMINI_API_KEY")
except Exception:
    gemini_api_key = None

if not gemini_api_key:
    gemini_api_key = os.getenv("GEMINI_API_KEY")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ StudyMate AI")

    feature = st.radio(
        "Choose a study utility:",
        [
            "📝 Summarize Notes",
            "❓ Generate Quiz",
            "✍️ Improve Answer",
            "💡 Explain Concept"
        ]
    )

    st.divider()

    st.markdown("### 📚 Available Features")

    st.write("📝 Summarize long study notes")
    st.write("❓ Generate practice MCQs")
    st.write("✍️ Improve written answers")
    st.write("💡 Explain difficult concepts")

    st.divider()

    st.caption(
        "Powered by Google Gemini API"
    )


# ============================================================
# PROMPT BUILDER
# ============================================================

def build_prompt(feature_name, content):

    if feature_name == "📝 Summarize Notes":

        return (
            "You are StudyMate AI, an academic study assistant.\n\n"
            "TASK:\n"
            "Summarize the student's study material.\n\n"
            "REQUIREMENTS:\n"
            "1. Create a clear and meaningful title.\n"
            "2. Give 5 to 10 important points.\n"
            "3. Use simple student-friendly language.\n"
            "4. Keep important definitions.\n"
            "5. Keep important facts and formulas.\n"
            "6. Do not remove important relationships between concepts.\n"
            "7. Do not add information that is not present in the material.\n"
            "8. Finish with a section called 'Quick Revision'.\n"
            "9. Quick Revision must contain exactly 3 important takeaways.\n\n"
            "STUDY MATERIAL:\n"
            + content
        )

    elif feature_name == "❓ Generate Quiz":

        return (
            "You are StudyMate AI, an educational quiz generator.\n\n"
            "TASK:\n"
            "Create a practice quiz using ONLY the study material provided.\n\n"
            "REQUIREMENTS:\n"
            "1. Generate exactly 5 multiple-choice questions.\n"
            "2. Every question must have four options: A, B, C, and D.\n"
            "3. Clearly identify the correct answer.\n"
            "4. Give a short explanation for every answer.\n"
            "5. Questions should test understanding.\n"
            "6. Do not use information that is not present in the study material.\n"
            "7. Keep the questions suitable for a student.\n\n"
            "STUDY MATERIAL:\n"
            + content
        )

    elif feature_name == "✍️ Improve Answer":

        return (
            "You are StudyMate AI, an academic writing assistant.\n\n"
            "TASK:\n"
            "Improve the student's answer while preserving its original meaning.\n\n"
            "OUTPUT FORMAT:\n\n"
            "## Improved Answer\n"
            "Write the improved answer here.\n\n"
            "## What Was Improved\n"
            "- Improvement 1\n"
            "- Improvement 2\n"
            "- Improvement 3\n\n"
            "## Study Tip\n"
            "Give one useful writing tip to the student.\n\n"
            "REQUIREMENTS:\n"
            "1. Improve grammar.\n"
            "2. Improve clarity.\n"
            "3. Improve sentence structure.\n"
            "4. Improve organization.\n"
            "5. Keep the original meaning.\n"
            "6. Do not invent unsupported facts.\n"
            "7. Use student-friendly language.\n\n"
            "STUDENT ANSWER:\n"
            + content
        )

    elif feature_name == "💡 Explain Concept":

        return (
            "You are StudyMate AI, a patient and friendly teacher.\n\n"
            "TASK:\n"
            "Explain the following concept or question so that a student "
            "can easily understand it.\n\n"
            "OUTPUT FORMAT:\n\n"
            "## Simple Definition\n"
            "Give a simple definition.\n\n"
            "## Step-by-Step Explanation\n"
            "Explain the concept step by step.\n\n"
            "## Real-World Example\n"
            "Give one simple real-world example or analogy.\n\n"
            "## Key Points to Remember\n"
            "Give exactly 3 important points.\n\n"
            "REQUIREMENTS:\n"
            "1. Use simple language.\n"
            "2. Avoid unnecessary technical jargon.\n"
            "3. If the input is a question, answer it directly.\n"
            "4. Make the explanation suitable for students.\n"
            "5. Do not make unsupported claims.\n\n"
            "TOPIC OR QUESTION:\n"
            + content
        )

    return content


# ============================================================
# INPUT PLACEHOLDERS
# ============================================================

placeholders = {
    "📝 Summarize Notes":
        "Paste your class notes or study material here...",

    "❓ Generate Quiz":
        "Paste your study material here to generate 5 MCQs...",

    "✍️ Improve Answer":
        "Paste your answer here and StudyMate AI will improve it...",

    "💡 Explain Concept":
        "Enter a difficult concept or question here..."
}


# ============================================================
# USER INPUT
# ============================================================

content = st.text_area(
    "📚 Enter Your Content",
    height=280,
    placeholder=placeholders[feature],
    help="Please enter at least 10 characters."
)


# ============================================================
# GENERATE BUTTON
# ============================================================

generate = st.button(
    "✨ Generate",
    type="primary"
)


# ============================================================
# AI GENERATION
# ============================================================

if generate:

    # --------------------------------------------------------
    # VALIDATE INPUT
    # --------------------------------------------------------

    cleaned_content = content.strip()

    if not cleaned_content:

        st.warning(
            "⚠️ Please enter some content before clicking Generate."
        )

        st.stop()

    if len(cleaned_content) < 10:

        st.warning(
            "⚠️ Please enter at least 10 characters."
        )

        st.stop()


    # --------------------------------------------------------
    # CHECK API KEY
    # --------------------------------------------------------

    if not gemini_api_key:

        st.error(
            "❌ Gemini API key is missing."
        )

        st.info(
            "Create .streamlit/secrets.toml and add "
            "GEMINI_API_KEY = \"YOUR_API_KEY\""
        )

        st.stop()


    # --------------------------------------------------------
    # CREATE GEMINI CLIENT
    # --------------------------------------------------------

    try:

        client = genai.Client(
            api_key=gemini_api_key
        )


        # ----------------------------------------------------
        # BUILD PROMPT
        # ----------------------------------------------------

        prompt = build_prompt(
            feature,
            cleaned_content
        )


        # ----------------------------------------------------
        # CALL GEMINI INTERACTIONS API
        # ----------------------------------------------------

        with st.spinner(
            "🤖 StudyMate AI is generating your answer..."
        ):

            interaction = client.interactions.create(
                model="gemini-3.6-flash",
                input=prompt,
                system_instruction=(
                    "You are StudyMate AI. "
                    "You are a helpful academic assistant. "
                    "Help students learn effectively. "
                    "Always be accurate, clear, concise, "
                    "student-friendly, and follow the requested "
                    "output structure. Do not invent information."
                )
            )


        # ----------------------------------------------------
        # GET AI RESPONSE
        # ----------------------------------------------------

        answer = getattr(
            interaction,
            "output_text",
            ""
        )


        # ----------------------------------------------------
        # CHECK EMPTY RESPONSE
        # ----------------------------------------------------

        if not answer or not answer.strip():

            st.error(
                "❌ Gemini returned an empty response. "
                "Please try again."
            )

            st.stop()


        # ----------------------------------------------------
        # DISPLAY RESPONSE
        # ----------------------------------------------------

        st.subheader(
            "✨ AI Generated Result"
        )

        st.markdown(
            '<div class="result-box">',
            unsafe_allow_html=True
        )

        st.markdown(
            answer
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        error_message = str(e)

        st.error(
            "❌ Something went wrong while contacting Gemini."
        )


        # ----------------------------------------------------
        # 404 MODEL ERROR
        # ----------------------------------------------------

        if "404" in error_message:

            st.warning(
                "The Gemini model is not available for this "
                "API key. Please check the models available "
                "for your Google AI Studio account."
            )


        # ----------------------------------------------------
        # 429 QUOTA ERROR
        # ----------------------------------------------------

        elif (
            "429" in error_message
            or "quota" in error_message.lower()
            or "resource exhausted" in error_message.lower()
        ):

            st.warning(
                "The Gemini API free-tier quota or rate limit "
                "has been reached. Please wait for the quota "
                "to reset and try again."
            )


        # ----------------------------------------------------
        # API KEY ERROR
        # ----------------------------------------------------

        elif (
            "401" in error_message
            or "403" in error_message
            or "api key" in error_message.lower()
            or "permission" in error_message.lower()
        ):

            st.warning(
                "Your Gemini API key may be invalid or may "
                "not have permission to use this model."
            )


        # ----------------------------------------------------
        # GENERAL ERROR
        # ----------------------------------------------------

        else:

            st.warning(
                "Please check your Gemini API key, internet "
                "connection, API availability, and try again."
            )


        # ----------------------------------------------------
        # TECHNICAL DETAILS
        # ----------------------------------------------------

        with st.expander(
            "🔧 Technical Details"
        ):

            st.code(
                error_message
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎓 StudyMate AI | Beginner AI Engineer Internship Project | "
    "Streamlit + Google Gemini API"
)