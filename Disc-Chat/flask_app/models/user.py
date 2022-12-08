from flask_app.config.mysqlconnection import connectToMySQL
import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app import app
from flask_app.models import course
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class User:
    db = "disc_chat"
    def __init__(self,data):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        self.user_name = data['user_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users ( email, password, user_name) VALUES(%(email)s,%(password)s, %(user_name)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) == 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['user_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if not results:
            return False
        else:
            return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM courses WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls((results[0]))

    @classmethod
    def get_from_courses(cls, data):
        query = "SELECT * FROM  users JOIN courses ON courses.user_id = users.id WHERE users.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        user = cls(results[0])
        if results[0]['courses.id'] == None:
            return user
        else:
            for row in results:
                db = {
                    'id': row['courses.id'],
                    'player': row['player'],
                    'score': row['score'],
                    'course_name': row['course_name'],
                    'comments' : row['comments'],
                    'discs' : row['discs'],
                    'user_id': row['user_id'],
                }
                user.courses.append(course.Course(db))
            return user