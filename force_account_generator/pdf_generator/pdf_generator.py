"""
Program that creates a PDF force account package from JSON data.
JSON input data must be in the same format as input.example.json.
"""
import argparse
from .config import PdfFieldConfig
from .data_loader import DataLoader
from .pdf_package import PdfPackage


def generate_pdf(input_data, output_file_path, daily_sheets=False, callback=None):
    config = PdfFieldConfig()
    data_loader = DataLoader(input_data)
    pdf = PdfPackage(data_loader, config, output_file_path, daily_sheets=daily_sheets, callback=callback)
    return pdf.generate_pdf()
