import marshmallow as ma

from models.students import StudentsModel

class StudentSchema(ma.Schema):
    class Meta:
        model = StudentsModel
        load_instance = True

    id = ma.fields.Integer()
    name = ma.fields.String(required = True)
    email = ma.fields.String(required = True)
    password = ma.fields.String(required = True, dump_only= True)



    