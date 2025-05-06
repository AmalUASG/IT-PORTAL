from odoo import models, fields, api
from odoo import http
from odoo.http import request
class BlogPostReport(models.AbstractModel):
    _name = 'report.uasg_custom_website_blog.report_blog_post'
    _description = 'Blog Post PDF Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        blog_post = self.env['blog.post'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'website.blog.post',
            'docs': blog_post,
        }



class ItDocumentsController(http.Controller):

    @http.route(['/it/documents'], type='http', auth='public', website=True)
    def list_it_documents(self, **kwargs):
        documents = request.env['it.documents'].sudo().search([('active', '=', True)])
        return request.render('uasg_custom_website_blog.website_it_documents', {
            'documents': documents
        })
