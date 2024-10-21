from .views import (
    BankListCreate,
    BankDetail,
    CreateLinkTokenView,
    ExchangePublicTokenView
)
from django.urls import path

urlpatterns = [
    path('banks/', BankListCreate.as_view(), name='banks-list-create'),  # List all banks and create new bank
    path('banks/<int:pk>/', BankDetail.as_view(), name='banks-detail'),  # Retrieve, update, delete specific bank
    path('plaid/create_link_token/', CreateLinkTokenView.as_view(), name='create_link_token'),
    path('plaid/exchange_public_token/', ExchangePublicTokenView.as_view(), name='exchange_public_token'),
]