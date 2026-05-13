from apps.core.models import (
    SystemSettings,
)


class SystemSettingsService:

    @staticmethod
    def get_settings():

        settings = (
            SystemSettings.objects.first()
        )

        if not settings:

            settings = (
                SystemSettings.objects.create()
            )

        return settings