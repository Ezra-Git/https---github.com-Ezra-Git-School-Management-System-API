import flask
from flask_jwt_extended import JWTManager


from flask_smorest import Api

import marshmallow

from resources.healthstatus import blp as health_blp
from resources.students import blp as students_blp
from resources.courses import blp as courses_blp
from resources.admin import blp as admin_blp

from db import db
from models.students import StudentsModel
from models.courses import CourseModel

app = flask.Flask (__name__, instance_relative_config=True)
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"

api = Api(app)
jwt = JWTManager(app)
db.init_app(app)

api.register_blueprint(health_blp)
api.register_blueprint(students_blp)
api.register_blueprint(courses_blp)
api.register_blueprint(admin_blp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)