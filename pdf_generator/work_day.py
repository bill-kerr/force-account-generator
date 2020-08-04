class WorkDay:
    def __init__(self, date):
        self.date = date
        self.__labor = []
        self.__equipment = []

    def __repr__(self):
        return 'WorkDay(' + self.date + ')'

    def add_labor(self, labor_id, unit, st_hours, ot_hours):
        self.__labor.append({
            'id': labor_id,
            'unit': unit,
            'st': st_hours,
            'ot': ot_hours
        })

    def add_equipment(self, equipment_id, unit, op_hours, sb_hours):
        self.__equipment.append({
            'id': equipment_id,
            'unit': unit,
            'op': op_hours,
            'sb': sb_hours
        })

    @property
    def labor_hours(self):
        return self.__labor

    @property
    def equipment_hours(self):
        return self.__equipment

    def paginate(self, labor_limit, equipment_limit):
        labor = []
        equipment = []

        for i, unit in enumerate(self.__labor):
            if i % labor_limit == 0:
                labor.append([])
            labor[-1].append(unit)

        for i, unit in enumerate(self.__equipment):
            if i % equipment_limit == 0:
                equipment.append([])
            equipment[-1].append(unit)

        return labor, equipment
