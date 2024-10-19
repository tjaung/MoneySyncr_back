from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            # Check if token is passed via Authorization header
            header = self.get_header(request)
            if header is not None:
                raw_token = self.get_raw_token(header)
            else:
                # Fall back to checking for token in cookies
                raw_token = request.COOKIES.get(settings.AUTH_COOKIE)

            if raw_token is None:
                return None

            # Validate the token
            validated_token = self.get_validated_token(raw_token)

            return self.get_user(validated_token), validated_token
        except Exception as e:
            print(f"Authentication error: {str(e)}")  # Log error for debugging
            return None
