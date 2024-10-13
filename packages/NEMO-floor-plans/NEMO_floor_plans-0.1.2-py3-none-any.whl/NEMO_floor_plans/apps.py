from django.apps import AppConfig


class FloorPlansConfig(AppConfig):
    name = "NEMO_floor_plans"

    def ready(self):
        """
        This code will be run when Django starts.
        """
        pass
