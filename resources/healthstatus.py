from flask_smorest import Blueprint
from flask.views import MethodView


blp = Blueprint("base_URL", "base_URL", url_prefix="/", description="Base URL operations")

@blp.route("/")
class HealthStatus(MethodView):
    def get(self):
        return "Hello World, Hi there"
    
    
