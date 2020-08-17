class Hours:
    def __init__(self, date, primary_hours, secondary_hours):
        self.date = date
        self.primary_hours = primary_hours
        self.secondary_hours = secondary_hours
    
    def __repr__(self):
        return "Hours(" + self.date + ", " + str(self.primary_hours or 0) + "/" + str(self.secondary_hours or 0) + ")"
