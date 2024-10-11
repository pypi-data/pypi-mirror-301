"""App Configuration"""

# Django
from django.apps import AppConfig

# AA EVE Uni Core
from eunicore import __version__


class EUniCoreConfig(AppConfig):
    """App Config"""

    name = "eunicore"
    label = "eunicore"
    verbose_name = f"EVE Uni Core v{__version__}"
