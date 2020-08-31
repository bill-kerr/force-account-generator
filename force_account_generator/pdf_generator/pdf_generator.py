from .config import PdfFieldConfig
from .data_loader import DataLoader
from .pdf_package import PdfPackage


def generate_pdf(input_data, daily_sheets=False, callback=None):
    config = PdfFieldConfig()
    data_loader = DataLoader(input_data)
    pdf = PdfPackage(data_loader, config, daily_sheets=daily_sheets, callback=callback)
    return pdf.generate_pdf()
