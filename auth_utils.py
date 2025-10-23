import os
import requests
from firebase_admin import auth as fb_auth, initialize_app, credentials
from firebase_admin import exceptions as fb_exceptions
from flask import session

FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY','')  # required for REST sign-in
FIREBASE_CREDENTIALS = os.getenv('FIREBASE_CREDENTIALS','./serviceAccountKey.json')

def init_firebase_admin():
    try:
        if not len(fb_auth._get_current_app()):
            pass
    except Exception:
        pass
    try:
        cred = credentials.Certificate(FIREBASE_CREDENTIALS)
        initialize_app(cred)
    except Exception as e:
        # If already initialized or missing, ignore for demo
        print('Firebase admin init warning:', e)

def create_firebase_user(email, password, display_name=None):
    """Create user using Firebase Admin SDK (server side)."""
    try:
        user = fb_auth.create_user(email=email, password=password, display_name=display_name)
        return {'uid': user.uid, 'email': user.email}
    except fb_exceptions.FirebaseError as e:
        return {'error': str(e)}
    except Exception as e:
        return {'error': str(e)}

def sign_in_with_email_and_password(email, password):
    """Sign in using Firebase Auth REST API to get idToken."""
    if not FIREBASE_API_KEY:
        return {'error': 'FIREBASE_API_KEY not set in environment.'}
    url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}'
    payload = {'email': email, 'password': password, 'returnSecureToken': True}
    r = requests.post(url, json=payload)
    if r.status_code != 200:
        return {'error': r.json()}
    return r.json()

def verify_id_token(id_token):
    """Verify idToken using firebase_admin."""
    try:
        decoded = fb_auth.verify_id_token(id_token)
        return decoded
    except Exception as e:
        return {'error': str(e)}

def login_user_session(flask_session, id_token_response):
    """Save minimal info in Flask session from idToken response"""
    flask_session['idToken'] = id_token_response.get('idToken')
    flask_session['uid'] = id_token_response.get('localId')
    flask_session['email'] = id_token_response.get('email')
    return True

def logout_session(flask_session):
    flask_session.pop('idToken', None)
    flask_session.pop('uid', None)
    flask_session.pop('email', None)
    return True
