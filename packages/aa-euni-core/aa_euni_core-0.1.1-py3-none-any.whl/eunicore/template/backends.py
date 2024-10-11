# Standard Library
import os

# Django
from django.template.backends.django import DjangoTemplates

# AA EVE Uni Core
import eunicore


class EUniDjangoTemplates(DjangoTemplates):
    def __init__(self, params):
        path = os.path.dirname(os.path.abspath(eunicore.__file__)) + "/templates"
        params = params.copy()
        dirs = params.get("DIRS", [])
        if path not in dirs:
            dirs.append(path)
        params["DIRS"] = dirs
        super().__init__(params)
