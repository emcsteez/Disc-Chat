from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Course:
    db_name = 'disc_chat'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.player = db_data['player']
        self.score = db_data['score']
        self.course_name = db_data['course_name']
        self.comments = db_data['comments']
        self.discs = db_data['discs']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user = None

    @classmethod
    def save(cls,data):
        query = "INSERT INTO courses (player, score, course_name, comments, discs, user_id) VALUES (%(player)s,%(score)s,%(course_name)s, %(comments)s, %(discs)s,%(users_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE courses SET player=%(player)s, score=%(score)s, course_name=%(course_name)s, comments=%(comments)s, discs=%(discs)s updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM courses WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM courses WHERE courses.id = %(id)s; "
        results = connectToMySQL(cls).query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validate_courses(var):
        is_valid = True
        if len(var['player']) < 0:
            is_valid = False
            flash("player must be greater than 0","car")
        if len(var['comments']) < 0:
            is_valid = False
            flash("comments must be greater than 0","car")
        return is_valid

    @classmethod
    def get_from_courses(cls):
        query = "SELECT * FROM  courses LEFT JOIN users ON courses.user_id = users.id"
        results = connectToMySQL(cls.db_name).query_db(query)
        courses = []
        for row in results:
            this_course = cls(row)
            db = {
                'id': row['users.id'],
                'player': row['player'],
                'score': row['score'],
                'course_name': row['course_name'],
                'comments': row['comments'],
                'discs' : row ['discs'],
            }
            this_course.user = user.User(db)
        courses.append(this_course)
        return courses

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM courses;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        users_courses = []
        if len(results) < 0:
            return users_courses
        else:
            for row in results:
                users_courses.append(cls(row))
            return users_courses

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM courses WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls((results[0]))