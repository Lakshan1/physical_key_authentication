from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Users(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    PKA = models.BooleanField(default=False)
    unique_id = models.UUIDField(default=uuid.uuid4,editable=False,null=True,blank=True)
    verified = models.BooleanField(null=True,blank=True)

    def __str__(self):
        return self.user.username