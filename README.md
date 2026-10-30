# Technical Seminar Preparation Kit

A local Streamlit application. Enter a seminar topic, choose an AI provider, and generate a Markdown seminar pack.

## Supported providers

- OpenAI
- Groq
- Anthropic Claude

The application uses provider APIs directly. You need a valid API key and model access for the provider you select. Model names and availability can change; edit the Model field in the sidebar if needed.

## Generated output

The kit asks the model to prepare:
- Abstract and learning objectives
- Prerequisites and timed agenda
- Detailed seminar content
- Slide-by-slide plan with visual suggestions
- Speaker notes
- Practical demo or case study
- Audience activity and FAQs
- Conclusion and references to verify

The model may make mistakes. Verify technical claims, code, statistics, and references before presenting. The app does not independently fact-check generated content.

## Setup (Windows)

1. Install Python 3.10 or newer.
2. Extract this ZIP file.
3. Open a terminal in the extracted folder.
4. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

6. Copy `.env.example` to `.env`.
7. Add at least one API key to `.env`:
   - `OPENAI_API_KEY`
   - `GROQ_API_KEY`
   - `ANTHROPIC_API_KEY`

8. Start the app:

   ```powershell
   streamlit run app.py
   ```

9. Open the local URL printed in the terminal (usually `http://localhost:8501`).

## Setup (macOS / Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your provider API key(s)
streamlit run app.py
```

## Security notes

- API keys are loaded from your local `.env` file and are not displayed in the interface.
- Do not upload your `.env` file, publish it, or commit it to source control.
- API usage may incur charges under the provider's pricing and account limits.
- This starter app sends the topic and prompt to the selected provider's API.

## Customize

- Add or change model IDs in the sidebar defaults in `app.py`.
- Edit the output structure in `build_prompt()` in `seminar_generator.py`.
- Add another provider by implementing its API call in `generate_seminar()`.

## Troubleshooting

- `..._API_KEY is missing`: check the spelling and location of `.env`, then restart Streamlit.
- Authentication error: confirm the key is valid, active, and belongs to the selected provider.
- Model not found / unavailable: enter a model ID enabled for your account.
- Rate limit or quota error: check provider billing, quota, and rate limits.
