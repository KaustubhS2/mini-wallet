from flask import Blueprint, jsonify, request, current_app
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

account_bp = Blueprint('account', __name__)

# TOKEN_EXPIRATION = 3600  # Token expiration time in seconds (1 hour)


@account_bp.route('/api/v1/init', methods=['POST'])
def initialize_account():

    customer_xid = request.form.get('customer_xid')

    secret_key = current_app.config['SECRET_KEY']
    token_serializer = Serializer(secret_key)
    token = token_serializer.dumps({'customer_xid': customer_xid})

    response_data = {'token': token}
    response = {'status': 'success', 'data': response_data}
    return jsonify(response), 201
