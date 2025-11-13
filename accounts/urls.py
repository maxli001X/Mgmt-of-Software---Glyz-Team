from django.urls import path

from .views import SignUpView, YaleLoginView, YaleLogoutView


app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", YaleLoginView.as_view(), name="login"),
    path("logout/", YaleLogoutView.as_view(), name="logout"),
]

