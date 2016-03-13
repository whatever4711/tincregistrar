import names
from django.db import models
from ipaddress import IPv4Address

class NodeManager(models.Manager):
    def create_Node(self, parser, public_IP, network_obj):

        if not parser.hostname:
            parser.hostname = self.random_name()
        if not parser.config_ip:
            parser.config_ip = public_IP

        ip_list = Node.objects.order_by('-private_IP')
        IP=""
        if ip_list:
            IP = str(IPv4Address(ip_list[0].private_IP) + 1)

        if Node.objects.filter(public_IP=public_IP).exists():
            node = Node.objects.get(public_IP=public_IP)
            node.network = network_obj
            node.hostname = parser.hostname
            node.pub_key = parser.rsa
            node.config_IP = parser.config_ip
        else:
            node = self.create(hostname=parser.hostname, public_IP=public_IP, config_IP=parser.config_ip, pub_key=parser.rsa, network=network_obj)
        if IP:
            node.private_IP = IP

        node.save()
        return node

    def delete_Node(self, public_IP):
        deleted = Node.objects.filter(public_IP=public_IP).delete()
        if deleted[0] > 0:
            return True
        else:
            return False

    def random_name(self):
        newName = names.get_first_name().lower()
        existingNames = map(lambda x: x.hostname , Node.objects.all())
        if newName not in existingNames:
            return newName
        else:
            return random_name

class Network(models.Model):
    netname = models.CharField('netname', default='tinc', max_length=100)
    net = models.GenericIPAddressField('net', default="10.0.0.0")
    netmask = models.PositiveSmallIntegerField('subnet', default=32)
    secret = models.CharField('secret', max_length=32)
    
    def __str__(self):
        return self.netname


# Create your models here.
class Node(models.Model):
    network = models.ForeignKey(Network)
    hostname = models.CharField('hostname', default='', max_length=100)
    public_IP = models.GenericIPAddressField('public IP')
    config_IP = models.GenericIPAddressField('config IP')
    private_IP = models.GenericIPAddressField('private IP', default='10.0.0.1')
    private_SN = models.PositiveSmallIntegerField('private Subnet', default=32)
    pub_key = models.TextField('pub Key')

    objects = NodeManager()

    def __str__(self):
        return self.hostname
