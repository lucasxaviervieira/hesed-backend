from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from app.models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@jwt_required()
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Dados inválidos'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Usuário já existe'}), 409

    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Usuário criado com sucesso'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        token = create_access_token(identity=str(user.id))
        return jsonify({'access_token': token}), 200
    
    return jsonify({'error': 'Credenciais inválidas'}), 401
