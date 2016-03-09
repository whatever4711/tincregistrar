from django.db import models

# Create your models here.
class Node(models.Model):
    public_IP = models.GenericIPAddressField('public IP')
    private_IP = models.GenericIPAddressField('private IP')
    pub_key = models.TextField('pub Key')
