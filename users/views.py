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
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def custom_login_view(request):
    if request.method == 'POST':
        # Extract email and password from POST request
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user using email and password
        user = authenticate(request, email=email, password=password)
        print('custom_login_authenticate', user)
        
        if user is not None:
            # User is authenticated, so log them in
            login(request, user)

            # At this point, request.user.is_authenticated will be True
            return JsonResponse({'message': 'Login successful', 'user': user.email})

        else:
            # Invalid credentials
            return JsonResponse({'error': 'Invalid email or password'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
from django.http import JsonResponse


def is_authenticated_view(request):
    if request.user.is_authenticated:
        return JsonResponse({'message': 'User is authenticated', 'email': request.user.email})
    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)
    
class CustomTokenObtainPairView(TokenObtainPairView):  
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # authenticateUser = custom_login_view(request)
            # print('jwt/create/ authenticate user: ', authenticateUser)
            # print('isAuth', is_authenticated_view(request))
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
       
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
        # out = {'response': response,
        #        'cookies': response.COOKIES}
        return response



class CustomTokenRefreshView(TokenRefreshView):
    authentication_classes = [JWTAuthentication]  # Add authentication
    permission_classes = [IsAuthenticated]

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
            print(response.cookies)

        return response


class CustomTokenVerifyView(TokenVerifyView):
    authentication_classes = [JWTAuthentication]  # Add authentication
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')

        if access_token:
            request.data['token'] = access_token

        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]  # Add authentication
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
