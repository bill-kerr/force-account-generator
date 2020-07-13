import sys

if __name__ == '__main__':
    USAGE = 'Usage: pdf_generator.py <./source.json> [./result.pdf]'

    if len(sys.argv) < 2:
        raise Exception(USAGE)
    source = sys.argv[1]
    dest = sys.argv[2] if len(sys.argv) > 2 else './result.pdf'

    if not dest.endswith('.pdf'):
        raise Exception(USAGE)
