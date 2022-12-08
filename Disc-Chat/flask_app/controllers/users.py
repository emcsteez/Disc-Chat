from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.course import Course
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "user_name": request.form['user_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/new/course')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/new/course')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    else:
        return render_template ("dashboard.html",user=User.get_by_id({"id": session ['user_id']}), courses=Course.get_from_courses())

@app.route("/user/<int:id>")
def show_user(id):
    return render_template("dashboard.html", user=User.get_by_id({"id": id}))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')