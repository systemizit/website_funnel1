odoo.define('funnel.button.dynamic.snippet', function (require) {
    'use strict';
    const publicWidget = require('web.public.widget');

    publicWidget.registry.funnel_buttons_dynamic_snippet = publicWidget.Widget.extend({
        selector: '.funnel_buttons',
        start: function () {
            const self = this;
            const productId = this.$el[0].dataset.productId;
            const productQty = this.$el[0].dataset.productQty;
            const successRedirect = this.$el[0].dataset.successRedirect;
            const failureRedirect = this.$el[0].dataset.failureRedirect;
            const expressCheckout = this.$el[0].dataset.expressCheckout;

            this.$el.find('input.product_id').remove();
            this.$el.find('input.add_qty').remove();
            this.$el.find('input.success_redirect').remove();
            this.$el.find('input.failure_redirect').remove();
            this.$el.find('input.csrf_token').remove();

            if (expressCheckout == 'true') {
                this.$el.find('button#reject_offer').attr("formaction", '/shop/cart/reject_offer?express=1');
                this.$el.attr("action", '/shop/cart/accept_offer?express=1');
            }
            else {
                this.$el.attr("action", '/shop/cart/accept_offer');
                this.$el.find('button#reject_offer').attr("formaction", '/shop/cart/reject_offer');
            }

            self.$el.append("<input type=\"hidden\" class=\"product_id\" name=\"product_id\" value='" + productId +"'/>");
            self.$el.append("<input type=\"hidden\" class=\"add_qty\" name=\"add_qty\" value='" + productQty +"'/>");

            if (successRedirect) {
                self.$el.append("<input type=\"hidden\" class=\"success_redirect\" name=\"success_redirect\" value='" + successRedirect +"'/>");
            }
            if (failureRedirect) {
                self.$el.append("<input type=\"hidden\" class=\"failure_redirect\" name=\"failure_redirect\" value='" + failureRedirect +"'/>");
            }

            self.$el.append("<input type=\"hidden\" name=\"csrf_token\" value='" + odoo.csrf_token +"'/>");
            return this._super.apply(this, arguments);
        },
    });

});
