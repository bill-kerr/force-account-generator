class Worksheet:
  def __init__(self, worksheet):
    self.__worksheet = worksheet
    self.worksheet_name = self.__worksheet.title

  def __repr__(self):
    return 'Worksheet(' + self.worksheet_name + ')'

  def cell_value(self, cell_coordinates):
    return self.__worksheet[cell_coordinates].value
