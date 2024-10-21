# plaid_client.py (create this file)
import plaid
from django.conf import settings
from plaid.api import plaid_api

configuration = plaid.Configuration(
  host='sandbox',
  api_key={
    'clientId': '62827976aec383001ac73eed', #settings.PLAID_CLIENT_ID,
    'secret': 'a161075216f831271dd0eae5a3fc95', #settings.PLAID_SANDBOX_SECRET,
    'plaidVersion': '2020-09-14'
  }
)
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)