from flask import Flask, render_template, request, redirect
from database_service import DatabaseService
from datetime import datetime
import os

from ocr_service import OCRService
from extractor import InvoiceExtractor

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from models import db, User, Invoice, Settings
app = Flask(__name__)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

# ------------------------
# Configuration
# ------------------------
app.config["SECRET_KEY"] = "your-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///invoice.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db.init_app(app)

with app.app_context():
    db.create_all()

db_service = DatabaseService()

ocr = None
extractor = None
# ------------------------
# Dashboard
# ------------------------


@app.route("/")
@login_required
def dashboard():

    dashboard = db_service.dashboard_data()

    return render_template(

        "dashboard.html",

        data=dashboard,

        user=current_user

    )

# ------------------------
# Upload
# ------------------------
@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    if request.method == "POST":

        if "invoice" not in request.files:
            return "No file selected"

        file = request.files["invoice"]

        if file.filename == "":
            return "Please select a file"

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        try:

            print("=" * 80)
            print("UPLOADED FILE :", filepath)

            # OCR
            text = ocr.extract_text(filepath)

            print("=" * 80)
            print("OCR RESULT")
            print("=" * 80)
            print(text)

            if text.strip() == "":
                return "OCR could not detect any text."

            # Extract
            invoice_data = extractor.extract(text)

            print("=" * 80)
            print("EXTRACTED DATA")
            print("=" * 80)

            for key, value in invoice_data.items():
                print(f"{key} : {value}")

            invoice_data["file_name"] = file.filename

            db_service.save_invoice(invoice_data)

            print("Invoice Saved Successfully")

            return redirect("/invoices")

        except Exception as e:

            import traceback

            traceback.print_exc()

            return f"OCR Error : {e}"

    return render_template("upload.html")
# ------------------------
# Invoices
# ------------------------
@app.route("/invoices")
@login_required
def invoices():

    invoices = db_service.get_all_invoices()

    return render_template(
        "invoices.html",
        invoices=invoices
    )



# ------------------------
# Delete Invoice
# ------------------------
@app.route("/delete/<int:id>")
def delete_invoice(id):

    db_service.delete_invoice(id)

    return redirect("/invoices")


# ------------------------
# Reports
# ------------------------
@app.route("/reports")
def reports():

    return render_template("reports.html")


# ------------------------
# Profile
# ------------------------
@app.route("/profile")
@login_required
def profile():

    data = db_service.dashboard_data()

    return render_template(
        "profile.html",
        user=current_user,
        data=data
    )


# ------------------------
# Settings
# ------------------------
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    settings = Settings.query.first()

    if settings is None:

        settings = Settings()

        db.session.add(settings)

        db.session.commit()

    if request.method == "POST":

        settings.company_name = request.form.get("company_name")

        settings.gst_number = request.form.get("gst")

        settings.company_email = request.form.get("company_email")

        settings.company_phone = request.form.get("phone")

        settings.currency = request.form.get("currency")

        settings.default_status = request.form.get("status")

        settings.theme = request.form.get("theme")

        settings.ocr_enabled = "ocr_enabled" in request.form

        settings.auto_extract = "auto_extract" in request.form

        settings.email_notifications = "email_notifications" in request.form

        settings.invoice_notifications = "invoice_notifications" in request.form

        settings.monthly_report = "monthly_report" in request.form

        db.session.commit()

        return redirect("/settings")

    return render_template(

        "settings.html",

        settings=settings,

        user=current_user

    ) 
# -------------------------
# Registeration  Route
# -------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]

        email = request.form["email"]

        password = request.form["password"]

        # Check existing user
        user = User.query.filter_by(email=email).first()

        if user:

            return "Email already registered."

        new_user = User(

            full_name=full_name,

            email=email

        )

        new_user.set_password(password)

        db.session.add(new_user)

        db.session.commit()

        return redirect("/login")

    return render_template("register.html")



# ------------------------
# Login
# ------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        print("Email:", email)

        user = User.query.filter_by(email=email).first()

        print("User Found:", user)

        if user:
            print("Password Correct:", user.check_password(password))

        if user and user.check_password(password):
            login_user(user)
            return redirect("/")

        return render_template(
            "login.html",
            error="Invalid Email or Password"
        )

    return render_template("login.html")


# ------------------------
# Logout
# ------------------------
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")


# ------------------------
# Run
# ------------------------
if __name__ == "__main__":

    app.run(debug=True)