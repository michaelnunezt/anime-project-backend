from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from account.serializers import *
from account.service import get_tokens_for_user
from shared.Enums import ProjectEnum
from shared.view_models.custom_responses import APIResponse
from http import HTTPStatus


# Create your views here.
class SignUpAPIView(APIView):
    def post(self, request):
        try:
            srlz = SignUpSerializer(data=request.data)

            if srlz.is_valid():
                srlz.save()
                return Response(APIResponse.success(project=ProjectEnum.ACCOUNT, message="Sing-Up successful!").to_dict())

            else:
                return Response(APIResponse.error(project=ProjectEnum.ACCOUNT,
                                                  message="Failed to sign up user",
                                                  error=srlz.errors).to_dict(), status=HTTPStatus.UNPROCESSABLE_ENTITY)
        except Exception as error:
            return Response(APIResponse.error(project=ProjectEnum.ACCOUNT,
                                              message="Failed to sign up user",
                                              error=str(error)).to_dict(), status=HTTPStatus.BAD_REQUEST)


class SignInAPIView(APIView):
    def post(self, request):
        try:
            singin_srlz = SingInSerializer(data=request.data)
            if singin_srlz.is_valid():
                user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
                if user:
                    refresh_token = get_tokens_for_user(user)
                    return Response(APIResponse.success(
                        project=ProjectEnum.ACCOUNT,
                        data={
                            "refresh": str(refresh_token),
                            "access": str(refresh_token.access_token)
                        }
                    ).to_dict())
                else:
                    return Response(APIResponse.error(
                        project=ProjectEnum.ACCOUNT,
                        message="Failed to sign in user",
                        error="Username or password not valid"
                    ).to_dict(), status=HTTPStatus.UNAUTHORIZED)
        except Exception as error:
            return Response(APIResponse.error(project=ProjectEnum.ACCOUNT,
                                              message="Failed to sign in user",
                                              error=str(error)).to_dict(), status=HTTPStatus.BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom Token Refresh API to return the response in a consistent format.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Handle valid and invalid responses
        if response.status_code == 200:
            return Response(APIResponse.success(
                project=ProjectEnum.ACCOUNT,
                data=response.data,
                message="Token refreshed successfully."
            ).to_dict())
        else:
            return Response(APIResponse.error(
                project=ProjectEnum.ACCOUNT,
                message="Token refresh failed.",
                error=response.data
            ).to_dict(), status=HTTPStatus.BAD_REQUEST)

