from ocr_service import OCRService

ocr = OCRService()

text = ocr.extract_text("uploads/your_invoice.jpg")

print(text)