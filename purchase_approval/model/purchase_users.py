from odoo import models,fields ,api

class UserApproval(models.Model):
    _inherit = 'res.users'

    director=fields.Float()
    finance_manager=fields.Float()
    manager=fields.Float()
    user=fields.Float()

