from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _name = 'product.template'

    family_id = fields.Many2one('product.family', 'Family')
    volume = fields.Float('Volume', help="The volume in m3.", digits=(32, 10))
    weight = fields.Float('Weight', help="The weight of the contents in Kg, not including any packaging, etc.",
                          digits=(32, 10))
    invoice_policy = fields.Selection(
        [('order', 'Ordered quantities'),
         ('delivery', 'Delivered quantities'),
         ], string='Invoicing Policy',
        help='Ordered Quantity: Invoice based on the quantity the customer ordered.\n'
             'Delivered Quantity: Invoiced based on the quantity the vendor delivered (time or deliveries).',
        default='delivery')

    purchase_method = fields.Selection([
        ('purchase', 'On ordered quantities'),
        ('receive', 'On received quantities'),
    ], string="Control Policy",
        help="On ordered quantities: control bills based on ordered quantities.\n"
             "On received quantities: control bills based on received quantity.", default="receive")

    type = fields.Selection([
        ('consu', _('Consumable')),
        ('service', _('Service')),
        ('product', 'Stockable Product')], string='Product Type', default='product', required=True,
        help='A stockable product is a product for which you manage stock. The "Inventory" app has to be installed.\n'
             'A consumable product, on the other hand, is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.\n'
             'A digital content is a non-material product you sell online. The files attached to the products are the '
             'one that are sold on '
             'the e-commerce such as e-books, music, pictures,... The "Digital Product" module has to be installed.')

    tracking = fields.Selection([
        ('serial', 'By Unique Serial Number'),
        ('lot', 'By Lots'),
        ('none', 'No Tracking')], string="Tracking", default='lot', required=True)

    property_valuation = fields.Selection([
        ('manual_periodic', 'Periodic (manual)'),
        ('real_time', 'Perpetual (automated)')], string='Inventory Valuation',
        company_dependent=True, copy=True, default='real_time',
        help="""Manual: The accounting entries to value the inventory are not posted automatically. Automated: An 
        accounting entry is automatically created to value the inventory when a product enters or leaves the 
        company.""")

    property_stock_valuation_account_id = fields.Many2one(
        'account.account', 'Stock Valuation Account', company_dependent=True,
        domain=[('deprecated', '=', False)],
        help="When real-time inventory valuation is enabled on a "
             "product, this account will hold the current value of the products.", )

    @api.multi
    def _get_product_accounts(self):
        """ Add the stock accounts related to product to the result of super()
        @return: dictionary which contains information regarding stock accounts and super (income+expense accounts)
        """
        accounts = super(ProductTemplate, self)._get_product_accounts()
        accounts.update({
            'stock_valuation': self.property_stock_valuation_account_id
                               or self.categ_id.property_stock_valuation_account_id,

        })
        return accounts
