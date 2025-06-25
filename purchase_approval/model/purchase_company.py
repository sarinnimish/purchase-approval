from odoo import models,fields ,api
from odoo.exceptions import ValidationError

class PurchaseApproval(models.Model):
    _inherit = 'res.company'

    three_level_approval = fields.Boolean(string="Three Level Approval")
    approval_email_template= fields.Many2one('mail.template')
    refuse_email_template=fields.Many2one('mail.template')
    manager_approve_limit=fields.Float()
    finance_manager_approve_limit=fields.Float()
    director_approve_limit=fields.Float()

    manager_approve_limit_backup = fields.Float()
    finance_manager_approve_limit_backup = fields.Float()
    director_approve_limit_backup = fields.Float()


    @api.onchange('three_level_approval')
    @api.constrains('three_level_approval')
    def _onchange_three_level_approval(self):
        # import pdb; pdb.set_trace();
        for rec in self:
            if not rec.three_level_approval:
                rec.manager_approve_limit_backup = rec.manager_approve_limit
                rec.finance_manager_approve_limit_backup = rec.finance_manager_approve_limit
                rec.director_approve_limit_backup = rec.director_approve_limit

                rec.manager_approve_limit = 0.0
                rec.finance_manager_approve_limit = 0.0
                rec.director_approve_limit = 0.0
            else:
                rec.manager_approve_limit = rec.manager_approve_limit_backup
                rec.finance_manager_approve_limit = rec.finance_manager_approve_limit_backup
                rec.director_approve_limit = rec.director_approve_limit_backup

    @api.onchange('manager_approve_limit')
    def _onchange_manager_approve_limit(self):
        if self.manager_approve_limit != 0.0 and self.manager_approve_limit < 1000:
            raise ValidationError("Manager limit should be 0 or greater than or equal to 1000")

        if self.manager_approve_limit == self.finance_manager_approve_limit == self.director_approve_limit and self.manager_approve_limit != 0.0 and self.finance_manager_approve_limit !=0.0 and self.director_approve_limit !=0.0:
            raise ValidationError("Manager limit should not be equal to Finance Manager or Director limit")

        if self.finance_manager_approve_limit != 0.0 and self.manager_approve_limit != 0.0:
            if self.manager_approve_limit >= self.finance_manager_approve_limit:
                raise ValidationError("Manager limit must be less than Finance Manager limit")

        if self.director_approve_limit != 0.0 and self.manager_approve_limit != 0.0 and self.finance_manager_approve_limit == 0.0:
            if self.manager_approve_limit >= self.director_approve_limit:
                raise ValidationError("Manager limit must be less than Director limit when Finance Manager limit is 0")

    @api.onchange('finance_manager_approve_limit')
    def _onchange_finance_manager_approve_limit(self):
        # if self.finance_manager_approve_limit == self.manager_approve_limit or \
        #    self.finance_manager_approve_limit == self.director_approve_limit:
        #     raise ValidationError("Finance Manager limit should not be equal to Manager or Director limit")
        
        if self.manager_approve_limit == self.finance_manager_approve_limit == self.director_approve_limit and self.manager_approve_limit != 0.0 and self.finance_manager_approve_limit !=0.0 and self.director_approve_limit !=0.0:
            raise ValidationError("Finance Manager limit should not be equal to Manager or Director limit")

        if self.manager_approve_limit != 0.0 and self.finance_manager_approve_limit != 0.0:
            if self.finance_manager_approve_limit <= self.manager_approve_limit:
                raise ValidationError("Finance Manager limit must be greater than Manager limit")

        if self.director_approve_limit != 0.0 and self.finance_manager_approve_limit != 0.0:
            if self.finance_manager_approve_limit >= self.director_approve_limit:
                raise ValidationError("Finance Manager limit must be less than Director limit")

        if self.director_approve_limit != 0.0 and self.manager_approve_limit == 0.0:
            if self.finance_manager_approve_limit >= self.director_approve_limit:
                raise ValidationError("Finance Manager limit must be less than Director limit when Manager limit is 0")
        

    @api.onchange('director_approve_limit')
    def _onchange_director_approve_limit(self):
        # if self.director_approve_limit == self.manager_approve_limit or \
        #    self.director_approve_limit == self.finance_manager_approve_limit:
        #     raise ValidationError("Director limit should not be equal to Manager or Finance Manager limit")
        
        if self.manager_approve_limit == self.finance_manager_approve_limit == self.director_approve_limit and self.manager_approve_limit != 0.0 and self.finance_manager_approve_limit !=0.0 and self.director_approve_limit !=0.0:
            raise ValidationError("Director limit should not be equal to Finance Manager or Manager")

        if self.finance_manager_approve_limit != 0.0 and self.director_approve_limit != 0.0:
            if self.director_approve_limit <= self.finance_manager_approve_limit:
                raise ValidationError("Director limit must be greater than Finance Manager limit")

        if self.manager_approve_limit != 0.0 and self.director_approve_limit != 0.0 and self.finance_manager_approve_limit == 0.0:
            if self.director_approve_limit <= self.manager_approve_limit:
                raise ValidationError("Director limit must be greater than Manager limit when Finance Manager limit is 0")

    
            
                 
 