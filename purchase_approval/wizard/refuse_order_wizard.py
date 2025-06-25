from odoo import models, fields, api

class PurchaseRefuseWizard(models.TransientModel):
    _name = 'purchase.refuse.wizard'
    _description = 'Purchase Refuse Wizard'

    refuse_reason = fields.Text(string="Refuse Reason", required=True)

    def refuse_approval(self):
        """Set the refusal reason and update the state of the purchase order."""
        active_id = self.env.context.get('active_id')
        if active_id:
            purchase_order = self.env['purchase.order'].browse(active_id)
            purchase_order.write({
                'state': 'cancel',  # Update the state to 'cancel' or any other state
                'refuse_reason': self.refuse_reason,
                'refused_by': self.env.user.id,
                'refuse_date': fields.Date.today(),
            })
            template = self.env.ref('purchase_approval.email_template_purchase_manager_refusal')
            if template:
                template.send_mail(self.id, force_send=True)
                purchase_order.message_post(
                    body=f"The purchase order has been refused with the reason: {self.refuse_reason}",
                    subtype_xmlid="mail.mt_note"
                )

   