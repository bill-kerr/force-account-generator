class Config(object):
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

    columns = {
        'material': {
            'check': [0],
            'description': 1,
            'quantity': 2,
            'unit': 3,
            'unit_price': 4,
            'invoice_number': 5,
            'sales_tax': 7
        },
        'labor': {
            'check': [0],
            'classification': 1,
            'name': 2,
            'base_rate': 3,
            'hw_pension_rate': 4,
            'date_start': 10
        },
        'equipment': {
            'check': [0],
            'description': 2,
            'year': 3,
            'h_yr_sec_pg': 4,
            'monthly_rate': 5,
            'equip_adj': 6,
            'area_adj': 7,
            'operating_cost': 8,
            'date_start': 14
        },
        'rentals_and_services': {
            'check': [0, 1],
            'r_description': 3,
            'r_invoice_number': 4,
            'r_amount': 5,
            's_description': 7,
            's_invoice_number': 8,
            's_amount': 9
        },
        'consumables': {
            'check': [0, 1],
            'p_description': 3,
            'p_quantity': 4,
            'p_unit_price': 5,
            'p_invoice_number': 6,
            's_description': 9,
            's_invoice_value': 10,
            's_percent_reimbursed': 11,
            's_invoice_number': 12
        }
    }
