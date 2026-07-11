"""
AI Invoice Processing System
OCR Service

Supports:
1. PDF Invoice
2. JPG
3. PNG
4. JPEG

Uses:
EasyOCR
pdf2image
OpenCV
"""

import os
import cv2
import easyocr

from PIL import Image
from pdf2image import convert_from_path


class OCRService:

    def __init__(self):

        # English Reader
        self.reader = easyocr.Reader(
            ['en'],
            gpu=False
        )

    # ---------------------------------
    # IMAGE PREPROCESSING
    # ---------------------------------

    def preprocess_image(self, image_path):

        image = cv2.imread(image_path)

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        blur = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )

        thresh = cv2.threshold(
            blur,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        return thresh

    # ---------------------------------
    # OCR IMAGE
    # ---------------------------------

    def read_image(self, image_path):

        processed = self.preprocess_image(
            image_path
        )

        result = self.reader.readtext(
    processed,
    detail=0,
    paragraph=True,
    decoder="beamsearch"
    )
        

        return "\n".join(result)

    # ---------------------------------
    # OCR PDF
    # ---------------------------------

    def read_pdf(self, pdf_path):

        pages = convert_from_path(
        pdf_path,
        dpi=300
           )

        final_text = ""

        temp_folder = "uploads/temp"

        os.makedirs(
            temp_folder,
            exist_ok=True
        )

        for i, page in enumerate(pages):

            image_file = os.path.join(
                temp_folder,
                f"page_{i}.jpg"
            )

            page.save(
                image_file,
                "JPEG"
            )

            final_text += self.read_image(
                image_file
            )

            final_text += "\n"

        return final_text

    # ---------------------------------
    # MAIN FUNCTION
    # ---------------------------------

    def extract_text(self, file_path):

        extension = file_path.split(".")[-1].lower()

        if extension in [
            "jpg",
            "jpeg",
            "png"
        ]:

            return self.read_image(
                file_path
            )

        elif extension == "pdf":

            return self.read_pdf(
                file_path
            )

        else:

            raise Exception(
                "Unsupported File Format"
            )


# ---------------------------------------
# TEST
# ---------------------------------------
if __name__ == "__main__":

    ocr = OCRService()

    file = "sample_invoice.pdf"

    print(
        ocr.extract_text(file)
    )