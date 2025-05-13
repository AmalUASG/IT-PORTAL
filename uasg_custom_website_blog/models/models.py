from odoo import models, fields, api
from odoo.exceptions import ValidationError
import mimetypes
import os
import base64


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

    name = fields.Char(string="Title", required=True, tracking=True)
    document_type_id = fields.Many2one('it.document.type', string="Document Type", required=True, tracking=True)
    description = fields.Text(string="Description")
    
    document_file = fields.Binary(string="Document File", attachment=True)
    file_name = fields.Char(string="Filename", tracking=True)
    mimetype = fields.Char(string="MIME Type", compute="_compute_mimetype", store=True)

    responsible_user_id = fields.Many2one('res.users', string="Responsible User", tracking=True)
    active = fields.Boolean(default=True)
    date_created = fields.Date(string="Date Created", default=fields.Date.context_today, readonly=True)
    date_modified = fields.Datetime(string="Last Modified", readonly=True)

    @api.depends('file_name')
    def _compute_mimetype(self):
        for record in self:
            if record.file_name:
                record.mimetype = mimetypes.guess_type(record.file_name)[0] or 'application/octet-stream'
            else:
                record.mimetype = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Auto-fix file extension if missing
            if vals.get('document_file') and vals.get('file_name'):
                if not os.path.splitext(vals['file_name'])[1]:
                    vals['file_name'] += '.docx'
        records = super(ItDocuments, self).create(vals_list)
        records.write({'date_modified': fields.Datetime.now()})
        return records

    def write(self, vals):
        # Auto-fix file extension on update
        if vals.get('document_file') and vals.get('file_name'):
            if not os.path.splitext(vals['file_name'])[1]:
                vals['file_name'] += '.docx'

        vals['date_modified'] = fields.Datetime.now()
        return super(ItDocuments, self).write(vals)

    @api.constrains('document_file', 'file_name')
    def _check_file_name(self):
        for record in self:
            if record.document_file and not record.file_name:
                raise ValidationError("Please provide a filename when uploading a document.")
