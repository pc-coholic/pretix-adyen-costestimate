from django.dispatch import receiver
from django.http import HttpRequest, HttpResponse
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _
from pretix.base.middleware import _merge_csp, _parse_csp, _render_csp
from pretix.base.settings import settings_hierarkey
from pretix.control.signals import nav_event_settings
from pretix.presale.signals import process_response
from pretix_adyen.payment import AdyenSettingsHolder


@receiver(signal=process_response, dispatch_uid="adyen_costestimate_middleware_resp")
def signal_process_response(sender, request: HttpRequest, response: HttpResponse, **kwargs):
    provider = AdyenSettingsHolder(sender)
    url = resolve(request.path_info)

    if url.url_name == 'estimate':
        if 'Content-Security-Policy' in response:
            h = _parse_csp(response['Content-Security-Policy'])
        else:
            h = {}

        sources = ['frame-src', 'style-src', 'script-src', 'img-src', 'connect-src']

        env = 'test' if sender.testmode else provider.settings.prod_env

        csps = {src: ['https://checkoutshopper-{}.adyen.com'.format(env)] for src in sources}

        # Adyen unfortunately applies styles through their script-src
        # Also, the unsafe-inline needs to specified within single quotes!
        csps['style-src'].append("'unsafe-inline'")

        _merge_csp(h, csps)

        if h:
            response['Content-Security-Policy'] = _render_csp(h)
    return response


@receiver(nav_event_settings, dispatch_uid="adyen_costestimate_nav_event_settings")
def navbar_info(sender, request, **kwargs):
    url = resolve(request.path_info)
    if not request.user.has_event_permission(
        request.organizer, request.event, "can_change_event_settings", request=request
    ):
        return []
    return [
        {
            "label": _("Adyen Cost Estimate"),
            "url": reverse(
                "plugins:pretix_adyen_costestimate:settings",
                kwargs={
                    "event": request.event.slug,
                    "organizer": request.organizer.slug,
                },
            ),
            "active": url.namespace == "plugins:pretix_adyen_costestimate",
        }
    ]


settings_hierarkey.add_default("adyen_estimate_interaction_channel", "POS", str)
