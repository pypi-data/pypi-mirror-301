from django.conf import settings
from django.contrib import admin
from jauth.models import (
    FacebookAccessToken,
    FacebookUser,
    GoogleUser,
    GoogleAccessToken,
)


class JauthAdminBase(admin.ModelAdmin):
    pass


class FacebookAdmin(JauthAdminBase):
    pass


class GoogleAdmin(JauthAdminBase):
    pass


class FacebookUserAdmin(FacebookAdmin):
    raw_id_fields = [
        "user",
    ]


class GoogleUserAdmin(GoogleAdmin):
    raw_id_fields = [
        "user",
    ]


if hasattr(settings, "FACEBOOK_APP_ID") and settings.FACEBOOK_APP_ID:
    admin.site.register(FacebookUser, FacebookUserAdmin)
    admin.site.register(FacebookAccessToken, FacebookAdmin)
if hasattr(settings, "GOOGLE_APP_ID") and settings.GOOGLE_APP_ID:
    admin.site.register(GoogleUser, GoogleUserAdmin)
    admin.site.register(GoogleAccessToken, GoogleAdmin)

required_params = ["JAUTH_AUTHENTICATION_ERROR_REDIRECT", "JAUTH_AUTHENTICATION_SUCCESS_REDIRECT"]
for p in required_params:
    if not hasattr(settings, p):
        raise Exception("{} configuration missing".format(p))
