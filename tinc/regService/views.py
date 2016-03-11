from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Node
from .logic import NodeParser as Parser
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
def config(request):
    if request.method == "POST":
        s = request.body.decode("utf-8")
        p = Parser()
        p.parseInput(s)

        node = Node.objects.create_Node(p)
        p.parseNode(node)
        return HttpResponse(str(p))
    elif request.method == "GET":
        node_list = Node.objects.all()

        p = Parser()
        response=[]
        for node in node_list:
            p.parseNode(node)
            response.append(str(p))
        return HttpResponse('\n'.join(response))
    elif request.method == "DELETE":
        s = request.body.decode("utf-8")
        print(request.META['REMOTE_ADDR'])
        p = Parser()
        p.parseInput(s)
        Node.objects.delete_Node(p)
        return HttpResponse("DELETED")
    else:
        raise Http404("Invalid Request")
