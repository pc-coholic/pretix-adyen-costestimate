from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = "1.0.0"


class PluginApp(PluginConfig):
    name = "pretix_adyen_costestimate"
    verbose_name = "Adyen Cost Estimate"

    class PretixPluginMeta:
        name = gettext_lazy("Adyen Cost Estimate")
        author = "Martin Gross"
        description = gettext_lazy("Allow customers to enter their card details and retrieve an approximate cost estimate for the transaction")
        visible = True
        version = __version__
        category = "FEATURE"
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = "pretix_adyen_costestimate.PluginApp"
