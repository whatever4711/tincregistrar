import names
from django.db import models
from ipaddress import IPv4Address
import uuid

def random_name(existingNames):
    newName = names.get_first_name().lower()
    if newName not in existingNames:
        return newName
    else:
        return random_name(existingNames)

class NodeManager(models.Manager):
    def create_Node(self, parser, public_IP, network):

        if not parser.hostname:
            parser.hostname = random_name(map(lambda x: x.hostname, Node.objects.all()))
        if not parser.config_ip:
            parser.config_ip = public_IP

        ip_list = Node.objects.order_by('-private_IP').filter(network=network)

        IP=""
        if ip_list:
            IP = str(IPv4Address(ip_list[0].private_IP) + 1)
        else:
            IP = str(IPv4Address(network.net) + 1)

        if Node.objects.filter(public_IP=public_IP).exists():
            node = Node.objects.get(public_IP=public_IP)
            node.network = network
            node.hostname = parser.hostname
            node.pub_key = parser.rsa
            node.private_IP = IP
            node.config_IP = parser.config_ip
        else:
            node = self.create(network=network_obj, hostname=parser.hostname,
                public_IP=public_IP, private_IP=IP, config_IP=parser.config_ip,
                pub_key=parser.rsa)

        node.save()
        return node

    def delete_Node(self, public_IP):
        deleted = Node.objects.filter(public_IP=public_IP).delete()
        if deleted[0] > 0:
            return True
        else:
            return False



class NetworkManager(models.Manager):
    def create_Network(self, parser, secret):
        if not parser.networkname:
            parser.networkname = random_name(map(lambda x: x.netname, Network.objects.all()))

        if Network.objects.filter(secret=secret).exists():
            network = Network.objects.get(secret=secret)
        else:
            network = self.create(netname=parser.networkname, secret=secret)
        #if parser.subnet:
        #    network.net = parser.net
        if parser.subnet:
            network.netmask = parser.subnet

        network.save()
        return network


class Network(models.Model):
    netname = models.CharField('netname', default='tinc', max_length=100)
    net = models.GenericIPAddressField('net', default="10.0.0.0")
    netmask = models.PositiveSmallIntegerField('subnet', default=32)
    secret = models.CharField('secret', max_length=32)

    objects = NetworkManager()

    def __str__(self):
        return self.netname


# Create your models here.
class Node(models.Model):
    network = models.ForeignKey(Network)
    hostname = models.CharField('hostname', default='', max_length=100)
    public_IP = models.GenericIPAddressField('public IP')
    config_IP = models.GenericIPAddressField('config IP')

    # TODO get from network
    private_IP = models.GenericIPAddressField('private IP', default='10.0.0.1')
    pub_key = models.TextField('pub Key')

    objects = NodeManager()

    def __str__(self):
        return self.hostname
