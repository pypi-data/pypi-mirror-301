from django.urls import path

from jauth.views import FacebookRedirectView, FacebookDeauthorizeView, FacebookDeleteView, GoogleRedirectView
from jauth_example.views import HomeView, LoginView, LogoutView


urlpatterns = [
    path("", HomeView.as_view(), name="jauth-example-home"),
    path("accounts/login", LoginView.as_view(), name="jauth-example-login"),
    path("accounts/logout", LogoutView.as_view(), name="jauth-example-logout"),
    path("accounts/facebook-redirect", FacebookRedirectView.as_view(), name="jauth-example-facebook-redirect"),
    path("accounts/facebook-deauthorize", FacebookDeauthorizeView.as_view(), name="jauth-example-facebook-deauthorize"),
    path("accounts/facebook-delete", FacebookDeleteView.as_view(), name="jauth-example-facebook-delete"),
    path("accounts/google-redirect", GoogleRedirectView.as_view(), name="jauth-example-google-redirect"),
]
