"""
Program that creates a PDF force account package from JSON data.
JSON input data must be in the same format as input.example.json.
"""
import argparse
from config.config import PdfFieldConfig
from data_loader import DataLoader
from pdf_package import PdfPackage


class PdfGenerator:
    def __init__(self, input_file_path, output_file_path, pdf_config_file="./config/pdf_config.json"):
        cfg = PdfFieldConfig(pdf_config_file)
        data_loader = DataLoader(input_file_path)
        pdf = PdfPackage(data_loader, cfg, output_file_path)
        pdf.generate_pdf()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'source', help='The path to the source JSON file (must end with .json)')
    parser.add_argument(
        'dest', help='The path to the destination PDF file (must end with .pdf)')
    args = parser.parse_args()

    if not args.source.endswith('.json') or not args.dest.endswith('.pdf'):
        raise parser.error(
            'Incorrect file extension (source=*.json dest=*.pdf)')

    config = PdfFieldConfig('./config/pdf_config.json')
    data = DataLoader(args.source)
    pdf_package = PdfPackage(data, config, args.dest)
    pdf_package.generate_pdf()
