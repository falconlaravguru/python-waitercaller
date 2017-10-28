from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
import dbconfig
from user import User
from mockdbhelper import MockDBHelper as DBHelper

app = Flask(__name__)
app.secret_key='8XsrhOfJENLDehV4+cNv1+06qcd07khYRnq8HkULe1lKzcEOKgrrCNCgYz8Gh5uWBloEhYHetI9Zq+CMM+co2QCbDGvP/juPbWu'
login_manager = LoginManager(app)
DB = DBHelper()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/account')
@login_required
def account():
    return "You are logged in"

@app.route('/login', methods=["POST"])
def login():
    email=request.form.get('user')
    user_password=request.form.get('password')
    db_password=DB.get_user(email)
    if db_password and db_password == user_password:
        user = User(email)
        login_user(user)
        return redirect(url_for('account'))
    return home()

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)    

if __name__ == '__main__':
    app.run(port=5000, debug=True)