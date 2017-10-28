from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
import dbconfig
from user import User
from mockdbhelper import MockDBHelper as DBHelper
from passwordhelper import PasswordHelper

app = Flask(__name__)
app.secret_key='8XsrhOfJENLDehV4+cNv1+06qcd07khYRnq8HkULe1lKzcEOKgrrCNCgYz8Gh5uWBloEhYHetI9Zq+CMM+co2QCbDGvP/juPbWu'
login_manager = LoginManager(app)
DB = DBHelper()
PH = PasswordHelper()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=["POST"])
def login():
    email=request.form.get('user')
    user_password=request.form.get('password')
    user=DB.get_user(email)
    if user and PH.validate_password(user_password, user['salt'],user['hashed']) :
        user = User(email)
        login_user(user)
        return redirect(url_for('account'))
    return home()

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/register', methods=['POST'])
def register():
    email=request.form.get('email')
    pw1=request.form.get('password')
    pw2=request.form.get('con-password')
    if not pw1 == pw2:
        return redirect(url_for('home'))
    if DB.get_user(email):
        return redirect(url_for('home'))
    salt=PH.get_salt()
    hashed=PH.get_hash(pw1+salt)
    DB.add_user(email,salt,hashed)
    return redirect(url_for('home'))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/account")
@login_required
def account():
    tables = DB.get_tables(current_user.get_id())
    return render_template("account.html", tables=tables)

@app.route("/account/createtable", methods=["POST"])
@login_required
def account_createtable():
    tablename = request.form.get("tablenumber")
    tableid = DB.add_table(tablename, current_user.get_id())
    new_url = dbconfig.base_url + "newrequest/" + tableid
    DB.update_table(tableid, new_url)
    return redirect(url_for('account'))

@app.route("/account/deletetable")
@login_required
def account_deletetable():
    tableid = request.args.get("tableid")
    DB.delete_table(tableid)
    return redirect(url_for('account'))

@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)    

if __name__ == '__main__':
    app.run(port=5000, debug=True)