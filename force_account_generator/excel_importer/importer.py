"""
Program that extracts Force Account data from Excel.
"""
from .workbook import Workbook


class Importer:
    def __init__(self, source_file, delay_processing=False, save_json=True, callback=None):
        self.__data_loaded = False
        self.__cb = callback
        self.__callback('Loading workbook')
        self.__wb = Workbook(source_file)
        if not delay_processing:
            self.process_data()

    def process_data(self):
        if not self.__data_loaded:
            self.__data = self.__wb.process_workbook()
            self.__data_loaded = True
            return self.__data

    def __callback(self, message):
        if self.__cb is None:
            return
        status = {'status': 'processing', 'stage': 1, 'stage_progress': 0, 'stage_total': 1, 'message': message}
        self.__cb(status)

    @property
    def data(self):
        return self.__data if self.__data_loaded else None
