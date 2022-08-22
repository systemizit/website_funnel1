# -*- coding: utf-8 -*-
from odoo import api, models, fields


class WebsitePage(models.Model):
    _inherit = 'website.page'

    is_funnel = fields.Boolean('Is a Funnel?')
