import firebase_admin
from firebase_admin import credentials, firestore
import os, datetime
db = None
def init_firebase(path=None):
    global db
    if firebase_admin._apps:
        db = firestore.client(); return
    p = path or os.getenv('FIREBASE_CREDENTIALS')
    cred = credentials.Certificate(p)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
def create_user_doc(uid, data):
    global db
    db.collection('users').document(uid).set(data)
def get_user_doc(uid):
    global db
    doc = db.collection('users').document(uid).get()
    if doc.exists: return doc.to_dict()
    return None
def save_assessment(uid, answers, analysis):
    global db
    coll = db.collection('users').document(uid).collection('assessments')
    coll.add({'timestamp': datetime.datetime.utcnow(), 'answers': answers, 'analysis': analysis})
