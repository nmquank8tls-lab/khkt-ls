# EI_WEB_APP_AI2_FINAL (UI-B, Firebase Auth, OpenAI)

This repository contains the student project **AI EI Assistant** — a Flask web app to assess Emotional Intelligence (EI),
store results in Firebase, and provide AI-powered reflections using OpenAI (optional).

## Features (added)
- Firebase Email/Password Authentication (create user via Admin, sign-in via REST)
- Firestore storage for user profiles and assessments
- Teacher view: filter / aggregate results by class
- AI Reflection (OpenAI) integration placeholder
- Dockerfile to run app in container
- UI-B: Dashboard with Radar chart + table + class summaries

## Quick start (local)
1. Create Python 3.10 venv and activate
2. Install requirements: `pip install -r requirements.txt`
3. Add your Firebase service account JSON as `serviceAccountKey.json` or update `config.py`
4. Export environment variables (Linux/macOS):
```bash
export FIREBASE_CREDENTIALS=./serviceAccountKey.json
export FIREBASE_API_KEY=YOUR_FIREBASE_WEB_API_KEY
export OPENAI_API_KEY=sk-...
```
On Windows use `set` instead of `export`.

5. Run the app:
```bash
python app_main.py
```

6. Open `http://127.0.0.1:5000`

## Docker
Build and run the container:
```bash
docker build -t ei_app:latest .
docker run -p 5000:5000 -e FIREBASE_CREDENTIALS=/app/serviceAccountKey.json -e FIREBASE_API_KEY=YOUR_API_KEY -e OPENAI_API_KEY=sk-... ei_app:latest
```

## Screenshots
Screenshots are in `static/screenshots/` (placeholders). You can replace them with real screenshots after running the app.

## Notes
- For security, do not commit your serviceAccountKey.json or API keys to a public repo.
- The project includes demo fallback behavior so you can run the app without Firebase for UI testing.
