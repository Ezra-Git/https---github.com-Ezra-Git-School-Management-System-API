from db import db

class CourseStudentLinker(db.Model):
    __tablename__ = "registration"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    score = db.Column(db.String(3), nullable=True)

class CourseModel(db.Model):
    __tablename__ = "courses"
    name = db.Column(db.String(50), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.String(50), nullable=False)
    student = db.relationship("StudentsModel", back_populates='course', secondary='registration')

    def __init__(self, new_course_data) -> None:
        self.id = None
        self.name = new_course_data["course name"]
        self.teacher = new_course_data["teacher"]
    

    @classmethod
    def get_all_courses(cls):
        print(cls.query.all())
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        course_data = db.get_or_404(CourseModel, id)
        return (course_data)
    

    @classmethod
    def update_course(cls, id):
        update_course = db.get_or_404(CourseModel, id)
        update_course.name = ""
        db.session.commit()
        return "Course updated successfully"
    
    @classmethod
    def delete_course(cls, id):
        course_data = db.get_or_404(CourseModel, id)
        db.session.delete(course_data)
        db.session.commit()
        return "Course deleted successfully"

    @classmethod
    def add_course(cls, new_course_data):
        if "course name" not in new_course_data:
            return False
        
        course_entry = cls(new_course_data)
        db.session.add(course_entry)
        db.session.commit()
        return True