from django.db import models
from users.models import UserAccount

# Create your models here.
class Banks(models.Model):
    accountId = models.CharField(max_length=2000)
    bankId = models.CharField(max_length=2000)
    accessToken = models.CharField(max_length=2000)
    fundingSourceUrl = models.CharField(max_length=2000)
    shareableId = models.CharField(max_length=2000)
    users = models.ForeignKey(UserAccount, db_column='users_id', on_delete = models.CASCADE, related_name='banks')

    def getAccountId(self):
        return self.accountId
    
    def getBankId(self):
        return self.bankId
    
    def getAccessToken(self):
        return self.accessToken
    
    def getFundingSourceUrl(self):
        return self.fundingSourceUrl
    
    def getShareableId(self):
        return self.shareableId
    
    def getUser(self):
        return(self.users)