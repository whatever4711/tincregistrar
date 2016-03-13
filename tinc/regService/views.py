from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Node
from .models import Network
from .logic import NodeParser as Parser
from django.views.generic import View
import uuid

#from django.views.decorators.csrf import csrf_protect
#import simplejson

def index(request):
    node_list = Node.objects.order_by('public_IP')
    template = loader.get_template('regService/index.html')
    context = {
        'node_list': node_list,
    }
    return HttpResponse(template.render(context, request))

#@csrf_protect


class ConfigView(View):
    
    
    def get(self, request, *args, **kwargs):
        node_list = Node.objects.all()
        p = Parser()
        response=[]
        for node in node_list:
            p.parseNode(node)
            response.append(str(p))
            response.append('%')
        return HttpResponse(''.join(response))

    def post(self, request, *args, **kwargs):
        s = request.body.decode("utf-8")
        p = Parser()
        p.parseInput(s)

        ip = request.META['REMOTE_ADDR']
        secret_uncleaned = request.META["HTTP_AUTHORIZATION"]
        
        secret_split = secret_uncleaned.split(" ")
        
        if len(secret_split) <= 1:
            secret = uuid.uuid1()
        else:
            secret = secret_split[1]
        
        
        obj, created = Network.objects.get_or_create(secret=secret)
        obj.netname = p.networkname
        obj.save()
        node = Node.objects.create_Node(p, ip, obj)
        
        
    
        
        p.parseNode(node)
        response=[]
        if p.config_ip is not ip:
            response.append("# Your external IP is: %s\n" % ip)

        response.append("# NetworkName: {}\n".format(p.networkname))
            
        response.append(str(p))
        return HttpResponse(''.join(response))
        
    def delete(self, request, *args, **kwargs):  
        ip = request.META['REMOTE_ADDR']
        if Node.objects.delete_Node(ip):
            return HttpResponse("DELETED %s" % ip)
        else:
            raise Http404("Node with IP %s not registered" % ip)

