import names
from django.db import models
from ipaddress import IPv4Address

class NodeManager(models.Manager):
    def create_Node(self, parser):


        if Node.objects.filter(public_IP=parser.public_ip).exists():
            node = Node.objects.filter(public_IP=parser.public_ip)
            return node[0]

        if not parser.hostname:
            parser.hostname = self.random_name()

        ip_list = Node.objects.order_by('-private_IP')
        IP=""
        if ip_list:
            IP = str(IPv4Address(ip_list[0].private_IP) + 1)

        node = self.create(hostname=parser.hostname, public_IP=parser.public_ip, pub_key=parser.rsa)
        if IP:
            node.private_IP = IP
        node.save()
        return node


    def random_name(self):
        newName = names.get_first_name().lower()
        existingNames = map(lambda x: x.hostname , Node.objects.all())
        if newName not in existingNames:
            return newName
        else:
            return random_name

# Create your models here.
class Node(models.Model):
    hostname = models.CharField('hostname', default='', max_length=100)
    public_IP = models.GenericIPAddressField('public IP')
    private_IP = models.GenericIPAddressField('private IP', default='10.0.0.1')
    private_SN = models.PositiveSmallIntegerField('private Subnet', default=32)
    pub_key = models.TextField('pub Key')

    objects = NodeManager()

    def __str__(self):
        return self.hostname + " PubIP: " + self.public_IP + " PrivIP: " + self.private_IP + "/" + str(self.private_SN)
