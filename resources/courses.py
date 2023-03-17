from flask import request
from flask_smorest import Blueprint
from flask.views import MethodView
from models.courses import CourseModel
from db import db
from schemas.courses import CourseSchema
from models.courses import CourseStudentLinker
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("courses", "courses", url_prefix="", description="Operations on courses")

course_schema = CourseSchema()

@blp.route("/courses")
class Courses(MethodView):
    def get(self):
        all_courses = CourseModel.get_all_courses()
        results = course_schema.dump(all_courses, many=True)
        return results

    @jwt_required()
    def post(self):
        """Add a course"""
        new_course_data = request.get_json()
        Is_successful = CourseModel.add_course(new_course_data)
        if Is_successful:
            return "Course added successfully"
        else:
            return "Error adding course"
        
    
@blp.route("/courses/register")
class RegisterCourse(MethodView):
    @jwt_required()
    def post(self):
        access_token = get_jwt()
        registration_data = request.get_json()
        student_id = access_token["sub"]
        course_id = registration_data["course_id"]
        score = registration_data.get("score")

        registration = CourseStudentLinker(student_id=student_id, course_id=course_id, score=score)
    
        db.session.add(registration)
        db.session.commit()
        return "Course registration was successful"

@blp.route("/courses/<int:course_id>")
class GetCourse(MethodView):
    def get (self, course_id):
        """Get course"""
        course_data = CourseModel.get_by_id(course_id)
        query = course_schema.dump(course_data)
        students = course_data.student
        names = []
        for student in students:
            names.append(student.name)
        return names
        
 
    