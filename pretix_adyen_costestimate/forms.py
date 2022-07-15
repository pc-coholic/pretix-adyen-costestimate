from django import forms
from django.utils.translation import gettext_lazy as _
from pretix.base.forms import SettingsForm


class AdyenEstimateSettingsForm(SettingsForm):
    adyen_estimate_interaction_channel = forms.ChoiceField(
        label=_('Shopper Interaction Channel'),
        required=True,
        choices=[
            ('Ecommerce', 'Ecommerce'),
            ('ContAuth', 'ContAuth'),
            ('Moto', 'Moto'),
            ('POS', 'POS'),
        ],
    )
