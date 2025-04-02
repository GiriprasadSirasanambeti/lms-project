from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db

class AuthManager:
    @staticmethod
    def register(username, email, password, role='student'):
        if User.query.filter_by(username=username).first():
            return False
        user = User(username=username, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'), role=role)
        db.session.add(user)
        db.session.commit()
        return True

    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return True
        return False