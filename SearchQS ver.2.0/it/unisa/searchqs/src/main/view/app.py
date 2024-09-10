import sys
sys.path.append("../../..")

import secrets
from flask import Flask, render_template, request, redirect, url_for, session

from src.main.view.authentication_view import authentication_bp
from src.main.view.user_area_view import user_area_bp
from src.main.view.analysis_view import analysis_bp
'''
'''

app = Flask(__name__, template_folder='../template', static_folder='../static')
app.secret_key = secrets.token_hex(16)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

app.register_blueprint(authentication_bp)
app.register_blueprint(user_area_bp)
app.register_blueprint(analysis_bp)
'''
'''

if __name__ == "__main__":
    app.run(host='0.0.0.0')








