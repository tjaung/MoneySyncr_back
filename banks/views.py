from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import BankSerializer
from .plaid_client import api_client
from .models import Banks, UserAccount

# Create your views here.
# Bank views
class BankListCreate(generics.ListCreateAPIView):
    queryset = Banks.objects.all()
    serializer_class = BankSerializer

class BankDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banks.objects.all()
    serializer_class = BankSerializer

#Plaid linktoken
class CreateLinkTokenView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')  # Get the user ID from the request
        try:
            response = api_client.LinkToken.create({
                'user': {
                    'client_user_id': user_id,
                },
                'products': ['auth', 'transactions'],  # Specify the products you want to use
                'client_name': 'Your App Name',
                'country_codes': ['US'],
                'language': 'en',
            })
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# exchange linktoken
class ExchangePublicTokenView(APIView):
    def post(self, request):
        public_token = request.data.get('public_token')
        user_id = request.data.get('user_id')  # Optionally get the user ID to link with your database
        try:
            response = api_client.Item.public_token.exchange(public_token)
            access_token = response['access_token']
            # Store access_token in your UserAccount model
            user = UserAccount.objects.get(id=user_id)
            user.plaid_access_token = access_token  # Make sure to add this field in your UserAccount model
            user.save()
            return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# 