from django.apps import AppConfig


class UsersappConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'usersapp'
