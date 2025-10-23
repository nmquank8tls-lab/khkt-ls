import os, json
from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import SECRET_KEY, FIREBASE_CREDENTIALS, OPENAI_API_KEY
from firebase_utils import init_firebase, save_assessment, get_user_doc, create_user_doc
from question_bank import SR, ER, EM
from ei_engine import score_sr, score_er, score_em, combine, classify, generate_ai_analysis
from auth_utils import init_firebase_admin, create_firebase_user, sign_in_with_email_and_password, login_user_session, logout_session, verify_id_token

app = Flask(__name__)
app.secret_key = SECRET_KEY

# initialize firebase admin (if service account present)
try:
    init_firebase(FIREBASE_CREDENTIALS)
except Exception as e:
    print('Firebase init warning:', e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        email = request.form.get('username').strip()
        password = request.form.get('password')
        full_name = request.form.get('full_name','')
        school_class = request.form.get('class','')
        # Create via Firebase Admin (server side) if possible
        res = create_firebase_user(email, password, display_name=full_name)
        if res.get('error'):
            flash('Đăng ký lỗi: ' + str(res.get('error')))
            return render_template('register.html')
        # create user doc in Firestore (profile)
        try:
            create_user_doc(res['uid'], {'email': email, 'full_name': full_name, 'class': school_class})
        except Exception as e:
            print('create_user_doc warning:', e)
        flash('Đăng ký thành công. Vui lòng đăng nhập.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get('username').strip()
        password = request.form.get('password')
        signin = sign_in_with_email_and_password(email, password)
        if signin.get('error'):
            flash('Đăng nhập thất bại: ' + str(signin.get('error')))
            return render_template('login.html')
        # save session
        login_user_session(session, signin)
        flash('Đăng nhập thành công.')
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_session(session)
    flash('Đã đăng xuất.')
    return redirect(url_for('index'))

@app.route('/test', methods=['GET','POST'])
def test():
    if request.method=='POST':
        answers = request.form.to_dict()
        sr_res = score_sr(answers)
        er_res = score_er(answers, ER)
        em_res = score_em(answers, EM)
        indices = combine(sr_res, er_res, em_res)
        classification = classify(indices)
        analysis = generate_ai_analysis(indices, sr_res, er_res, em_res)
        # save if firebase available and user logged in
        uid = session.get('uid') or 'anonymous'
        try:
            save_assessment(uid, answers, analysis)
        except Exception as e:
            print('Save failed:', e)
        return render_template('result.html', classification=classification, analysis=analysis.get('ai_analysis') or analysis.get('summary'))
    return render_template('test.html', SR=SR, ER=ER, EM=EM)

@app.route('/dashboard')
def dashboard():
    # If user is teacher (for demo we assume any logged-in user can view teacher page)
    uid = session.get('uid')
    # attempt to aggregate by class from Firestore if available
    classes_summary = []
    try:
        # This requires Firestore; collection 'users' and subcollections 'assessments'
        from firebase_admin import firestore
        db = firestore.client()
        users = db.collection('users').stream()
        class_map = {}
        for u in users:
            ud = u.to_dict()
            c = ud.get('class','Chưa xác định')
            # compute average of last assessment summary if exists
            class_map.setdefault(c, {'count':0, 'sum_avg':0.0})
            class_map[c]['count'] += 1
            # try to read last_assessment summary
            la = ud.get('last_assessment')
            if la and isinstance(la, dict):
                # try extract avg number from summary string (naive)
                import re
                s = la.get('summary','')
                m = re.search(r'([0-9]{1,3}\.?[0-9]*)', s)
                if m:
                    class_map[c]['sum_avg'] += float(m.group(1))
        for k,v in class_map.items():
            avg = v['sum_avg'] / v['count'] if v['count'] else 0.0
            classes_summary.append({'class':k, 'avg': round(avg,1), 'count': v['count']})
    except Exception as e:
        print('Aggregation warning:', e)
        # fallback demo data
        classes_summary = [{'class':'12H', 'avg':72.0, 'count':30}, {'class':'12T1','avg':58.0,'count':28}]
    demo_indices = {'Self-awareness':70.0,'Self-management':65.0,'Social-awareness':60.0,'Relationship-management':68.0}
    return render_template('dashboard.html', indices=demo_indices, classes_summary=classes_summary)

@app.route('/teacher')
def teacher():
    # teacher filter page - list classes and allow drilldown (demo)
    classes = []
    try:
        from firebase_admin import firestore
        db = firestore.client()
        users = db.collection('users').stream()
        s = set()
        for u in users:
            ud = u.to_dict()
            s.add(ud.get('class','Chưa xác định'))
        classes = [{'class':c} for c in s]
    except Exception as e:
        print('Teacher aggregation warning:', e)
        classes = [{'class':'12H'},{'class':'12T1'}]
    return render_template('teacher.html', classes=classes)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')
