from django.conf.urls import url

from pretix_adyen_costestimate.views import AdyenEstimateSettingsView, AdyenEstimateView

urlpatterns = [
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/settings/adyen_estimate/$',
        AdyenEstimateSettingsView.as_view(), name='settings'),
]

event_patterns = [
    url(r'^adyen_estimate/$', AdyenEstimateView.as_view(), name='estimate'),
]
