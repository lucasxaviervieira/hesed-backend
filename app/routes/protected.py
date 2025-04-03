from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/test-protected', methods=['GET'])
@jwt_required()
def test_protected():
    return jsonify({"message": "This is a protected route!"}), 200