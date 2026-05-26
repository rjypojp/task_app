from flask import session



def require_login():
    
    if "user" not in session:
        return None
    
    return session["user"]

def validate_task(title, comment):
    
    if not title:
        return "タイトルを入力してください。"
    
    if len(title) > 100:
        return "タイトルは100字以内です。"
    
    if len(comment) > 500:
        return "コメントは500字以内です。"
    
    return None
