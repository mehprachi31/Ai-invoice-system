import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = "AIInvoice@2026#SecureKey"

    SQLALCHEMY_DATABASE_URI = \
        "sqlite:///" + os.path.join(
            BASE_DIR,
            "instance",
            "invoice.db"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "pdf",
        "png",
        "jpg",
        "jpeg"
    }