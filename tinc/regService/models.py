import names, ipaddress, uuid
from django.db import models
from .error import AddressError

def random_name(existingNames):
    newName = names.get_first_name().lower()
    if newName not in existingNames:
        return newName
    else:
        return random_name(existingNames)

class NodeManager(models.Manager):
    def create_Node(self, parser, public_IP, network):

        if not parser.hostname:
            parser.hostname = random_name(map(lambda x: x.hostname,
                Node.objects.all()))
        if not parser.public_ip:
            parser.public_ip = public_IP

        ip_list = Node.objects.order_by('-private_IP').filter(network = network)

        # TODO Adjust for subnets on one host
        IP=""
        if not ip_list:
            IP = str(network.getNetwork().network_address + 1)
        elif ipaddress.ip_address(ipaddress.ip_address(ip_list[0].private_IP) + 1) in network.getNetwork():
            IP = str(ipaddress.ip_address(ip_list[0].private_IP) + 1)
        else:
            raise AddressError("NO FREE IPs", "Subnet %s completely allocated"
                % network.getNetwork())

        if Node.objects.filter(public_IP=public_IP).exists():
            node = Node.objects.get(public_IP=public_IP)
            node.network = network
            node.hostname = parser.hostname
            node.pub_key = parser.rsa
            # TODO Within an update a new IP is set?
            node.private_IP = IP
            node.config_IP = parser.public_ip
        else:
            node = self.create(network=network, hostname=parser.hostname,
                public_IP=parser.public_ip, private_IP=IP, config_IP=parser.public_ip,
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
            parser.networkname = random_name(map(lambda x: x.netname,
                Network.objects.all()))

        #TODO: Check if Net is the same / different secrets for different nets
        if Network.objects.filter(secret=secret).exists():
            network = Network.objects.get(secret=secret)
        else:
            network = self.create(netname=parser.networkname, secret=secret)

        if parser.net:
            base_net = ipaddress.ip_network(parser.net, strict=False)
            network.net = str(base_net.network_address)
            network.netmask = int(base_net.prefixlen)

        network.save()
        return network


class Network(models.Model):
    netname = models.CharField('netname', default='tinc', max_length=100)
    net = models.GenericIPAddressField('net', default="10.0.0.0")
    netmask = models.PositiveSmallIntegerField('netmask', default=16)
    secret = models.CharField('secret', max_length=32)

    objects = NetworkManager()

    def getNetwork(self):
        return ipaddress.ip_network("%s/%s" % (self.net, self.netmask))

    def __str__(self):
        return self.netname

class Node(models.Model):
    network = models.ForeignKey(Network)
    hostname = models.CharField('hostname', default='', max_length=100)
    public_IP = models.GenericIPAddressField('public IP')
    config_IP = models.GenericIPAddressField('config IP')
    private_IP = models.GenericIPAddressField('private IP')
    private_netmask = models.PositiveSmallIntegerField('netmask', default=32)
    pub_key = models.TextField('pub Key')

    objects = NodeManager()

    def getSubnet(self):
        return ipaddress.ip_network("%s/%s" % (self.private_IP, self.private_netmask))

    def __str__(self):
        return self.hostname
