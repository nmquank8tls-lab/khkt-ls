import os
OPENAI_KEY = os.getenv('OPENAI_API_KEY','')
def score_sr(answers):
    total = sum(int(answers.get(f'sr{i}',3)) for i in range(1,11))
    return {'score': total, 'max':50, 'percent': total/50}
def score_er(answers, er_bank):
    correct = 0
    for item in er_bank:
        if answers.get(item['id']) == item.get('answer'):
            correct += 1
    total = len(er_bank)
    return {'correct': correct, 'total': total, 'percent': correct/total if total else 0}
def score_em(answers, em_bank):
    total = 0
    for item in em_bank:
        sel = answers.get(item['id'],'0')
        try: idx = int(sel); total += item.get('scores',[0])[idx]
        except: pass
    max_score = 2*len(em_bank)
    return {'score': total, 'max': max_score, 'percent': total/max_score if max_score else 0}
def combine(sr, er, em):
    sa = sr['percent']*100
    SA = 0.5*sa + 0.5*(er['percent']*100)
    SM = 0.6*sa + 0.4*(em['percent']*100)
    return {'Self-awareness': round(SA,1),'Self-management': round(SM,1),'Social-awareness': round(er['percent']*100,1),'Relationship-management': round(em['percent']*100,1)}
def classify(indices):
    avg = sum(indices.values())/len(indices)
    if avg>=85: label='Rất tốt'
    elif avg>=70: label='Tốt'
    elif avg>=50: label='Trung bình'
    elif avg>=35: label='Thấp'
    else: label='Cần hỗ trợ đặc biệt'
    return {'avg': round(avg,1), 'label': label}
def generate_ai_analysis(indices, sr, er, em):
    summary = f"Chỉ số trung bình: {classify(indices)['avg']} -> {classify(indices)['label']}"
    ai_text = None
    if OPENAI_KEY:
        try:
            import openai
            openai.api_key = OPENAI_KEY
            prompt = f"Dựa vào các chỉ số: {indices} và kết quả SR:{sr}, ER:{er}, EM:{em}, viết phân tích ngắn bằng tiếng Việt."
            resp = openai.ChatCompletion.create(model='gpt-4o-mini', messages=[{'role':'user','content':prompt}], max_tokens=300)
            ai_text = resp['choices'][0]['message']['content']
        except Exception as e:
            ai_text = f'OpenAI error: {e}'
    return {'summary': summary, 'ai_analysis': ai_text}
