from datetime import datetime

from flask import Blueprint, jsonify, request, current_app
from app.models.wallet import Wallet
from app import db

wallet_bp = Blueprint('wallet', __name__)

from itsdangerous import URLSafeTimedSerializer as Serializer


def decode_token(token):
    secret_key = current_app.config['SECRET_KEY']
    token_serializer = Serializer(secret_key)
    try:
        decoded_data = token_serializer.loads(token)
        return decoded_data
    except Exception as e:
        return None


@wallet_bp.route('/api/v1/wallet', methods=['POST'])
def enable_wallet():
    token = request.headers.get('Authorization').split(' ')[1]
    decoded_data = decode_token(token)

    if not decoded_data or 'customer_xid' not in decoded_data:
        return jsonify({'status': 'error', 'message': 'Invalid or missing token'}), 401

    customer_xid = decoded_data['customer_xid']
    # print(customer_xid)

    wallet = Wallet.query.filter_by(owned_by=customer_xid).first()

    if wallet:
        if wallet.status == 'disabled':
            current_time = datetime.utcnow()
            wallet.status = 'enabled'
            wallet.enabled_at = current_time
            db.session.commit()

            response_data = {
                'wallet': {
                    'id': wallet.id,
                    'owned_by': wallet.owned_by,
                    'status': wallet.status,
                    'enabled_at': wallet.enabled_at.isoformat(),
                    'balance': wallet.balance
                }
            }
            response = {'status': 'success', 'data': response_data}
            return jsonify(response)

        return jsonify({'status': 'fail', 'message': 'Already enabled'}), 400

    current_time = datetime.utcnow()
    wallet = Wallet(owned_by=customer_xid, status='enabled', enabled_at=current_time, balance=0)
    db.session.add(wallet)
    db.session.commit()

    response_data = {
        'wallet': {
            'id': wallet.id,
            'owned_by': wallet.owned_by,
            'status': wallet.status,
            'enabled_at': wallet.enabled_at.isoformat(),
            'balance': wallet.balance
        }
    }
    response = {'status': 'success', 'data': response_data}
    return jsonify(response), 201  # Return 201 Created status code


@wallet_bp.route('/api/v1/wallet', methods=['GET'])
def view_balance():
    token = request.headers.get('Authorization').split(' ')[1]
    decoded_data = decode_token(token)

    if not decoded_data or 'customer_xid' not in decoded_data:
        return jsonify({'status': 'error', 'message': 'Invalid or missing token'}), 401

    customer_xid = decoded_data['customer_xid']

    wallet = Wallet.query.filter_by(owned_by=customer_xid).first()

    if not wallet:
        return jsonify({'status': 'error', 'message': 'Wallet not found'}), 404

    wallet_data = {
        'id': wallet.id,
        'owned_by': wallet.owned_by,
        'status': wallet.status,
        'enabled_at': wallet.enabled_at.isoformat(),
        'balance': wallet.balance
    }

    response_data = {'wallet': wallet_data}
    response = {'status': 'success', 'data': response_data}

    return jsonify(response)


@wallet_bp.route('/api/v1/wallet', methods=['PATCH'])
def disable_wallet():
    token = request.headers.get('Authorization').split(' ')[1]
    decoded_data = decode_token(token)

    if not decoded_data or 'customer_xid' not in decoded_data:
        return jsonify({'status': 'fail', 'data': {'error': 'Wallet disabled'}}), 400

    user_id = decoded_data['customer_xid']
    transacted_at = datetime.utcnow()
    is_disabled = request.form.get('is_disabled')

    if is_disabled.lower() == 'true':
        status = 'disabled'
    else:
        status = 'enabled'

    wallet = Wallet.query.filter_by(owned_by=user_id).first()

    if not wallet:
        return jsonify({'status': 'fail', 'data': {'error': 'Wallet not found'}}), 404

    wallet.status = status

    wallet.disabled_at = transacted_at
    db.session.commit()

    response_data = {
        'wallet': {
            'id': wallet.id,
            'owned_by': wallet.owned_by,
            'status': wallet.status,
            'disabled_at': wallet.disabled_at.isoformat(),
            'balance': wallet.balance
        }
    }
    response = {'status': 'success', 'data': response_data}
    return jsonify(response)
