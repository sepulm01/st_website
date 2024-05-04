from django.apps import AppConfig


class RobotConfig(AppConfig):
    name = 'robot'
    

    def ready(self):
        import robot.signals  # noqa




