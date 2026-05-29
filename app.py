import os
from datetime import date

from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS

from config import Config
from models import db
from models.user import User
from models.food import FoodItem, FoodLog
from models.health import HealthLog, Reminder
from models.diet import DietPlan, DiseaseDietRule

from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.food_routes import food_bp
from routes.health_routes import health_bp
from routes.diet_routes import diet_bp
from routes.chatbot_routes import chatbot_bp

migrate = Migrate()

# Temporary in-memory water tracker storage
# Key format: "<user_id>_<YYYY-MM-DD>"
water_tracker_store = {}


def get_today_water_tracker(user_id):
    today_key = f"{user_id}_{date.today().isoformat()}"

    if today_key not in water_tracker_store:
        water_tracker_store[today_key] = {
            "current_intake": 0,
            "goal": 2000,
            "date": date.today().isoformat()
        }

    return water_tracker_store[today_key]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["REPORT_FOLDER"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)
    CORS(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(food_bp, url_prefix="/food")
    app.register_blueprint(health_bp, url_prefix="/health")
    app.register_blueprint(diet_bp, url_prefix="/diet")
    app.register_blueprint(chatbot_bp, url_prefix="/chatbot")

    @app.route("/")
    def home():
        return render_template("login.html")

    @app.route("/register-page")
    def register_page():
        return render_template("register.html")

    @app.route("/dashboard-page")
    def dashboard_page():
        return render_template("dashboard.html")

    @app.route("/profile-page")
    def profile_page():
        return render_template("profile.html")

    @app.route("/food-scan-page")
    def food_scan_page():
        return render_template("food_scan.html")

    @app.route("/diet-page")
    def diet_page():
        return render_template("diet_plan.html")

    @app.route("/health-page")
    def health_page():
        return render_template("health_monitor.html")

    @app.route("/chatbot-page")
    def chatbot_page():
        return render_template("chatbot.html")

    # ------------------------------------------------------------------
    # Water Tracker Routes
    # ------------------------------------------------------------------

    @app.route("/water-tracker", methods=["GET"])
    @jwt_required()
    def get_water_tracker():
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        tracker = get_today_water_tracker(user_id)
        return jsonify(tracker), 200

    @app.route("/water-tracker/add", methods=["POST"])
    @jwt_required()
    def add_water_tracker():
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json(silent=True) or {}
        amount = data.get("amount")

        if amount is None:
            return jsonify({"error": "Water amount is required"}), 400

        try:
            amount = int(amount)
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid water amount"}), 400

        if amount <= 0:
            return jsonify({"error": "Water amount must be greater than 0"}), 400

        tracker = get_today_water_tracker(user_id)
        tracker["current_intake"] += amount

        return jsonify({
            "message": f"{amount} ml water added successfully.",
            "tracker": tracker
        }), 200

    @app.route("/water-tracker/reset", methods=["POST"])
    @jwt_required()
    def reset_water_tracker():
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        tracker = get_today_water_tracker(user_id)
        tracker["current_intake"] = 0

        return jsonify({
            "message": "Water tracker reset successfully.",
            "tracker": tracker
        }), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)