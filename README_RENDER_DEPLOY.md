# Render Deployment Guide for EI_WEB_APP_AI2_FINAL
This guide helps you deploy the project to Render (https://render.com) under the service name `khkt-lamson` and default AI language Tiếng Việt.

## Steps (summary)
1. Create a GitHub repository and push the project root (the contents of this folder).
2. Create a new Web Service on Render and connect your GitHub repo.
   - Name: khkt-lamson (or change as desired)
   - Branch: main (or your chosen branch)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python render_startup.py && gunicorn app_main:app --bind 0.0.0.0:$PORT`
3. In Render's service settings, add the following **Environment** variables (secure):
   - FIREBASE_CREDENTIALS_JSON -> paste full JSON text of your Firebase service account
   - FIREBASE_API_KEY -> your Firebase Web API key
   - OPENAI_API_KEY -> your OpenAI key (if using AI features)
   - SECRET_KEY -> a secure random string
   - DEFAULT_AI_LANG -> `vi`
4. Deploy. Render will build and run the app. Visit the public URL provided by Render.

## Notes
- The helper script `render_startup.py` writes `serviceAccountKey.json` from the env var at startup so you don't need to store the JSON file in Git.
- Do NOT commit secrets to GitHub.
- If you want me to finish the GitHub push and link to Render automatically, you'll need to grant access to a GitHub repo or invite me (not possible here). I will provide exact commands to run locally.
