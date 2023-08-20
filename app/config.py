class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:smartpay@127.0.0.1:3306/miniwallet'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking

    # Secret key for session management and token generation
    SECRET_KEY = 'bda74c292365a0316af73d537831d40dab4320ab2ac6d5ebdb7ed37281e0c657'
    DEBUG = False
