from Adyen import AdyenError
from decimal import Decimal
from django.views.generic import TemplateView
from pretix.base.models import Event
from pretix.control.views.event import EventSettingsFormView, EventSettingsViewMixin
from pretix_adyen.payment import AdyenMethod

from pretix_adyen_costestimate.forms import AdyenEstimateSettingsForm


class AdyenEstimateView(TemplateView):
    template_name = 'pretix_adyen_costestimate/estimate.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['environment'] = (
            'test' if self.request.event.testmode else self.request.event.settings.get('payment_adyen_prod_env', 'live')
        )
        ctx['clientKey'] = (
            self.request.event.settings.get('payment_adyen_test_client_key', '') if self.request.event.testmode
            else self.request.event.settings.get('payment_adyen_prod_client_key', '')
        )
        return ctx

    def get(self, request, *args, **kwargs):
        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        if 'encrypted_carddata' in request.POST and 'price' in request.POST:
            pprov = AdyenMethod(request.event)
            pprov._init_api()
            try:
                rqdata = {
                    "amount": {
                        "value": pprov._decimal_to_int(Decimal(request.POST.get('price', '0.00'))),
                        "currency": request.event.currency,
                    },
                    "encryptedCardNumber": request.POST.get("encrypted_carddata"),
                    "shopperInteraction": request.event.settings.get('adyen_estimate_interaction_channel', 'POS'),
                    **pprov.api_kwargs
                }
                result = pprov.adyen.binlookup.get_cost_estimate(rqdata)
            except AdyenError as e:
                print(e)
            else:
                ctx = self.get_context_data()
                ctx['estimate'] = pprov._amount_to_decimal(result.message['costEstimateAmount']['value'])
                ctx['amount'] = request.POST.get('price', '0.00')
                return self.render_to_response(ctx)

        return super().get(request, args, kwargs)


class AdyenEstimateSettingsView(EventSettingsViewMixin, EventSettingsFormView):
    model = Event
    form_class = AdyenEstimateSettingsForm
    template_name = 'pretix_adyen_costestimate/settings.html'
    permission = 'can_change_settings'
