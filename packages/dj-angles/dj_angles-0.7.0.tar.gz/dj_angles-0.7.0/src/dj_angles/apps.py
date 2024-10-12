import re
from contextlib import suppress

import django.contrib.admin
import django.template
from dj_app import AppInstaller
from django.apps import AppConfig
from django.conf import settings


class DjAnglesConfig(AppConfig):
    """ """

    name = "dj_angles"
    default = True

    def ready(self):
        pass


class DJAnglesInstaller(AppInstaller):
    name = "dj-angles"
    module_name = "dj_angles"

    def update_settings(self, settings: Dict) -> None:
        templates = settings.get("TEMPLATES", [])

        if self.is_module_available:
            if len(templates) > 0:
                template = templates[0]  # TODO: Only get the Django template?

                if "APP_DIRS" in template:
                    del template["APP_DIRS"]

                template["OPTIONS"]["loaders"] = [
                    "dj_angles.template_loader.Loader",
                    "django.template.loaders.filesystem.Loader",
                    "django.template.loaders.app_directories.Loader",
                ]
