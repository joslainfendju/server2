from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'
    _name = 'product.category'

    code = fields.Char('code')
    property_valuation = fields.Selection([

        ('real_time', 'Automated'), ('manual_periodic', 'Manual'), ], string='Inventory Valuation', default='real_time',
        company_dependent=True, copy=True, required=True,
        help="""Manual: The accounting entries to value the inventory are not posted automatically.
        Automated: An accounting entry is automatically created to value the inventory when a product enters or leaves the company.
        """)