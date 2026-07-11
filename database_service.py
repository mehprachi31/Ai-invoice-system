"""
database_service.py

Corporate AI Invoice System
Handles all SQLite database operations.
"""

from sqlalchemy import func
from models import db, Invoice
from datetime import datetime



class DatabaseService:

    # -----------------------------------------
    # Save Invoice
    # -----------------------------------------
    def save_invoice(self, data):

     invoice_date = None
     due_date = None

    # Convert Invoice Date
     if data.get("invoice_date"):
       try:
            invoice_date = datetime.strptime(
                data["invoice_date"],
                "%d-%m-%Y"
            ).date()
       except:
        pass

    # Convert Due Date
     if data.get("due_date"):
      try:
            due_date = datetime.strptime(
                data["due_date"],
                "%d-%m-%Y"
            ).date()
      except:
        pass

    # Prevent duplicate invoice numbers
     if self.duplicate_exists(data.get("invoice_number")):
        raise ValueError("Invoice Number already exists.")

     invoice = Invoice(

        vendor_name=data.get("vendor_name"),

        gst_number=data.get("gst_number"),

        invoice_number=data.get("invoice_number"),

        invoice_date=invoice_date,

        due_date=due_date,

        amount=float(data.get("amount") or 0),

        cgst=float(data.get("cgst") or 0),

        sgst=float(data.get("sgst") or 0),

        igst=float(data.get("igst") or 0),

        category=data.get("category", "General"),

        status="Pending",

        file_name=data.get("file_name"),

        notes=data.get("notes", "")

    )

     db.session.add(invoice)

     db.session.commit()

     return invoice
    # -----------------------------------------
    # Get All Invoices
    # -----------------------------------------
    def get_all_invoices(self):

        return Invoice.query.order_by(
            Invoice.created_at.desc()
        ).all()

    # -----------------------------------------
    # Recent Invoices
    # -----------------------------------------
    def get_recent_invoices(self, limit=5):

        return Invoice.query.order_by(
            Invoice.created_at.desc()
        ).limit(limit).all()

    # -----------------------------------------
    # Get Invoice
    # -----------------------------------------
    def get_invoice(self, invoice_id):

        return Invoice.query.get(invoice_id)

    # -----------------------------------------
    # Delete Invoice
    # -----------------------------------------
    def delete_invoice(self, invoice_id):

        invoice = Invoice.query.get(invoice_id)

        if invoice:

            db.session.delete(invoice)
            db.session.commit()

            return True

        return False

    # -----------------------------------------
    # Update Status
    # -----------------------------------------
    def update_status(self, invoice_id, status):

        invoice = Invoice.query.get(invoice_id)

        if invoice:

            invoice.status = status

            db.session.commit()

            return True

        return False

    # -----------------------------------------
    # Duplicate Check
    # -----------------------------------------
    def duplicate_exists(self, invoice_number):

        return Invoice.query.filter_by(
            invoice_number=invoice_number
        ).first() is not None

    # -----------------------------------------
    # Search Invoice
    # -----------------------------------------
    def search(self, keyword):

        keyword = f"%{keyword}%"

        return Invoice.query.filter(

            (Invoice.vendor_name.like(keyword)) |
            (Invoice.invoice_number.like(keyword))

        ).all()

    # -----------------------------------------
    # Dashboard Statistics
    # -----------------------------------------
    def dashboard_data(self):

        invoices = Invoice.query.all()

        total_invoices = len(invoices)

        total_vendors = len(
            set(
                invoice.vendor_name
                for invoice in invoices
            )
        )

        total_revenue = round(
            sum(invoice.amount for invoice in invoices),
            2
        )

        pending = Invoice.query.filter_by(
            status="Pending"
        ).count()

        paid = Invoice.query.filter_by(
            status="Paid"
        ).count()

        cancelled = Invoice.query.filter_by(
            status="Cancelled"
        ).count()

        average_invoice = round(
            total_revenue / total_invoices,
            2
        ) if total_invoices else 0

        recent = self.get_recent_invoices()

        top_vendors = self.get_top_vendors()

        category_stats = self.category_statistics()

        monthly = self.monthly_statistics()

        return {

            "total_invoices": total_invoices,

            "total_vendors": total_vendors,

            "monthly_expense": total_revenue,

            "average_invoice": average_invoice,

            "pending": pending,

            "paid": paid,

            "cancelled": cancelled,

            "recent": recent,

            "top_vendors": top_vendors,

            "categories": category_stats,

            "monthly": monthly

        }

    # -----------------------------------------
    # Top Vendors
    # -----------------------------------------
    def get_top_vendors(self, limit=5):

        return (

            db.session.query(

                Invoice.vendor_name,

                func.count(Invoice.id).label("count"),

                func.sum(Invoice.amount).label("total")

            )

            .group_by(
                Invoice.vendor_name
            )

            .order_by(
                func.sum(Invoice.amount).desc()
            )

            .limit(limit)

            .all()

        )

    # -----------------------------------------
    # Monthly Statistics
    # -----------------------------------------
    def monthly_statistics(self):

        data = (

            db.session.query(

                func.strftime(
                    "%Y-%m",
                    Invoice.created_at
                ).label("month"),

                func.sum(
                    Invoice.amount
                ).label("amount")

            )

            .group_by("month")

            .order_by("month")

            .all()

        )

        labels = []
        values = []

        for month, amount in data:

            labels.append(month)
            values.append(float(amount))

        return {

            "labels": labels,

            "values": values

        }

    # -----------------------------------------
    # Category Statistics
    # -----------------------------------------
    def category_statistics(self):

        data = (

            db.session.query(

                Invoice.category,

                func.count(Invoice.id)

            )

            .group_by(
                Invoice.category
            )

            .all()

        )

        labels = []
        values = []

        for category, total in data:

            labels.append(category)
            values.append(total)

        return {

            "labels": labels,

            "values": values

        }

    # -----------------------------------------
    # Revenue Summary
    # -----------------------------------------
    def revenue_summary(self):

        total = db.session.query(

            func.sum(
                Invoice.amount
            )

        ).scalar()

        return round(total or 0, 2)

    # -----------------------------------------
    # Invoice Status
    # -----------------------------------------
    def invoice_status(self):

        return {

            "Paid": Invoice.query.filter_by(
                status="Paid"
            ).count(),

            "Pending": Invoice.query.filter_by(
                status="Pending"
            ).count(),

            "Cancelled": Invoice.query.filter_by(
                status="Cancelled"
            ).count()

        }