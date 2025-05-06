from odoo import models, fields

class ItDocumentType(models.Model):
    _name = "it.document.type"
    _description = "IT Document Type"

    name = fields.Char(string="Type Name", required=True)
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)



class ItDocuments(models.Model):
    _name = "it.documents"
    _inherit = ['mail.thread']
    _description = "IT Documents"

    name = fields.Char(string="Title", required=True)
    document_type_id = fields.Many2one('it.document.type', string="Document Type", required=True)
    description = fields.Text(string="Description")
    document_file = fields.Binary(string="Document File")
    file_name = fields.Char(string="Filename")
    responsible_user_id = fields.Many2one('res.users', string="Responsible User")
    active = fields.Boolean(default=True)
    date_created = fields.Date(string="Date Created", default=fields.Date.context_today)
    date_modified = fields.Datetime(string="Last Modified", readonly=True)

    def write(self, vals):
        vals['date_modified'] = fields.Datetime.now()
        return super(ItDocuments, self).write(vals)