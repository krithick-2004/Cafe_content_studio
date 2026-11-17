# Brew Studio – AI Creative Studio

Brew Studio is a multimodal AI creative studio that helps turn an initial idea into a structured creative brief. It accepts different types of input and uses AI to organise the information into a clear concept that can guide creative work.

## Features

- **Text input:** describe an idea in your own words.
- **Voice input:** use a voice transcript as part of the creative brief.
- **PDF input:** include content extracted from a PDF.
- **Reference image analysis:** use information from a reference image to guide the brief.
- **Structured AI output:** generate a validated creative brief containing:
  - Name
  - Tagline
  - Concept
  - Mood
  - Visual style
  - Target audience
  - Key features
- **Creative history:** the frontend includes a recent-creations/history experience.
- **Image workflows:** the frontend includes image generation and image-variation workflows.

> Note: Available workflows depend on the corresponding backend routes, services, API credentials, and configuration being set up.

## Tech Stack

- **Backend:** Python, FastAPI
- **AI integration:** Groq API
- **Model:** `openai/gpt-oss-120b`
- **Frontend:** HTML, CSS, JavaScript
- **Configuration:** environment variables using a `.env` file

## Project Structure

```text
Ai-content_studio/
├── backend/
│   ├── models/          # Data models and schemas
│   ├── routes/          # API route handlers
│   ├── services/        # Application and AI services
│   └── main.py          # FastAPI application entry point
├── frontend/
│   └── index.html       # Frontend application
├── .env                # Local secrets (not committed)
├── .gitignore
├── README.md
├── requirements.txt
└── test_groq.py         # Groq API test script
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/krithick-2004/brew-studio-ai.git
cd brew-studio-ai
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get an API key from the [Groq Console](https://console.groq.com/). Keep the key private. Never commit your `.env` file or paste your API key into source code.

### 5. Run the backend

From the project root, run:

```bash
uvicorn backend.main:app --reload
```

If your FastAPI instance or module uses a different name, adjust the command to match the application entry point in `backend/main.py`.

### 6. Open the frontend

Open `frontend/index.html` in your browser, or serve the frontend using your preferred local development server. Make sure the frontend's API base URL matches the address where the backend is running.

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key used to access the Groq model |

## API and Model

The backend uses the Groq API with the `openai/gpt-oss-120b` model to generate structured creative-brief output. The expected brief fields are defined by the project's `CreativeBrief` schema.

## Development Notes

- Keep credentials and other secrets in your local `.env` file.
- Update `requirements.txt` when adding or changing Python dependencies.
- Keep frontend API endpoints in sync with the backend routes.
- Add screenshots or a demo GIF to this README when you are ready to showcase the interface.

## Future Improvements

- Add example outputs and project screenshots.
- Expand creative brief templates for different industries and use cases.
- Improve validation and error handling for uploaded files and AI responses.

## Author

**Krithick**  
GitHub: [@krithick-2004](https://github.com/krithick-2004)

---

If you find this project interesting, feel free to explore the code and share feedback.
"# Cafe_content_studio" 
