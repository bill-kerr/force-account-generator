"""
Program that creates a PDF force account package from JSON data.
JSON input data must be in the same format as input.example.json.
"""
import argparse
from config.config import PdfFieldConfig
from input_data import InputData
from material import MaterialCollection
from labor import LaborCollection
from pdf_writer import make_pdf


class PdfGenerator:
    def __init__(self, input_file_path, output_file_path, pdf_config_file="./config/pdf_config.json"):
        cfg = PdfFieldConfig(pdf_config_file)
        input_data = InputData(input_file_path)
        pdf = PdfPackage(input_data, cfg, output_file_path)
        pdf.generate_pdf()


class PdfPackage:
    def __init__(self, input_data, pdf_config, output_file_path):
        self.__input_data = input_data
        self.__pdf_config = pdf_config
        self.__output_file_path = output_file_path
        self.__material_pages = MaterialCollection(self.__input_data, self.__pdf_config).pages
        self.__labor_pages = LaborCollection(self.__input_data, self.__pdf_config).pages

    def generate_pdf(self):
        pages = self.__material_pages + self.__labor_pages
        make_pdf(pages, self.__output_file_path)


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
    data = InputData(args.source)
    pdf_package = PdfPackage(data, config, args.dest)
    pdf_package.generate_pdf()
