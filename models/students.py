from passlib.hash import pbkdf2_sha256
from db import db


class StudentsModel(db.Model):
    __tablename__ = "students"
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable =False)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique = True)
    course = db.relationship("CourseModel", back_populates='student', secondary='registration')

    def __init__(self, new_student_data) -> None:
        self.id = None
        self.name = new_student_data["name"]
        self.password = new_student_data["password"]
        self.email = new_student_data["email"]


    @classmethod
    def get_all_students(cls):
        print(cls.query.all())
        return cls.query.all()
       
       
    @classmethod
    def get_by_id(cls, id):
        student_data = db.get_or_404(StudentsModel, id)
        return (student_data)
    

    @classmethod
    def update_student(cls, id):
        student_data = db.get_or_404(StudentsModel, id)
        student_data.name = ""
        db.session.commit()
        return "Student updated successfully"
    
    @classmethod
    def delete_student(cls, id):
        student_data = db.get_or_404(StudentsModel, id)
        db.session.delete(student_data)
        db.session.commit()
        return "Student deleted successfully"

    @classmethod
    def create_student(cls, new_student_data):
        if "name" not in new_student_data:
            return False
        if "email" not in new_student_data:
            return False
        if StudentsModel.query.filter(StudentsModel.email == new_student_data["email"]).first():
            return False

        hashed_password = pbkdf2_sha256.hash(new_student_data["password"])
        student_signup = StudentsModel({
            "name" : new_student_data["name"],
            "password" : hashed_password,
            "email" : new_student_data["email"]
        })
        db.session.add(student_signup)
        db.session.commit()

        # student_entry = cls(new_student_data)
        # db.session.add(student_entry)
        # db.session.commit()
        return True


