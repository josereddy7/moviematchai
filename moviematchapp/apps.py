from django.apps import AppConfig


class MoviematchappConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'moviematchapp'
