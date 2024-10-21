from django.shortcuts import render
from django.conf import settings
from rest_framework_simplejwt.views import ( 
    TokenObtainPairView, 
    TokenRefreshView, 
    TokenVerifyView)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserAccount
# Create your views here.
# overide jwt views


class CustomTokenObtainPairView(TokenObtainPairView):  
    def post(self, request, *args, **kwargs):
        print("Request Data:", request.data)
        response = super().post(request, *args, **kwargs)
        print(request, response)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            print("Access Token:", access_token)
            print("Refresh Token:", refresh_token)

            # Assuming you're also fetching the user for some logic
            user_email = request.data.get('email')
            user = UserAccount.objects.get(email=user_email)

            # Accessing the new users_id field
            print("User ID:", user.users_id)
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response



class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')

        if access_token:
            request.data['token'] = access_token

        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
