import marshmallow as ma
from models.courses import CourseModel

class CourseSchema(ma.Schema):
    class Meta:
        model = CourseModel
        load_instance = True

    id = ma.fields.Integer()
    name = ma.fields.String(required = True)
    teacher = ma.fields.String(required = True)
    student_list = ma.fields.String(required = True)