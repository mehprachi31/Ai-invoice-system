# 🤖 AI Invoice System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-green.svg">
  <img src="https://img.shields.io/badge/OCR-EasyOCR-orange.svg">
  <img src="https://img.shields.io/badge/SQLite-Database-blue.svg">
  <img src="https://img.shields.io/badge/Status-Active-success.svg">
  <img src="https://img.shields.io/badge/License-MIT-red.svg">
</p>

---

# 📄 AI Invoice System

An **AI-powered Invoice Management System** built with **Python, Flask, EasyOCR, and SQLite** that automatically extracts invoice information using Optical Character Recognition (OCR), stores it securely, and provides an easy-to-use dashboard for managing invoices.

This project eliminates manual data entry by allowing users to upload invoice images or PDFs and automatically extract important details.

---

## 🚀 Features

### 🤖 AI OCR Processing
- Upload invoice images
- Automatic text extraction using EasyOCR
- Intelligent invoice data recognition

### 📊 Dashboard
- Total invoices
- Invoice statistics
- Recent uploads
- Quick overview

### 📁 Invoice Management
- Upload invoices
- View invoice details
- Search invoices
- Delete invoices
- Download records

### 🔐 User Authentication
- User Registration
- Secure Login
- Logout
- Profile Management

### 💾 Database
- SQLite Database
- Store invoice information
- User management
- Fast data retrieval

### 📈 Reports
- Invoice reports
- Data summaries
- Organized records

---

# 🖥️ Screenshots

> Add your project screenshots here.

```
Dashboard Screenshot
```

```
Upload Invoice Page
```

```
Invoice List
```

```
OCR Result
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Flask | Web Framework |
| EasyOCR | AI OCR Engine |
| SQLite | Database |
| HTML5 | Frontend |
| CSS3 | Styling |
| JavaScript | User Interaction |

---

# 📂 Project Structure

```
AI-INVOICE-SYSTEM/
│
├── app.py
├── config.py
├── extractor.py
├── ocr_service.py
├── database_service.py
├── models.py
├── requirements.txt
│
├── instance/
│   └── invoice.db
│
├── static/
│   ├── css/
│   └── uploads/
│
├── templates/
│   ├── dashboard.html
│   ├── upload.html
│   ├── invoices.html
│   ├── reports.html
│   ├── settings.html
│   ├── login.html
│   ├── register.html
│   └── profile.html
│
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/mehprachi31/Ai-invoice-system.git
```

Move to project folder

```bash
cd Ai-invoice-system
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
python app.py
```

Application will start at

```
http://127.0.0.1:5000
```

---

# 📷 How It Works

```
Upload Invoice
        │
        ▼
 AI OCR (EasyOCR)
        │
        ▼
Extract Text
        │
        ▼
Process Invoice Data
        │
        ▼
Store in SQLite Database
        │
        ▼
Display on Dashboard
```

---

# 📊 OCR Extracted Information

The system can detect:

- Invoice Number
- Invoice Date
- Vendor Name
- Customer Name
- GST Number
- Invoice Amount
- Tax Amount
- Total Amount
- Address
- Item Details
- Contact Information

---

# 🔒 Security Features

- User Authentication
- Password Protection
- Secure Database Storage
- Session Management

---

# 🌟 Future Improvements

- PDF OCR Support
- AI Invoice Classification
- Multi-language OCR
- Export to Excel
- Export to PDF
- Email Notifications
- Cloud Storage
- REST API
- Admin Panel
- Charts & Analytics

---

# 📦 Requirements

- Python 3.10+
- Flask
- EasyOCR
- OpenCV
- SQLite
- Pillow
- NumPy

Install using

```bash
pip install -r requirements.txt
```

---

# 👨‍💻 Author

**Prachi Mehra**

GitHub:
https://github.com/mehprachi31

---

# ⭐ Support

If you like this project,

⭐ Star the repository

🍴 Fork the repository

🐛 Report issues

💡 Suggest improvements

---

# 📜 License

This project is licensed under the **MIT License**.

---

<p align="center">
Made with ❤️ using Python, Flask & AI OCR
</p>
