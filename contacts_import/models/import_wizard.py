from odoo import models, fields, api
import base64
import csv
import io

class CSVImportWizard(models.TransientModel):
    _name = 'csv.import.wizard'

    csv_file = fields.Binary(string='CSV File', required=True)
    file_name = fields.Char(string='File Name')

    def import_csv(self):
        self.ensure_one() 

        # decode the file
        data = base64.b64decode(self.csv_file)
        file = io.StringIO(data.decode("UTF-8"))
        reader = csv.reader(file, delimiter=',', quotechar='"')

        # extract headers
        headers = next(reader)
        ResPartner = self.env['res.partner']

        for row in reader:
            vals = dict(zip(headers, row))
            # separate individual and company data
            individual_vals = {k: v for k, v in vals.items() if 'individual' in k}
            company_vals = {k: v for k, v in vals.items() if 'company' in k}

            # search for existing company
            company = ResPartner.search([('name', '=', company_vals.get('company_name'))], limit=1)
            if not company:
                # create company if not exists
                company = ResPartner.create({
                    'name': company_vals.get('company_name'),
                    'is_company': True,
                    'customer_rank': 1,
                    # add additional company fields here
                })
                
            # create individual
            individual = ResPartner.create({
                'name': individual_vals.get('individual_name'),
                'parent_id': company.id,
                'customer_rank': 1,
                # add additional individual fields here
            })
