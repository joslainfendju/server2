# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseTeam(models.Model):
    _name = "expense.team"
    _description = "Expense Team"

    active = fields.Boolean('Active', default=True)

    name = fields.Char('Name')

    user_id = fields.Many2one(
        comodel_name='res.users', string='Team Leader',
        default=lambda self: self.env.user, required=True, index=True)

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        required=True, index=True, default=lambda self: self.env.user.company_id)

    lock_amount_total = fields.Boolean(
        string="Lock Amount Total",
        help="Prevent changes of amount total if approval route generated"
    )

    approver_ids = fields.One2many(
        comodel_name="expense.team.approver", inverse_name='team_id', string='Approvers')

    @api.constrains('company_id')
    def _check_company(self):
        for team in self:
            if team.company_id.expense_approval_route == 'no':
                raise UserError(_('Approval Route functionality is disabled for the company %s') % team.company_id.name)


class ExpenseTeamApprover(models.Model):
    _name = "expense.team.approver"
    _description = "Expense Team Approver"
    _order = 'sequence'
    _rec_name = 'user_id'

    sequence = fields.Integer(string='Sequence', default=10)

    team_id = fields.Many2one(
        comodel_name='expense.team', string='Team',
        required=True, ondelete='cascade')

    user_id = fields.Many2one(
        comodel_name='res.users', string='Approver',
        required=True)

    role = fields.Char('Role/Position', required=True, default="Approver")

    min_amount = fields.Monetary(
        string="Minimum Amount",
        currency_field='company_currency_id', readonly=False,
        help="Minimum amount for which a validation by approver is required")

    company_currency_id = fields.Many2one(
        comodel_name='res.currency', string="Company Currency",
        related='team_id.company_id.currency_id', readonly=True,
        help='Utility field to express threshold currency')

    lock_amount_total = fields.Boolean(
        string="Lock Amount Total",
        help="Prevent changes of amount total if Expense approved by this user"
    )

    @api.onchange('user_id')
    def _detect_user_role(self):
        for approver in self:
            # if user related to employee, try to get job title for hr.employee
            employee = hasattr(approver.user_id, 'employee_ids') and getattr(approver.user_id, 'employee_ids')
            employee_job_id = hasattr(employee, 'job_id') and getattr(employee, 'job_id')
            employee_job_title = employee_job_id.name if employee_job_id else False
            if employee_job_title:
                approver.role = employee_job_title
                continue
            # if user related partner, try to get job title for res.partner
            partner = approver.user_id.partner_id
            partner_job_title = hasattr(partner, 'function') and getattr(partner, 'function')
            if partner_job_title:
                approver.role = partner_job_title

    def write(self, vals):
        if vals == {}:
            return True
        return super(ExpenseTeamApprover, self).write(vals)


class ExpenseSheetApprover(models.Model):
    _name = "hr.expense.sheet.approver"
    _description = "Expense Approver"

    _inherits = {'expense.team.approver': 'team_approver_id'}

    team_approver_id = fields.Many2one(
        comodel_name='expense.team.approver', string='Expense Team Approver',
        required=True)

    expense_sheet_id = fields.Many2one(
        comodel_name='hr.expense.sheet', string='Expense',
        required=True, ondelete='cascade')

    state = fields.Selection(
        selection=[
            ('to approve', 'To Approve'),
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ], string='Status', readonly=True, required=True, default='to approve')
