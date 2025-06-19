from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
TokenObtainPairView, TokenRefreshView
)

urlpatterns = [
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("refresh", TokenRefreshView.as_view(), name="refresh"),
    path("view/protected", views.secret_view, name="protected"),
]