import werkzeug.urls
import werkzeug.utils
import werkzeug.wrappers
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.website.controllers.main import Website

from odoo import http, _
from odoo.http import request
from odoo.tools.json import scriptsafe as json_scriptsafe


class FunnelButtonsSnippet(http.Controller):

    @http.route(['/shop/cart/accept_offer'], type='http', auth="public", methods=['POST'], website=True)
    def accept_offer(self, product_id, add_qty=1, set_qty=0, success_redirect='', **kw):
        """This route is called when adding a product to cart (no options)."""
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        product_custom_attribute_values = None
        if kw.get('product_custom_attribute_values'):
            product_custom_attribute_values = json_scriptsafe.loads(kw.get('product_custom_attribute_values'))

        no_variant_attribute_values = None
        if kw.get('no_variant_attribute_values'):
            no_variant_attribute_values = json_scriptsafe.loads(kw.get('no_variant_attribute_values'))

        sale_order._cart_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values
        )

        if success_redirect:
            return request.redirect(success_redirect)

        if kw.get('express'):
            return request.redirect("/shop/checkout?express=1")

        return request.redirect("/shop/cart")

    @http.route(['/shop/cart/reject_offer'], type='http', auth="public", methods=['POST'], website=True)
    def reject_offer(self, failure_redirect='', **kw):
        if failure_redirect:
            return request.redirect(failure_redirect)

        if kw.get('express'):
            return request.redirect("/shop/checkout?express=1")

        return request.redirect("/shop/cart")


class WebsiteFunnel(Website):

    @http.route(['/website/pages', '/website/pages/page/<int:page>'], type='http', auth="user", website=True)
    def pages_management(self, page=1, sortby='url', search='', **kw):
        # only website_designer should access the page Management
        if not request.env.user.has_group('website.group_website_designer'):
            raise werkzeug.exceptions.NotFound()

        Page = request.env['website.page']
        searchbar_sortings = {
            'url': {'label': _('Sort by Url'), 'order': 'url'},
            'name': {'label': _('Sort by Name'), 'order': 'name'},
            'funnel': {'label': _('Sort by Funnel'), 'order': 'is_funnel desc'},
        }
        # default sortby order
        sort_order = searchbar_sortings.get(sortby, 'url')['order'] + ', website_id desc, id'

        domain = request.website.website_domain()
        if search:
            domain += ['|', ('name', 'ilike', search), ('url', 'ilike', search)]

        pages = Page.search(domain, order=sort_order)
        if sortby != 'url' or not request.env.user.has_group('website.group_multi_website'):
            pages = pages.filtered(pages._is_most_specific_page)
        pages_count = len(pages)

        step = 50
        pager = portal_pager(
            url="/website/pages",
            url_args={'sortby': sortby},
            total=pages_count,
            page=page,
            step=step
        )

        pages = pages[(page - 1) * step:page * step]

        values = {
            'pager': pager,
            'pages': pages,
            'search': search,
            'sortby': sortby,
            'searchbar_sortings': searchbar_sortings,
        }
        return request.render("website.list_website_pages", values)
