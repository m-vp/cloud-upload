from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
import os

app = Flask(__name__)
CORS(app)

# AWS RDS PostgreSQL Configuration
DB_USER = "admin123"
DB_PASSWORD = "admin123"
DB_HOST = "reg1.ce2bp6jj4rwp.us-east-1.rds.amazonaws.com"  # Replace with actual RDS endpoint
DB_NAME = "reg1"

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "supersecretkey"

db = SQLAlchemy(app)
jwt = JWTManager(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Initialize Database
@app.before_first_request
def create_tables():
    db.create_all()

# Register Route
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    new_user = User(username=data["username"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# Login Route
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and user.password == data["password"]:
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token})
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
