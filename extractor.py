"""
AI Invoice Processing System
Invoice Data Extractor

Extracts:
- Vendor Name
- GST Number
- Invoice Number
- Invoice Date
- Due Date
- Total Amount
- CGST
- SGST
- IGST
"""

import re
from datetime import datetime


class InvoiceExtractor:

    def __init__(self):
        pass

    # -------------------------------
    # GST Number
    # -------------------------------

    def get_gst(self, text):

        pattern = r"\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}\b"

        match = re.search(pattern, text)

        if match:
            return match.group()

        return ""

    # -------------------------------
    # Invoice Number
    # -------------------------------

    def get_invoice_number(self, text):

        patterns = [

            r"Invoice\s*No\.?\s*[:\-]?\s*([A-Za-z0-9\-\/]+)",

            r"Invoice\s*Number\s*[:\-]?\s*([A-Za-z0-9\-\/]+)",

            r"Inv\s*No\s*[:\-]?\s*([A-Za-z0-9\-\/]+)"

        ]

        for pattern in patterns:

            result = re.search(pattern, text, re.IGNORECASE)

            if result:
                return result.group(1)

        return ""

    # -------------------------------
    # Invoice Date
    # -------------------------------

    def get_invoice_date(self, text):

        pattern = r"(\d{2}[\/\-]\d{2}[\/\-]\d{4})"

        result = re.search(pattern, text)

        if result:
            return result.group()

        return ""

    # -------------------------------
    # Due Date
    # -------------------------------

    def get_due_date(self, text):

        pattern = r"Due\s*Date\s*[:\-]?\s*(\d{2}[\/\-]\d{2}[\/\-]\d{4})"

        result = re.search(pattern, text, re.IGNORECASE)

        if result:
            return result.group(1)

        return ""

    # -------------------------------
    # Total Amount
    # -------------------------------

    def get_total_amount(self, text):

        patterns = [

            r"Total\s*Amount\s*[:\-]?\s*₹?\s*([\d,]+\.\d{2})",

            r"Grand\s*Total\s*[:\-]?\s*₹?\s*([\d,]+\.\d{2})",

            r"Amount\s*Payable\s*[:\-]?\s*₹?\s*([\d,]+\.\d{2})"

        ]

        for pattern in patterns:

            result = re.search(pattern, text, re.IGNORECASE)

            if result:
                return result.group(1)

        return ""

    # -------------------------------
    # CGST
    # -------------------------------

    def get_cgst(self, text):

        result = re.search(

            r"CGST.*?([\d,]+\.\d{2})",

            text,

            re.IGNORECASE

        )

        return result.group(1) if result else "0"

    # -------------------------------
    # SGST
    # -------------------------------

    def get_sgst(self, text):

        result = re.search(

            r"SGST.*?([\d,]+\.\d{2})",

            text,

            re.IGNORECASE

        )

        return result.group(1) if result else "0"

    # -------------------------------
    # IGST
    # -------------------------------

    def get_igst(self, text):

        result = re.search(

            r"IGST.*?([\d,]+\.\d{2})",

            text,

            re.IGNORECASE

        )

        return result.group(1) if result else "0"

    # -------------------------------
    # Vendor Name
    # -------------------------------

    def get_vendor(self, text):

        lines = text.split("\n")

        for line in lines:

            line = line.strip()

            if len(line) > 5:

                if "invoice" not in line.lower():

                    if "gst" not in line.lower():

                        return line

        return "Unknown Vendor"

    # -------------------------------
    # Extract All
    # -------------------------------

    def extract(self, text):

        data = {

            "vendor_name": self.get_vendor(text),

            "gst_number": self.get_gst(text),

            "invoice_number": self.get_invoice_number(text),

            "invoice_date": self.get_invoice_date(text),

            "due_date": self.get_due_date(text),

            "amount": self.get_total_amount(text),

            "cgst": self.get_cgst(text),

            "sgst": self.get_sgst(text),

            "igst": self.get_igst(text)

        }

        return data


# ----------------------------------------
# TEST
# ----------------------------------------

if __name__ == "__main__":

    sample_text = """

    ABC PRIVATE LIMITED

    GSTIN : 23ABCDE1234F1Z5

    Invoice No : INV2026001

    Invoice Date : 03-07-2026

    Due Date : 10-07-2026

    Total Amount : 25000.00

    CGST : 2250.00

    SGST : 2250.00

    """

    extractor = InvoiceExtractor()

    result = extractor.extract(sample_text)

    print("\nExtracted Data\n")

    for key, value in result.items():

        print(f"{key} : {value}")