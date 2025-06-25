from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    manager_approval = fields.Many2one('res.users', string="Manager Approval")
    finance_manager_approval = fields.Many2one('res.users', string="Finance Manager Approval")
    director_approval = fields.Many2one('res.users', string="Director Approval")
    manager_approval_date = fields.Date(string="Manager Approval Date")
    finance_manager_approval_date = fields.Date(string="Finance Manager Approval Date")
    director_approval_date = fields.Date(string="Director Approval Date")

    purchase_manager = fields.Many2one('res.users', string="Purchase Manager")
    finance_manager = fields.Many2one('res.users', string="Finance Manager")
    director_manager = fields.Many2one('res.users', string="Director Manager")

    refused_by = fields.Many2one('res.users', string="Refused By")
    refuse_date = fields.Date(string="Refused Date")
    refuse_reason = fields.Text(string="Refused Reason")

    state = fields.Selection(selection_add=[
        ('waiting finance approval', 'Waiting Finance Approval'),
        ('waiting director approval', 'Waiting Director Approval'),
    ], tracking=True, readonly=True, ondelete={'waiting finance approval': 'cascade'})
    


    # hide_fields = fields.Boolean(
    #     compute='_compute_hide_fields', string="Hide Fields", store=False
    # )

    # @api.depends('three_level_approval')
    # def _compute_hide_fields(self):
    #     for record in self:
    #         record.hide_fields = not record.three_level_approval


    def button_confirm(self):
        """Send an email notification to the Purchase Manager."""
        res = super(PurchaseOrder, self).button_confirm()
   
        
        if (self.company_id.manager_approve_limit == 0 and
            self.company_id.finance_manager_approve_limit == 0 and
            self.company_id.director_approve_limit == 0):
            self.state = 'purchase'
            return res
        
        if self.amount_total < 1000:
            self.state = 'purchase'

        if self.amount_total < self.company_id.manager_approve_limit :
            self.state = 'purchase'

        if self.amount_total > self.company_id.manager_approve_limit and self.amount_total < self.company_id.finance_manager_approve_limit :
            self.state = 'to approve'
        
        if self.amount_total > self.company_id.manager_approve_limit:
            self.state = 'to approve'

        if self.company_id.manager_approve_limit == 0.0:
            self.state = 'waiting finance approval'
        
        if self.company_id.manager_approve_limit == 0.0 and self.company_id.finance_manager_approve_limit == 0:
            self.state = 'waiting director approval'

        template = self.env.ref('purchase_approval.email_template_purchase_manager_notification')
        if template:
            template.send_mail(self.id, force_send=True)
            self.message_post(
                    body="An email notification has been sent to the Purchase Manager for approval.",
                    subtype_xmlid="mail.mt_note"
                )

        return res

    
    def button_manager_approve(self):
        """Manager approves the purchase order."""
        self.ensure_one()
        if  self.amount_total < self.company_id.finance_manager_approve_limit and self.amount_total > self.company_id.manager_approve_limit:
            self.state = 'purchase'
            self.manager_approval = self.env.user.id
            self.purchase_manager = self.env.user.id
            self.manager_approval_date = date.today() 
        
        if  self.amount_total >self.company_id.finance_manager_approve_limit and self.amount_total > self.company_id.manager_approve_limit:
            self.state = 'waiting finance approval'
            self.manager_approval = self.env.user.id
            self.purchase_manager = self.env.user.id
            self.manager_approval_date = date.today() 

        if self.company_id.finance_manager_approve_limit == 0.0 and self.company_id.director_approve_limit == 0.0 and self.amount_total > self.company_id.manager_approve_limit :
            self.state = 'purchase'
            self.manager_approval = self.env.user.id
            self.purchase_manager = self.env.user.id
            self.manager_approval_date = date.today() 
        
        if self.company_id.finance_manager_approve_limit == 0.0 and self.amount_total > self.company_id.manager_approve_limit and self.amount_total < self.company_id.director_approve_limit:
            self.state='purchase'
            self.manager_approval = self.env.user.id
            self.purchase_manager = self.env.user.id
            self.manager_approval_date = date.today() 
        
        if self.company_id.finance_manager_approve_limit == 0.0 and self.amount_total > self.company_id.manager_approve_limit and self.amount_total > self.company_id.director_approve_limit and self.company_id.director_approve_limit !=0.0:
            self.state='waiting director approval'
            self.manager_approval = self.env.user.id
            self.purchase_manager = self.env.user.id
            self.manager_approval_date = date.today()
        
        if self.company_id.finance_manager_approve_limit == self.amount_total:
            self.state='purchase'
            self.manager_approval = self.env.user.id
            self.purchase_manager = self.env.user.id
            self.manager_approval_date = date.today()
          
        template = self.env.ref('purchase_approval.email_template_finance_manager_notification')
        if template:
            template.send_mail(self.id, force_send=True)
        self.message_post(
                body="Now an email notification has been sent to the Finance Manager for approval.",
                subtype_xmlid="mail.mt_note"
            )  
       

    def button_finance_approve(self):
        # import pdb; pdb.set_trace();
        """Finance Manager approves the purchase order."""
        self.ensure_one()
        if self.amount_total < self.company_id.director_approve_limit:
            self.state = 'purchase'
            self.finance_manager_approval = self.env.user.id
            self.finance_manager = self.env.user.id
            self.finance_manager_approval_date = date.today()
        
        if self.company_id.director_approve_limit == 0.0 and self.amount_total > self.company_id.finance_manager_approve_limit:
            self.state = 'purchase'
            self.finance_manager_approval = self.env.user.id
            self.finance_manager = self.env.user.id
            self.finance_manager_approval_date = date.today()

        if self.company_id.director_approve_limit == 0.0 and self.company_id.manager_approve_limit == 0.0 and self.amount_total >= self.company_id.finance_manager_approve_limit:
            self.state = 'purchase'
            self.finance_manager_approval = self.env.user.id
            self.finance_manager = self.env.user.id
            self.finance_manager_approval_date = date.today()

        if self.company_id.director_approve_limit != 0.0 and self.amount_total > self.company_id.director_approve_limit:
            self.state = 'waiting director approval'
            self.finance_manager_approval = self.env.user.id
            self.finance_manager = self.env.user.id
            self.finance_manager_approval_date = date.today()
        
        if self.company_id.director_approve_limit == self.amount_total:
            self.state='purchase'
            self.manager_approval = self.env.user.id
            self.purchase_manager = self.env.user.id
            self.manager_approval_date = date.today()

        template = self.env.ref('purchase_approval.email_template_director_notification')
        if template:
            template.send_mail(self.id, force_send=True)
        self.message_post(
                body="Now an email notification has been sent to the Director Manager for approval.",
                subtype_xmlid="mail.mt_note"
            )
        

    def button_director_approve(self):
        """Director approves the purchase order."""
        self.ensure_one()
        if self.state == 'waiting director approval':
            self.state = 'purchase'
            self.director_approval = self.env.user.id
            self.director_manager = self.env.user.id
            self.director_approval_date = date.today()
            template = self.env.ref('purchase_approval.email_template_director_approved_notification')
            if template:
                template.send_mail(self.id, force_send=True)
            self.message_post(
                body="Now an email notification has been sent to the User for the approved order.",
                subtype_xmlid="mail.mt_note"
            )
        else:
            raise ValidationError("Director cannot approve this order. It exceeds their approval limit.")
   

  



    




