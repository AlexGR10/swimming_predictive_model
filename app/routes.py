from flask import jsonify, request, current_app as app
from app.services.auth_service import login_user, register_user, update_profile, get_user_data
from app.utils.mongo import get_db

def register_routes(app):
    @app.route('/')
    def index():
        return jsonify("Welcome to the Flask API!")

    @app.route('/collections', methods=['GET'])
    def list_collections():
        db = get_db()
        colecciones = db.list_collection_names()
        return jsonify({"collections": colecciones})

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('user')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        response, status_code = login_user(username, password)
        return jsonify(response), status_code

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        user = data.get('user')
        nombre = data.get('nombre')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        gender = data.get('gender')
        height_cm = data.get('height_cm')
        weight_kg = data.get('weight_kg')
        competition_time_s = data.get('competition_time_s')
        current_age = data.get('current_age')
        competition_years = data.get('competition_years')
        best_time_s = data.get('best_time_s')
        imc = data.get('imc')
        training_hours_week = data.get('training_hours_week')

        # Verificar que todos los campos estén presentes y no vacíos
        if not all([user, nombre, email, password, confirm_password, gender, height_cm, weight_kg, competition_time_s, current_age, competition_years, best_time_s, imc, training_hours_week]):
            return jsonify({"error": "All fields are required"}), 400

        response, status_code = register_user(user, nombre, email, password, confirm_password, gender, height_cm, weight_kg, competition_time_s, current_age, competition_years, best_time_s, imc, training_hours_week)
        return jsonify(response), status_code

    @app.route('/edit_profile', methods=['POST'])
    def edit_profile():
        data = request.get_json()
        username = data.get('user')
        updates = data.get('updates')

        if not username or not updates:
            return jsonify({"error": "Missing username or updates"}), 400

        response, status_code = update_profile(username, updates)
        return jsonify(response), status_code

    @app.route('/predict', methods=['POST'])
    def predict():
        data = request.get_json()
        username = data.get('user')

        if not username:
            return jsonify({"error": "Missing username"}), 400

        response, status_code = get_user_data(username)
        return jsonify(response), status_code
