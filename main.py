from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'xavesecreta'

lm = LoginManager()
lm.init_app(app)

USERNAME = 'adm'
PASSWORD = '1234'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@lm.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('homeauth.html')
    else:
        return render_template('homenotauth.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            user = User(id=username)
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('invalid.html')
    return render_template('login.html')       

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
