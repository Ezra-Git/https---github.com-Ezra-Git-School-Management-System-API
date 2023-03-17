from db import db

class AdminModel(db.Model):
    __tablename__ = "Admins"
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable =False)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique = True)

    def __init__(self, new_admin_data) -> None:
        self.id = None
        self.name = new_admin_data["name"]
        self.password = new_admin_data["password"]
        self.email = new_admin_data["email"]

