from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.course import Course
from flask_app.models.user import User


@app.route('/new/course')
def new_show():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_course.html',user=User.get_by_id(data))

@app.route('/create/course',methods=['POST'])
def create_course():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Course.validate_course(request.form):
        return redirect('/new/car')
    data = {
        "player": request.form["player"],
        "score": request.form["score"],
        "course_name": request.form["course_name"],
        "comments": request.form["comments"],
        "discs": request.form["discs"],
        "user_id": session["user_id"]
    }
    Course.save(data)
    return redirect('/dashboard')

@app.route('/course/<int:id>')
def get_from_course(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("course_info.html",user=User.get_by_id(user_data))


@app.route('/destroy/course/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Course.destroy(data)
    return redirect('/dashboard')

@app.route('/edit/course/<int:id>')
def edit_course(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_course.html",cars=Course.get_one(data),user=User.get_by_id(user_data))

@app.route('/course/<int:id>')
def show_course(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("course_info.html",this_car=Course.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/course',methods=['POST'])
def update_course():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Course.validate_course(request.form):
        return redirect('/new/course')
    data = {
        "player": request.form["player"],
        "score": request.form["score"],
        "course_name": request.form["course_name"],
        "comments": request.form["comments"],
        "discs": request.form["discs"],
        "user_id": session["user_id"]
    }
    Course.update(data)
    return redirect('/dashboard')