from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import simplejson

def index(request):
    return HttpResponse("Hello world.")

@csrf_protect
def json(request):
    print(request)
    to_json = {
        "key1": "value1",
        "key2": "value2"
    }
    return HttpResponse(simplejson.dumps(to_json), content_type='application/json')
