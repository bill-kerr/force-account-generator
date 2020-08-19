class PurchasedConsumable:
    def __init__(self):
        self.description = ""
        self.quantity = 0
        self.unit_price = 0
        self.invoice_number = ""

class StockConsumable:
    def __init__(self):
        self.description = ""
        self.invoice_value = 0
        self.percent_reimbursed = 0
        self.invoice_number = ""
