import argparse
from excel_importer import Importer
from pdf_generator import generate_pdf


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='The path to the source Excel file (must end with .xlsx)')
    parser.add_argument('dest', help='The path to the destination PDF file (must end with .pdf)')
    args = parser.parse_args()

    if not args.source.endswith('.xlsx') or not args.dest.endswith('.pdf'):
        raise parser.error('Incorrect file extension (source=*.xlsx dest=*.pdf)')

    input_data = Importer(args.source).data
    generate_pdf(input_data, './pdf_config.json', args.dest)
