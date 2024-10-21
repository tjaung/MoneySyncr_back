from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from rest_framework import exceptions

UserAccount = get_user_model()
class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        print(request)
        try:
            # Check if token is passed via Authorization header
            header = self.get_header(request)
            print(request)
            if header is not None:
                raw_token = self.get_raw_token(header)
                print('header not none: ', raw_token)
            else:
                # Fall back to checking for token in cookies
                raw_token = request.COOKIES.get('access')
                print('header none: ', raw_token)
            if raw_token is None:
                return None
            
            # Validate the token
            validated_token = self.get_validated_token(raw_token)

             # Get the users_id from the token payload
            user_id = validated_token.get('users_id')  # Change to users_id

            # Retrieve the user using users_id
            user = UserAccount.objects.get(users_id=user_id)  # Ensure you're using your UUID field
            print('custom jwt', user, validated_token)
            return user, validated_token
        except UserAccount.DoesNotExist:
            raise exceptions.AuthenticationFailed('User does not exist.')
        except Exception as e:
            print(f"Authentication error: {str(e)}")  # Log error for debugging
            return None