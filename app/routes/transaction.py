from datetime import datetime

from flask import jsonify, request

from app import db
from app.models.transaction import Transaction
from app.models.wallet import Wallet
from app.routes.wallet import wallet_bp
from app.utils import decode_token


@wallet_bp.route('/api/v1/wallet/transactions', methods=['GET'])
def view_transactions():
    token = request.headers.get('Authorization').split(' ')[1]
    decoded_data = decode_token(token)

    if not decoded_data or 'customer_xid' not in decoded_data:
        return jsonify({'status': 'error', 'message': 'Invalid or missing token'}), 401

    customer_xid = decoded_data['customer_xid']

    wallet = Wallet.query.filter_by(owned_by=customer_xid).first()

    if not wallet or wallet.status != 'enabled':
        return jsonify({'status': 'fail', 'data': {'error': 'Wallet disabled'}}), 400

    transactions = Transaction.query.filter_by(user_id=customer_xid).all()

    response_data = {
        'transactions': [{
            'id': transaction.id,
            'status': transaction.status,
            'transacted_at': transaction.transacted_at.isoformat(),
            'type': transaction.type,
            'amount': transaction.amount,
            'reference_id': transaction.reference_id
        } for transaction in transactions]
    }
    response = {'status': 'success', 'data': response_data}
    return jsonify(response)


@wallet_bp.route('/api/v1/wallet/deposits', methods=['POST'])
def add_deposit():
    token = request.headers.get('Authorization').split(' ')[1]
    decoded_data = decode_token(token)

    if not decoded_data or 'customer_xid' not in decoded_data:
        return jsonify({'status': 'fail', 'data': {'error': 'Wallet disabled'}}), 400

    user_id = decoded_data['customer_xid']
    status = 'success'
    transacted_at = datetime.utcnow()
    type = 'deposit'
    amount = float(request.form.get('amount'))
    reference_id = request.form.get('reference_id')

    wallet = Wallet.query.filter_by(owned_by=user_id).first()

    if not wallet or wallet.status != 'enabled':
        return jsonify({'status': 'fail', 'data': {'error': 'Wallet disabled'}}), 400

    existing_transaction = Transaction.query.filter_by(reference_id=reference_id).first()

    if existing_transaction:
        return jsonify({'status': 'fail', 'data': {'error': 'Reference ID already used'}}), 400

    new_transaction = Transaction(user_id, status, transacted_at, type, amount, reference_id)
    db.session.add(new_transaction)

    wallet = Wallet.query.filter_by(owned_by=user_id).first()
    wallet.balance += amount
    db.session.commit()

    response_data = {
        'deposit': {
            'id': new_transaction.id,
            'deposited_by': new_transaction.user_id,
            'status': new_transaction.status,
            'deposited_at': new_transaction.transacted_at.isoformat(),
            'amount': new_transaction.amount,
            'reference_id': new_transaction.reference_id
        }
    }
    response = {'status': 'success', 'data': response_data}
    return jsonify(response), 201


@wallet_bp.route('/api/v1/wallet/withdrawals', methods=['POST'])
def make_withdrawal():
    token = request.headers.get('Authorization').split(' ')[1]
    decoded_data = decode_token(token)

    if not decoded_data or 'customer_xid' not in decoded_data:
        return jsonify({'status': 'fail', 'data': {'error': 'Wallet disabled'}}), 400

    user_id = decoded_data['customer_xid']
    status = 'success'
    transacted_at = datetime.utcnow()
    type = 'withdrawal'
    amount = float(request.form.get('amount'))
    reference_id = request.form.get('reference_id')

    wallet = Wallet.query.filter_by(owned_by=user_id).first()

    if not wallet or wallet.status != 'enabled':
        return jsonify({'status': 'fail', 'data': {'error': 'Wallet disabled'}}), 400

    existing_transaction = Transaction.query.filter_by(reference_id=reference_id).first()
    if existing_transaction:
        return jsonify({'status': 'fail', 'data': {'error': 'Reference ID already used'}}), 400

    if wallet.balance < amount:
        return jsonify({'status': 'fail', 'data': {'error': 'Insufficient balance'}}), 400

    new_transaction = Transaction(user_id, status, transacted_at, type, amount, reference_id)
    db.session.add(new_transaction)

    wallet.balance -= amount
    db.session.commit()

    response_data = {
        'withdrawal': {
            'id': new_transaction.id,
            'withdrawn_by': new_transaction.user_id,
            'status': new_transaction.status,
            'withdrawn_at': new_transaction.transacted_at.isoformat(),
            'amount': new_transaction.amount,
            'reference_id': new_transaction.reference_id
        }
    }
    response = {'status': 'success', 'data': response_data}
    return jsonify(response), 201
