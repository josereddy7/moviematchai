from django.urls import path, include

from .views import RegisterView

# Step 4: create url and include in projects urls file

urlpatterns = [
    path("", include('django.contrib.auth.urls')),
    path("register/", RegisterView.as_view(), name="register"),
]