from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.template import loader
import os

# Create your views here.
def index(request):
    pathDir =  os.listdir('/Users/zhangquanming/')
    print pathDir
    c = {
    "request":request,
    "pathdir":pathDir
    }
    c.update(csrf(request))
    template = loader.get_template('tt.html')
    return HttpResponse(template.render(c))

def download(request):
    data = request.POST
    print data
    #filename = data["filename"]
    filename = str(data["filename"])
    print str(filename),type(str(filename))
    print filename,type(filename)
    with open(filename,'rt') as f:
        result = f.read()
        # for line in f:
    print result
    c = { "result":result }
    c.update(csrf(request))
    template = loader.get_template('downtable.html')
    return HttpResponse(result)

def readxml(request):
    data = request.GET
    print data
    #filename = data["filename"]
    v = str(data["v"])
    s = str(data["s"])
    c = str(data["c"])
    filename = '/' + v + '/' + s + '/' + c
    #print str(filename),type(str(filename))
    print filename,type(filename)
    with open(filename,'rt') as f:
        result = f.read()
        # for line in f:
    print result,type(result)
    # c = { "result":result }
    # c.update(csrf(request))
    # template = loader.get_template('downtable.html')
    #return HttpResponse(template.render(c))
    return HttpResponse(result,content_type='text/xml')
