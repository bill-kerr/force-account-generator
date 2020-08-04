from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from PyPDF2 import PdfFileReader, PdfFileWriter


def make_pdf(pages, output_file_path):
    pdf_writer = set_need_appearances_writer(PdfFileWriter())
    streams = []
    for page in pages:
        streams.append(add_page(pdf_writer, page))
    save_pdf(pdf_writer, output_file_path)
    for stream in streams:
        stream.close()


def add_page(pdf_writer, page):
    input_stream = open(page.template, "rb")
    pdf_reader = get_pdf_reader(input_stream)
    pdf_writer.addPage(pdf_reader.getPage(0))
    pdf_writer.updatePageFormFieldValues(
        pdf_writer.getPage(-1), page.fields)
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


def save_pdf(pdf_writer, output_file_path):
    with open(output_file_path, "wb") as output_stream:
        pdf_writer.write(output_stream)
