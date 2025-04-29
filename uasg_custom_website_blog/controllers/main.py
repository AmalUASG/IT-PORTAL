from odoo import models, fields, api

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
