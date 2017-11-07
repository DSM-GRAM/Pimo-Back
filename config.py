from datetime import timedelta

PORT = 5001

SECRET_KEY = 'L0v3Pyth'
JWT_SECRET_KEY = SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)
JWT_HEADER_TYPE = 'JWT'