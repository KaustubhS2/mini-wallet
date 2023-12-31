from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')

    db.init_app(app)

    from app.routes.account import account_bp
    from app.routes.wallet import wallet_bp
    app.register_blueprint(account_bp)
    app.register_blueprint(wallet_bp)

    return app
