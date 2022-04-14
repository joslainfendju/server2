# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    expense_approval_route = fields.Selection(related='company_id.expense_approval_route',
                                              string="Use Approval Route", readonly=True)

    team_id = fields.Many2one(
        comodel_name="expense.team", string="Expense Team", domain="[('company_id', '=', company_id)]",
        readonly=True, states={'draft': [('readonly', False)], 'submit': [('readonly', False)]}, ondelete="restrict"
    )

    approver_ids = fields.One2many(
        comodel_name="hr.expense.sheet.approver", inverse_name="expense_sheet_id", string="Approvers", readonly=True)

    current_approver = fields.Many2one(
        comodel_name="hr.expense.sheet.approver", string="Approver",
        compute="_compute_approver")

    next_approver = fields.Many2one(
        comodel_name="hr.expense.sheet.approver", string="Next Approver",
        compute="_compute_approver")

    is_current_approver = fields.Boolean(
        string="Is Current Approver", compute="_compute_approver"
    )

    lock_amount_total = fields.Boolean(
        string="Lock Amount Total", compute="_compute_approver"
    )

    state = fields.Selection([('submit', 'Submitted'),
                              ('to approve', 'To approve'),
                              ('approve', 'Approved'),
                              ('post', 'Posted'),
                              ('done', 'Paid'),
                              ('cancel', 'Refused')
                              ], string='Status', index=True, readonly=True, track_visibility='onchange', copy=False,
                             default='submit', required=True,
                             help='Expense Report State')

    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'total_amount' in init_values and self.amount_total != init_values.get('total_amount'):
            self._check_lock_amount_total()
        return super(ExpenseSheet, self)._track_subtype(init_values)

    @api.multi
    def button_approve(self):
        for expense in self:
            if not expense.team_id:
                # Do default behaviour if Expense Team is not set
                super(ExpenseSheet, expense).approve_expense_sheets()
            elif expense.current_approver:
                if expense.current_approver.user_id == self.env.user or self.env.user._is_superuser():
                    # If current user is current approver (or superuser) update state as "approved"
                    expense.current_approver.state = 'approved'
                    expense.message_post(body=_('Expense approved by %s') % self.env.user.name)
                    # Check is there is another approver
                    if expense.next_approver:
                        # Send request to approve is there is next approver
                        expense.send_to_approve()
                    else:
                        # If there is not next approval, than assume that approval is finished and send notification
                        expense.message_post_with_view(
                            'purchase_approval_route.order_approval',
                            composition_mode='mass_mail',
                            partner_ids=[(4, expense.create_uid.partner_id.id)],
                            auto_delete=True,
                            auto_delete_message=True,
                            parent_id=False,
                            subtype_id=self.env.ref('mail.mt_note').id)
                        # Do default behaviour to set state as "approve" and update date_approve
                        return super(ExpenseSheet, expense).approve_expense_sheets()

    def approve_expense_sheets(self):
        for expense in self:
            if expense.state not in ['draft', 'sent', 'submit']:
                continue

            if not expense.team_id:
                # Do default behaviour if PO Team is not set
                super(ExpenseSheet, expense).approve_expense_sheets()
            else:
                # Generate approval route and send expense to approve
                expense.generate_approval_route()
                if expense.next_approver:
                    # If approval route is generated and there is next approver mark the order "to approve"
                    expense.write({'state': 'to approve'})
                    # And send request to approve
                    expense.send_to_approve()
                else:
                    # If there are not approvers, do default behaviour and move expense to the "approve" state
                    super(ExpenseSheet, expense).approve_expense_sheets()

            if expense.employee_id.address_id not in expense.message_partner_ids:
                expense.message_subscribe([expense.employee_id.address_id.id])
        return True

    def generate_approval_route(self):
        """
        Generate approval route for order
        :return:
        """
        for order in self:
            if not order.team_id:
                continue
            if order.approver_ids:
                # reset approval route
                order.approver_ids.unlink()
            for team_approver in order.team_id.approver_ids:
                currency = order.team_id.company_id.currency_id
                date = fields.Date.today()
                min_amount = currency.with_context(date=date).compute(team_approver.min_amount, order.currency_id)
                if order.total_amount >= min_amount:
                    self.env['hr.expense.sheet.approver'].create({
                        'team_approver_id': team_approver.id,
                        'expense_sheet_id': order.id,
                    })

    @api.depends('approver_ids.state', 'approver_ids.lock_amount_total')
    def _compute_approver(self):
        for order in self:
            if not order.team_id:
                order.next_approver = False
                order.current_approver = False
                order.is_current_approver = False
                order.lock_amount_total = False
                continue
            next_approvers = order.approver_ids.filtered(lambda a: a.state == "to approve")
            order.next_approver = next_approvers[0] if next_approvers else False

            current_approvers = order.approver_ids.filtered(lambda a: a.state == "pending")
            order.current_approver = current_approvers[0] if current_approvers else False

            order.is_current_approver = (order.current_approver and order.current_approver.user_id == self.env.user) \
                                        or self.env.user._is_superuser()

            order.lock_amount_total = len(
                order.approver_ids.filtered(lambda a: a.state == "approved" and a.lock_amount_total)) > 0

    def send_to_approve(self):
        for order in self:
            if order.state != 'to approve' and not order.team_id:
                continue

            main_error_msg = _("Unable to send approval request to next approver.")
            if order.current_approver:
                reason_msg = _("The order must be approved by %s") % order.current_approver.user_id.name
                raise UserError("%s %s" % (main_error_msg, reason_msg))

            if not order.next_approver:
                reason_msg = _("There are no approvers in the selected Expense team.")
                raise UserError("%s %s" % (main_error_msg, reason_msg))
            # use sudo as purchase user cannot update hr.expense.sheet.approver
            order.sudo().next_approver.state = 'pending'
            # Now next approver became as current
            current_approver_partner = order.current_approver.user_id.partner_id
            if current_approver_partner not in order.message_partner_ids:
                order.message_subscribe([current_approver_partner.id])
            order.sudo(user=order.create_uid).message_post_with_view(
                'its_hr_expensel_route.request_to_approve',
                composition_mode='mass_mail',
                partner_ids=[(4, current_approver_partner.id)],
                auto_delete=True,
                auto_delete_message=True,
                parent_id=False,
                subtype_id=self.env.ref('mail.mt_note').id)

    def _check_lock_amount_total(self):
        msg = _('Sorry, you are not allowed to change Amount Total of Expense. ')
        for order in self:
            if order.state in ('draft', 'sent'):
                continue
            if order.lock_amount_total:
                reason = _('It is locked after received approval. ')
                raise UserError(msg + "\n\n" + reason)
            if order.team_id.lock_amount_total:
                reason = _('It is locked after generated approval route. ')
                suggestion = _('To make changes, cancel and reset expense to draft. ')
                raise UserError(msg + "\n\n" + reason + "\n\n" + suggestion)
