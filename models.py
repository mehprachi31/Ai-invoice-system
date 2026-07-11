from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# ======================================
# USER TABLE
# ======================================

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="Admin"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Password Hash
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Password Verify
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def _repr_(self):
        return f"<User {self.email}>"


# ======================================
# INVOICE TABLE
# ======================================

class Invoice(db.Model):

    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)

    vendor_name = db.Column(
        db.String(200),
        nullable=False
    )

    gst_number = db.Column(
        db.String(20)
    )

    invoice_number = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    invoice_date = db.Column(
        db.Date
    )

    due_date = db.Column(
        db.Date
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    cgst = db.Column(
        db.Float,
        default=0
    )

    sgst = db.Column(
        db.Float,
        default=0
    )

    igst = db.Column(
        db.Float,
        default=0
    )

    category = db.Column(
        db.String(100),
        default="General"
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    file_name = db.Column(
        db.String(255)
    )

    notes = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Invoice {self.invoice_number}>"
    
    
class Settings(db.Model):

    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)

    company_name = db.Column(db.String(150), default="AI Invoice Processing")

    gst_number = db.Column(db.String(30))

    company_email = db.Column(db.String(120))

    company_phone = db.Column(db.String(20))

    currency = db.Column(db.String(10), default="INR")

    default_status = db.Column(
        db.String(20),
        default="Pending"
    )

    ocr_enabled = db.Column(
        db.Boolean,
        default=True
    )

    auto_extract = db.Column(
        db.Boolean,
        default=True
    )

    email_notifications = db.Column(
        db.Boolean,
        default=True
    )

    invoice_notifications = db.Column(
        db.Boolean,
        default=True
    )

    monthly_report = db.Column(
        db.Boolean,
        default=False
    )

    theme = db.Column(
        db.String(20),
        default="Light"
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )