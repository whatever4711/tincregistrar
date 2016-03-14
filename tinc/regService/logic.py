from .models import Node

class NodeParser:
    hostnameComment = "# Hostname = "
    networknameComment = "# NetworkName = "
    beginRSA = "-----BEGIN RSA PUBLIC KEY-----"
    endRSA = "-----END RSA PUBLIC KEY-----"
    addressName = "Address = "
    subnetName = "Subnet = "

    def __init__(self):
        self.hostname = ""
        self.networkname = ""
        self.rsa = ""
        self.public_ip = ""
        self.subnet = ""

    def parseInput(self, txt):
        spl = txt.split(self.beginRSA)
        addresses = [x.strip() for x in spl[0].split("\n") if x]
        for address in addresses:
            if address.startswith(self.hostnameComment):
                self.hostname = address.replace(self.hostnameComment, '')
            if address.startswith(self.networknameComment):
                self.networkname = address.replace(self.networknameComment, '')
            if address.startswith(self.addressName):
                self.public_ip = address.replace(self.addressName, '')
            if address.startswith(self.subnetName):
                self.subnet = address.replace(self.subnetName, '')
        self.rsa = spl[1].split(self.endRSA)[0].replace('\n', '')

    def parseNode(self, Node):
        self.hostname = Node.hostname
        self.network = Node.network.netname
        self.rsa = Node.pub_key
        self.public_ip = Node.config_IP
        self.subnet = Node.private_IP

    def splitRSA(self,n):
        s = self.rsa
        o = []
        while s:
            o.append(s[:n])
            s = s[n:]
        return '\n'.join(o)

    def __str__(self):
        sos = []
        sos.append('%s %s \n' % (self.hostnameComment, self.hostname))
        sos.append('%s %s \n' % (self.addressName, self.public_ip))
        sos.append('%s %s \n\n' % (self.subnetName, self.subnet))
        sos.append('%s \n' % self.beginRSA)
        sos.append('%s \n' % self.splitRSA(64))
        sos.append('%s \n' % self.endRSA)
        return ''.join(sos)
