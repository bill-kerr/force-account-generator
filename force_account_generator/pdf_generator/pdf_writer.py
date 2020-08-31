import os
from io import BytesIO
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from PyPDF2 import PdfFileReader, PdfFileWriter


def make_pdf(pages, callback=None):
    root_dir = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(root_dir, 'templates')
    pdf_writer = set_need_appearances_writer(PdfFileWriter())
    streams = []
    num_pages = len(pages)
    for i, page in enumerate(pages):
        streams.append(add_page(pdf_writer, page, dir_path))
        message = f'Creating PDF page {i+1} of {num_pages}.'
        progress_callback(callback, message, num_pages=num_pages, completed=i + 1)
    file_path = save_pdf(pdf_writer, callback=callback)
    for stream in streams:
        stream.close()
    return file_path


def progress_callback(callback, message, num_pages=1, completed=1):
    if callback is None:
        return
    status = {'status': 'processing', 'stage': 2, 'stage_progress': completed,
              'stage_total': num_pages, 'message': message}
    callback(status)


def add_page(pdf_writer, page, root_dir):
    file_path = os.path.join(root_dir, page.template)
    input_stream = open(file_path, 'rb')
    pdf_reader = get_pdf_reader(input_stream)
    pdf_writer.addPage(pdf_reader.getPage(0))
    pdf_writer.updatePageFormFieldValues(pdf_writer.getPage(-1), page.values)
    return input_stream


def get_pdf_reader(input_stream):
    pdf_reader = PdfFileReader(input_stream, strict=False)
    if '/AcroForm' in pdf_reader.trailer['/Root']:
        pdf_reader.trailer['/Root']['/AcroForm'].update({NameObject('/NeedAppearances'): BooleanObject(True)})
    return pdf_reader


def set_need_appearances_writer(writer):
    try:
        catalog = writer._root_object
        if '/AcroForm' not in catalog:
            writer._root_object.update({
                NameObject('/AcroForm'): IndirectObject(len(writer._objects), 0, writer)})

        need_appearances = NameObject('/NeedAppearances')
        writer._root_object['/AcroForm'][need_appearances] = BooleanObject(True)
        return writer

    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
        return writer


def save_pdf(pdf_writer, callback=None):
    callback({'status': 'processing', 'stage': 3, 'stage_progress': 0,
              'stage_total': 1, 'message': 'Saving PDF to file.'})

    file_result = BytesIO()
    pdf_writer.write(file_result)
    file_result.seek(0)
    return file_result
