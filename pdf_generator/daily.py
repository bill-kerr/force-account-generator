from itertools import zip_longest
from page import PageCollection, Page
from paginator import simple_paginate

class DailyPage(Page):
    def __init__(self, labor, equipment, )


class DailyCollection(PageCollection):
    def __init__(self, data_loader, field_config):
        super().__init__(data_loader, field_config)
        self.__paginated_labor = simple_paginate(
            data_loader.labor,
            field_config.daily_config.labor_row_count)
        self.__paginated_equipment = simple_paginate(
            data_loader.equipment,
            field_config.daily_config.equipment_row_count)
        self.__create_pages()

    def __create_pages(self):
        if len(self.__paginated_labor) == 0 and len(self.__paginated_equipment) == 0:
            return
