"""
Program that creates a PDF force account package from JSON data.
JSON input data must be in the same format as input.example.json.
"""
import argparse
from config.config import PdfFieldConfig
from input_data import InputData
from material import MaterialCollection
from labor import LaborCollection


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

    pdf_config = PdfFieldConfig('./config/pdf_config.json')
    input_data = InputData(args.source)
    material_collection = MaterialCollection(pdf_config, input_data)
    labor_collection = LaborCollection(pdf_config, input_data)
