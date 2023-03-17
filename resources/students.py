from flask import request, make_response
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from models.students import StudentsModel
from db import db
from passlib.hash import pbkdf2_sha256
from schemas.students import StudentSchema
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_access_cookies, get_jwt
from models.courses import CourseStudentLinker

blp = Blueprint("students", "students", url_prefix="/students", description="Operations on students")

student_schema = StudentSchema()


@blp.route("/")
class Students(MethodView):
    def get(self):
        """List students"""
        all_students = StudentsModel.get_all_students()
        results = student_schema.dump(all_students, many=True)
        return results

    def post(self):
        """Add a new student"""
        new_student_data = request.get_json()
        Is_successful = StudentsModel.create_student(new_student_data)
        if Is_successful:
            return "Student profile was created successfully."
        else:
            return "Error creating student profile."

# Add student profile endpoint?
@blp.route("/<int:student_id>")
class StudentsById(MethodView):
    def get(self, student_id):
        """Get student data"""
        student_data = StudentsModel.get_by_id(student_id)
        query = student_schema.dump(student_data)
        return query
    
    @jwt_required()
    def patch(self, student_id):
        access_token = get_jwt()
        if access_token["admin"] is False:
            return "You are not authorized to update student information"
        new_student_data = request.get_json()
        student_data = db.get_or_404(StudentsModel, student_id)
        if "name" in new_student_data:
            student_data.name = new_student_data["name"]
        if "password" in new_student_data:
            student_data.password = new_student_data["password"]

        db.session.commit()
        return "Student updated successfully"
    
    @jwt_required()
    def delete(self, student_id):
        access_token = get_jwt()
        if access_token["admin"] is False:
            return "You are not authorized to delete student information"
        student_data = db.get_or_404(StudentsModel, student_id)
        db.session.delete(student_data)
        db.session.commit()
        return "Student deleted successfully"
    
@blp.route("/<int:student_id>/courses/<int:course_id>")
class StudentScorebyId(MethodView):
    @jwt_required()
    def get(self, student_id, course_id):
        access_token = get_jwt()
        if access_token["admin"] is False:
            return "You are not authorized to retrieve student information"
        """Get student score for specific course"""
        student_score = db.session.execute(db.select(CourseStudentLinker.score)
                           .where(CourseStudentLinker.student_id==student_id, 
                                  CourseStudentLinker.course_id==course_id)).scalars()
        return student_score
    
@blp.route("/<int:student_id>/scores")
class GetStudentGPA(MethodView):
    @jwt_required()
    def get(self, student_id):
        access_token = get_jwt()
        if access_token["admin"] is False:
            return "You are not authorized to view student information"
        """Get GPA for a particular student"""
        student_score = db.session.execute(db.select(CourseStudentLinker.score)
                           .where(CourseStudentLinker.student_id==student_id)).scalars()
        total_units = 0
        number_of_courses = 0
        grade_to_unit = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0}

        for score in student_score:
            if score == "":
                continue
            else:
                unit = grade_to_unit[score]
                total_units += unit
                number_of_courses += 1

        cgpa = total_units/number_of_courses
        return round(cgpa, 2)
    
@blp.route("/signup")
class Signup(MethodView):
    def post(self):
        """Student Signup"""
        student_data = request.get_json()
        if StudentsModel.query.filter(StudentsModel.email == student_data["email"]):
            abort(409, message="Error creating profile.")

        hashed_password = pbkdf2_sha256.hash(student_data["password"])
        student_signup = StudentsModel(
            name = student_data["name"],
            password = hashed_password,
            email = student_data["email"]
        )
        db.session.add(student_signup)
        db.session.commit()

        return "student profile created successfully."
    
@blp.route("/login")
class Login(MethodView):
    def post(self):
        """Student Login"""
        student_data = request.get_json()
        hashed_password = pbkdf2_sha256.hash(student_data["password"])
        student = StudentsModel.query.filter(StudentsModel.email == student_data["email"], 
                                             StudentsModel.password == hashed_password)
        if student:
            additional_claims = {"admin": False}
            access_token = create_access_token(student.id, additional_claims=additional_claims)
            response = make_response("Student logged in")
            set_access_cookies(response, access_token)
            return response
        else:
            return "Login failed"
        
