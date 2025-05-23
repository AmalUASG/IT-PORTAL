from odoo import models, fields, api
from odoo import http
import werkzeug
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





class BlogPDFReportController(http.Controller):

    @http.route(['/blog/post/pdf/<int:blog_id>'], type='http', auth='public', website=True)
    def generate_blog_pdf(self, blog_id, **kw):
        blog_post = request.env['blog.post'].sudo().browse(blog_id)

        if not blog_post.exists():
            return werkzeug.exceptions.NotFound()

        # Get the report action for your report
        report_action = request.env['ir.actions.report']._get_report_from_name(
            'uasg_custom_website_blog.report_blog_post_pdf'
        )

        # Correct usage: model name, and list of record IDs
        pdf_content, _ = report_action._render_qweb_pdf('uasg_custom_website_blog.report_blog_post_pdf', res_ids = blog_post.id)

        filename = (blog_post.name or "blog_post").replace(' ', '_') + ".pdf"

        return request.make_response(
            pdf_content,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', f'attachment; filename="{filename}"'),
            ]
        )

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
    '/web/image',
    '/favicon.ico',
    '/robots.txt',
]


class IrHttpCustom(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls, endpoint):  # Include 'args' to match Odoo's signature
        path = request.httprequest.path

        # Exclude asset-related paths to make sure they are not blocked
        if any(path.startswith(p) for p in EXCLUDED_PATHS) or path.startswith('/web/static') or path.startswith('/web/assets') or path.startswith('/website')  or  path.startswith('/auth_oauth'):
            return super()._dispatch(endpoint)

        user = request.env.user

        if not user or not user.ids:
            uid = request.session.uid or request.env.ref('base.public_user').id
            user = request.env['res.users'].browse(uid)

        # Exclude the login redirect for certain paths (like public pages or asset URLs)
        # You can add additional paths to this check as needed.
        if user._is_public() and not path.startswith('/web/login'):
            # return request.redirect('/web/login?redirect=' + path)
            return request.redirect('/web/login?redirect=' + path)

        return super()._dispatch(endpoint)
