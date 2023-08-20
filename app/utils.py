from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer


def decode_token(token):
    secret_key = current_app.config['SECRET_KEY']
    token_serializer = Serializer(secret_key)
    try:
        decoded_data = token_serializer.loads(token)
        return decoded_data
    except Exception as e:
        return None
