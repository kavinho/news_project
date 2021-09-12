import os

APP_PORT = os.environ.get("APP_PORT", 8888)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://root:password@localhost:27017/")