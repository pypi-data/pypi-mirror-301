from uuid import uuid1
from django.conf import settings
from django.contrib import auth
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView


class HomeView(View):
    def get(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        user = request.user
        if not user.is_authenticated:
            return redirect("jauth-example-login")
        return render(request, "jauth_example/home.html")


class LoginView(TemplateView):
    template_name = "jauth_example/login.html"

    def get_context_data(self, **kw):  # pylint: disable=unused-argument
        request = self.request
        assert isinstance(request, HttpRequest)
        cx = {
            "uuid": uuid1().hex,
            "account_kit_redirect_url": settings.ACCOUNT_KIT_REDIRECT_URL,
            "account_kit_app_id": settings.ACCOUNT_KIT_APP_ID,
            "facebook_app_id": settings.FACEBOOK_APP_ID,
            "facebook_redirect_url": settings.FACEBOOK_REDIRECT_URL,
            "google_app_id": settings.GOOGLE_APP_ID,
            "google_redirect_url": settings.GOOGLE_REDIRECT_URL,
            "error": request.GET.get("error", ""),
        }
        for k, v in kw.items():
            if v:
                cx[k] = v
        return cx


class LogoutView(View):
    def get(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        auth.logout(request)
        return redirect(reverse("jauth-example-login"))
