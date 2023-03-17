from flask import request, make_response
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from models.admin import AdminModel
from flask_jwt_extended import create_access_token, set_access_cookies, unset_access_cookies
from passlib.hash import pbkdf2_sha256
from db import db


blp = Blueprint("admin", "admin", url_prefix="/admin", description="Operations on admin")


@blp.route("/signup")
class AdminSignup(MethodView):
    def post(self):
        """Admin Signup"""
        admin_data = request.get_json()
        if AdminModel.query.filter(AdminModel.email == admin_data["email"]):
            abort(409, message="Error creating profile.")

        hashed_password = pbkdf2_sha256.hash(admin_data["password"])
        admin_signup = AdminModel(
            name = admin_data["name"],
            password = hashed_password,
            email = admin_data["email"]
        )
        db.session.add(admin_signup)
        db.session.commit()

        return "Admin profile created successfully."
    
@blp.route("/login")
class AdminLogin(MethodView):
    def post(self):
        """Admin Login"""
        admin_data = request.get_json()
        hashed_password = pbkdf2_sha256.hash(admin_data["password"])
        admin = AdminModel.query.filter(AdminModel.email == admin_data["email"], 
                                             AdminModel.password == hashed_password)
        if admin:
            additional_claims = {"admin": True}
            access_token = create_access_token(admin.id, additional_claims=additional_claims)
            response = make_response("Admin logged in")
            set_access_cookies(response, access_token)
            print(access_token)
            return response
        else:
            return "Login failed"

        
        
@blp.route("/logout")
class Signup(MethodView):
    def post(self):
        """Admin Logout"""
        response = "Logout successful"
        unset_access_cookies(response)
        return response
