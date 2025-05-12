from odoo import models, fields, api
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website

from odoo.addons.base.models.ir_http import IrHttp

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


EXCLUDED_PATHS = [
    '/web/login',
    '/web/signup',
    '/web/reset_password',
    '/website/static/',
    '/web/static/',
    '/favicon.ico',
    '/robots.txt',
]

class IrHttpCustom(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls, endpoint):
        path = request.httprequest.path

        if any(path.startswith(p) for p in EXCLUDED_PATHS):
            return super()._dispatch(endpoint)

        if request.env.user._is_public():
            return request.redirect('/web/login?redirect=' + path)

        return super()._dispatch(endpoint)
