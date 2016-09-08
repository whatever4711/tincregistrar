from os import path
from django.shortcuts import render
from django.http import HttpResponse, Http404, FileResponse
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

def check_secret(request):
    auth_field = 'HTTP_AUTHORIZATION'
    ip = request.META['REMOTE_ADDR']
    if auth_field not in request.META:
        raise Http404("IP %s is not authorized to access this service" % ip)
    secret_uncleaned = request.META[auth_field]
    return secret_uncleaned
    # TODO UUID as secret
    #secret_split = secret_uncleaned.split(" ")
    #if len(secret_split) <= 1:
    #    return uuid.uuid1()
    #else:
    #    return secret_split[1]

#@csrf_protect

def send_script(request):
    filename = "tincsetup.sh"
    response = FileResponse(open(filename, 'rb'), content_type='text/plain')
    response['Content-Length'] = path.getsize(filename)
    return response

class ConfigView(View):

    def get(self, request, *args, **kwargs):
        check_secret(request)
        node_list = Node.objects.all()
        p = Parser()
        response=[]
        for node in node_list:
            p.parseNode(node)
            response.append(str(p))
            response.append('%\n')
        return HttpResponse(''.join(response))

    def post(self, request, *args, **kwargs):
        secret = check_secret(request)
        s = request.body.decode("utf-8")
        p = Parser()
        p.parseInput(s)

        ip = request.META['REMOTE_ADDR']

        created = Network.objects.create_Network(p, secret)
        node = Node.objects.create_Node(p, ip, created)

        p.parseNode(node)
        response=[]
        if p.public_ip is not ip:
            response.append("# Your external IP is: %s\n" % ip)

        response.append(str(p))
        return HttpResponse(''.join(response))

    def delete(self, request, *args, **kwargs):
        check_secret(request)
        ip = request.META['REMOTE_ADDR']
        if Node.objects.delete_Node(ip):
            return HttpResponse("DELETED %s" % ip)
        else:
            raise Http404("Node with IP %s not registered" % ip)
