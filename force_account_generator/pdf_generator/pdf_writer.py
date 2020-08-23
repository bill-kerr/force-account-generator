import os
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from PyPDF2 import PdfFileReader, PdfFileWriter


def make_pdf(pages, output_file_path, callback=None):
    root_dir = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(root_dir, 'templates')
    pdf_writer = set_need_appearances_writer(PdfFileWriter())
    streams = []
    num_pages = len(pages)
    progress_callback(callback, num_pages, 0, 2)
    for i, page in enumerate(pages):
        progress_callback(callback, num_pages, i + 1, 2)
        streams.append(add_page(pdf_writer, page, dir_path))
    save_pdf(pdf_writer, output_file_path, callback=callback)
    for stream in streams:
        stream.close()


def progress_callback(callback, num_pages=1, completed=1, stage=0, message=None):
    if callback is None:
        return
    progress = (completed / num_pages)
    msg = f'Creating PDF page {completed} of {num_pages}.' if message is None else message
    status = {'message': msg, 'num_pages': num_pages,
              'completed_pages': completed, 'progress': progress, 'stage': stage}
    callback(status)


def add_page(pdf_writer, page, root_dir):
    file_path = os.path.join(root_dir, page.template)
    input_stream = open(file_path, "rb")
    pdf_reader = get_pdf_reader(input_stream)
    pdf_writer.addPage(pdf_reader.getPage(0))
    pdf_writer.updatePageFormFieldValues(
        pdf_writer.getPage(-1), page.values)
    return input_stream


def get_pdf_reader(input_stream):
    pdf_reader = PdfFileReader(input_stream, strict=False)
    if "/AcroForm" in pdf_reader.trailer["/Root"]:
        pdf_reader.trailer["/Root"]["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})
    return pdf_reader


def set_need_appearances_writer(writer):
    try:
        catalog = writer._root_object
        if "/AcroForm" not in catalog:
            writer._root_object.update({
                NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(
            True)
        return writer

    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
        return writer


def save_pdf(pdf_writer, output_file_path, callback=None):
    progress_callback(callback, stage=3, message="Saving PDF.")
    with open(output_file_path, "wb") as output_stream:
        pdf_writer.write(output_stream)
    progress_callback(callback, stage=4, message="PDF saved.")
