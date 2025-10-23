import os, json
from pathlib import Path
# If FIREBASE_CREDENTIALS_JSON is present in env, write to serviceAccountKey.json
creds = os.getenv('FIREBASE_CREDENTIALS_JSON')
if creds:
    try:
        p = Path('./serviceAccountKey.json')
        p.write_text(creds)
        print('Wrote serviceAccountKey.json from FIREBASE_CREDENTIALS_JSON env var.')
    except Exception as e:
        print('Failed to write serviceAccountKey.json:', e)
# Set DEFAULT_AI_LANG fallback
DEFAULT_AI_LANG = os.getenv('DEFAULT_AI_LANG', 'vi')
print('DEFAULT_AI_LANG=', DEFAULT_AI_LANG)
