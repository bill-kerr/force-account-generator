class Config:
    worksheet_names = {
        'summary': 'FINAL SUMMARY',
        'material': 'MATERIAL BD',
        'labor': 'LABOR',
        'equipment': 'EQUIPMENT',
        'rentals_and_services': 'RENTALS & SBO',
        'consumables': 'CONSUMABLES'
    }

    defined_cells = {
        'county': 'COUNTY',
        'state_route': 'SR',
        'section': 'SEC',
        'work_order_number': 'WO_NO',
        'contract': 'CONTRACT',
        'item_number': 'ITEM_NO',
        'prime_contractor': 'PRIME_CONTRACTOR',
        'statement_of_cost': 'STATEMENT_OF_COST',
        'sales_tax': 'MB_SALES_TAX_RATE',
        'social_security_tax_rate': 'SS_TAX',
        'medicare_tax_rate': 'MEDICARE_TAX',
        'unemployment_tax_rate': 'UNEMPLOYMENT_TAX',
        'workers_comp_insurance_rate': 'WORKERS_COMP',
        'liability_insurance_rate': 'LIABILITY_INSURANCE'
    }

    check_columns = {
        'material': [0],
        'labor': [0],
        'equipment': [0],
        'rentals_and_services': [0, 1],
        'consumables': [0, 1]
    }
