# 🎓 StudyMate AI — Gemini Edition

StudyMate AI is a beginner-level AI Engineer internship project built with **Python, Streamlit, and the Google Gemini API**.

It provides four focused student utilities:

- 📝 Summarize Notes
- ❓ Generate Quiz
- ✍️ Improve Answer
- 💡 Explain Concept

## Why Gemini?

This version uses the Google Gemini Developer API instead of OpenAI. Google currently lists a free tier for models including `gemini-2.5-flash`, although free-tier rate limits and availability can change. Check Google's current pricing page before deployment.

Official documentation:
- Google AI Studio / Gemini API
- Gemini API pricing
- Gemini Python SDK

## 1. Problem

Students frequently work with lengthy notes, difficult concepts, and draft answers. They need quick tools to revise material, test their understanding, and improve their responses.

## 2. Solution

StudyMate AI converts a student's input into a useful, structured study result using an LLM. Instead of being a generic chatbot, each feature has a dedicated prompt and output format.

## 3. AI Workflow

```text
User Input
    ↓
Input Validation
    ↓
Feature Selection
    ↓
Structured Prompt Construction
    ↓
Gemini API
    ↓
Response Validation
    ↓
Readable AI Output
```

## 4. Prompt Design

Each feature uses a structured prompt containing:

- Role
- Task
- Output requirements
- Constraints
- User content

This makes the output more consistent and relevant than sending a generic chatbot instruction.

## 5. Validation and Error Handling

The app handles:

- Empty input
- Very short input
- Missing Gemini API key
- API failures
- Free-tier quota/rate-limit errors
- Empty model responses

## 6. Project Structure

```text
StudyMate_AI_Gemini/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```

## 7. Run Locally in VS Code

### Step 1: Open the project

Extract the ZIP and open the `StudyMate_AI_Gemini` folder in VS Code.

### Step 2: Create/activate virtual environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If your existing virtual environment is already activated, you can skip this step.

### Step 3: Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Create the secrets file

Inside the project folder create:

```text
.streamlit
└── secrets.toml
```

Put:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Do not upload this file to GitHub. It is already included in `.gitignore`.

### Step 5: Start the app

```powershell
streamlit run app.py
```

Open the displayed local URL, normally:

```text
http://localhost:8501
```

## 8. Get a Gemini API Key

Use Google AI Studio and create a Gemini API key.

Google's official getting-started documentation explains that Google AI Studio can create an API key for new users. Free-tier usage is available for supported models, subject to rate limits and quota.

Never publish the API key in GitHub or inside `app.py`.

## 9. Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
   - `.env.example`
3. Do NOT upload `.streamlit/secrets.toml`.
4. Create the Streamlit app using `app.py`.
5. Open the Streamlit app settings.
6. Add this secret:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

7. Deploy/reboot the app.

## 10. Submission Explanation

### How does the app work?

The user selects a study utility and provides content. The application validates the input, builds a feature-specific structured prompt, sends it to Gemini, validates the response, and displays the generated result.

### Why is it not just a generic chatbot?

The application is designed around four concrete student workflows. Each workflow has a different prompt, requirements, and output structure.

### What prompt engineering was used?

Prompts specify the AI's role, task, expected output, constraints, and user content. This improves consistency and keeps responses aligned with the selected student utility.

### What happens when the API fails?

The application catches runtime/API exceptions and displays a clear message instead of crashing. Quota/rate-limit errors are also explained to the user.

## 11. Future Improvements

- PDF note upload
- Persistent study history
- Flashcard generation
- Difficulty levels for quizzes
- Quiz scoring
- User authentication
- Subject-wise study dashboard
