from django.db import models

# Create your models here.
class Node(models.Model):
    public_IP = models.GenericIPAddressField('public IP')
    private_IP = models.GenericIPAddressField('private IP')
    private_SN = models.PositiveSmallIntegerField('private Subnet', default=32)
    pub_key = models.TextField('pub Key')

    def __str__(self):
        return "PubIP: " + public_IP + "PrivIP" + private_IP + "/" + private_SN
