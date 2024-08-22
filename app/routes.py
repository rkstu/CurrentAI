# from flask import Blueprint, jsonify, render_template, request
# from .models import TiDBDatabaseComponent
# from .utils import save_query_and_response, queries_and_response, clear_queries

# api_bp = Blueprint('api_bp', __name__, template_folder='templates')

# # Initialize the database component
# db_component = TiDBDatabaseComponent()

# @api_bp.route('/')
# def welcome():
#     return render_template('index.html')

# @api_bp.route('/generate_id', methods=['GET'])
# def generate_id():
#     user_id = db_component.generate_user_id()
#     return jsonify({"token": user_id}), 201

# @api_bp.route('/get_user_id_by_email/<email>', methods=['GET'])
# def get_user_id_by_email(email):
#     user_id = db_component.get_user_id_by_email(email)
#     return jsonify({"token": user_id}), 201

# @api_bp.route('/add_user/<email>/<password>/<first_name>/<last_name>', methods=['POST'])
# def add_user(email, password, first_name, last_name):
#     user_id = db_component.add_user(email, password, first_name, last_name)
#     return jsonify({"userId": user_id}), 201

# @api_bp.route('/add_queries/<userId>', methods=['POST']) 
# def add_queries(userId):
#     db_component.add_queries(userId)
#     clear_queries()
#     return jsonify({"status": "success"}), 200

# @api_bp.route('/user_exists/<email>/<password>', methods=['GET'])
# def user_exists(email, password):
#     exists = db_component.user_exists(email, password)
#     return jsonify({"exists": exists}), 200

# @api_bp.route('/get_user_queries/<userId>', methods=['GET'])
# def get_user_queries(userId):
#     queries = db_component.get_user_queries(userId)
#     return jsonify(queries), 200

# @api_bp.route('/update_user_password/<userId>/<new_password>', methods=['POST'])
# def update_user_password(userId, new_password):
#     db_component.update_user_password(userId, new_password)
#     return jsonify({"status": "success"}), 200

# @api_bp.route('/get_response/<userQuery>', methods=['GET'])
# def get_response(userQuery):
#     response = save_query_and_response(userQuery)
#     return jsonify({"status": "success", "response": response}), 200


# @api_bp.route('/get_query_history', methods=['GET'])
# def get_query_history():
#     return jsonify({"status": "success", "response": queries_and_response}), 200

# # @api_bp.route('/sentiment', methods=['POST'])
# # def sentiment():
# #     sentences = request.json['sentences']
# #     results = analyze_sentiment(sentences)
# #     return jsonify(results), 200

# # @api_bp.route('/query_response', methods=['POST'])
# # def query_response():
# #     data = request.json
# #     save_query_and_response(data['query'])
# #     return jsonify({"status": "success"}), 200
