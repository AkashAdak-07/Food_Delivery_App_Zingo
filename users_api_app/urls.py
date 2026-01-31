# from django.urls import path
# from .views import (
#     register_user,
#     activate_user,
#     login_user,
#     verify_login_otp
# )

# urlpatterns = [
#     path("register/", register_user, name="register"),
#     path("activate/<uidb64>/<token>/", activate_user, name="activate"),
#     path("login/", login_user, name="login"),
#     path("verify-otp/", verify_login_otp, name="verify-otp"),
# ]

from django.urls import path
from .views import (
    register_user,
    verify_registration_otp,
    login_user,
    verify_login_otp,
)

urlpatterns = [
    path("register/", register_user),
    path("register/verify-otp/", verify_registration_otp),
    path("login/", login_user),
    path("login/verify-otp/", verify_login_otp),
]
