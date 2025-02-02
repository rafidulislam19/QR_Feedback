from django.apps import AppConfig


class FeedbacksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feedbacks'

    def ready(self) -> None:
        import feedbacks.signals
