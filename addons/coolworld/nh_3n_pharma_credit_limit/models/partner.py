# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _

class ResPartner(models.Model):
    _inherit = "res.partner"
    _name = "res.partner"

    #branch_id=fields.Many2one('res.branch','Branch')
    over_credit = fields.Boolean('Allow Over Credit?')

