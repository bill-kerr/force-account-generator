"""
Program that extracts Force Account data from Excel.
"""
from .workbook import Workbook


class Importer:
    def __init__(self, source_file, delay_processing=False, save_json=True):
        self.__data_loaded = False
        self.__wb = Workbook(source_file)
        if not delay_processing:
            self.process_data()

    def process_data(self):
        if not self.__data_loaded:
            self.__data = self.__wb.process_workbook()
            self.__data_loaded = True
            return self.__data

    @property
    def data(self):
        return self.__data if self.__data_loaded else None
