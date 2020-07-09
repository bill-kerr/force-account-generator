from openpyxl import load_workbook as load_wb
from worksheet import Worksheet
from config import config

class Workbook:
  def __init__(self, excel_file_path):
    self.__load_workbook(excel_file_path)
    self.__generate_worksheets()
    self.__generate_named_cells()
  
  def __load_workbook(self, file_path):
    self.__workbook = load_wb(file_path, read_only=True, data_only=True)
  
  def __generate_worksheets(self):
    self.worksheets = [Worksheet(self.__workbook[worksheet_name])
                        for worksheet_name in self.__workbook.get_sheet_names()]
  
  def __generate_named_cells(self):
    self.named_cells = self.__get_defined_names_from_workbook(config['defined_cell_names'])
  
  def __get_defined_names_from_workbook(self, cell_names):
    named_cells = {}
    for cell_name in cell_names:
      for worksheet_name, cell_coordinates in self.__workbook.defined_names[cell_name].destinations:
        worksheet = self.get_worksheet(worksheet_name)
        named_cells[cell_name] = worksheet.cell_value(cell_coordinates)
    
    return named_cells
  
  def get_worksheet(self, worksheet_name):
    for worksheet in self.worksheets:
      if worksheet.worksheet_name == worksheet_name:
        return worksheet
    
    raise Exception('Specified Worksheet "' + worksheet_name + '" does not exist.')

  def get_named_cell_value(self, cell_name):
    for worksheet_name, cell_coordinates in self.__workbook.defined_names[cell_name].destinations:
      worksheet = self.get_worksheet(worksheet_name)
      return worksheet.cell_value(cell_coordinates)
    
    raise Exception('Specified named cell "' + cell_name + '" does not exist.')

  def get_named_cell_values(self, cell_names=config['defined_cell_names']):
    return [self.get_named_cell_value(cell_name) for cell_name in cell_names]