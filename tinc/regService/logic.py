from .models import Node

class NodeParser:
    hostnameComment = "# Hostname = "
    beginRSA = "-----BEGIN RSA PUBLIC KEY-----"
    endRSA = "-----END RSA PUBLIC KEY-----"
    addressName = "Address = "
    subnetName = "Subnet = "

    def __init__(self):
        self.hostname = ""
        self.rsa = ""
        self.config_ip = ""
        self.subnet = ""

    def parseInput(self, txt):
        spl = txt.split(self.beginRSA)
        addresses = [x.strip() for x in spl[0].split("\n") if x]
        for address in addresses:
            if address.startswith(self.hostnameComment):
                self.hostname = address.replace(self.hostnameComment, '')
            if address.startswith(self.addressName):
                self.config_ip = address.replace(self.addressName, '')
            if address.startswith(self.subnetName):
                self.subnet = address.replace(self.subnetName, '')
        self.rsa = spl[1].split(self.endRSA)[0].replace('\n', '')

    def parseNode(self, Node):
        self.hostname = Node.hostname
        self.rsa = Node.pub_key
        self.config_ip = Node.config_IP
        self.subnet = ''.join([Node.private_IP, '/', str(Node.private_SN)])

    def splitRSA(self,n):
        s = self.rsa
        o = []
        while s:
            o.append(s[:n])
            s = s[n:]
        return '\n'.join(o)

    def __str__(self):
        sos = []
        sos.append(self.hostnameComment)
        sos.append(self.hostname)
        sos.append('\n')
        sos.append(self.addressName)
        sos.append(self.config_ip)
        sos.append('\n')
        sos.append(self.subnetName)
        sos.append(self.subnet)
        sos.append('\n\n')
        sos.append(self.beginRSA)
        sos.append('\n')
        sos.append(self.splitRSA(64))
        sos.append('\n')
        sos.append(self.endRSA)
        sos.append('\n')
        return ''.join(sos)
