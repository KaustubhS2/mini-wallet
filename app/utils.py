from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer


def decode_token(token):
    """
    Decode token helper function. Returns decoded [customer_xd]
    :param token:
    :return: decoded token, None failure
    """
    secret_key = current_app.config['SECRET_KEY']
    token_serializer = Serializer(secret_key)
    try:
        decoded_data = token_serializer.loads(token)
        return decoded_data
    except Exception as e:
        return None
