from django.urls import path, re_path

from account.views import *


urlpatterns = [
    path("sign-up", SignUpAPIView.as_view()),
    path("sign-in", SignInAPIView.as_view()),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
