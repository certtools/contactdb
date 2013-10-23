from django.http import HttpResponse
from django.template import RequestContext, Context, loader
from contactdb.models import Countrycode
import contactdb.netobjects

# exception handling
import sys
import traceback

def index(request):
    country_list = Countrycode.objects.all().order_by('-cc')
    t = loader.get_template("index.html")
    c = Context({
        'country_list' : country_list,
        })
    return HttpResponse(t.render(c))

def search(request):
    try:
        search_string = request.POST["country_name"]
        country_list = Countrycode.objects.filter(country_name__contains=search_string).order_by('cc')
        c = RequestContext(request, {'country_list' : country_list})
        t = loader.get_template("index.html")
        return HttpResponse(t.render(c))
    except:
        c = RequestContext(request, {})
        t = loader.get_template("search.html")
        return HttpResponse(t.render(c))
    
def addasn(request):
    try:
        asn = request.POST["asn"]
        asname = request.POST["asname"]
        print("DEBUG asn = %s asname = %s" % (asn, asname))
        contactdb.netobjects.addASN(asn, asname)
        print("DEBUG object added to DB")
        c = RequestContext(request, {'asn' : asn, 'asname' : asname})
        t = loader.get_template("index.html")
        return HttpResponse(t.render(c))
    except:
        e = sys.exc_info()[0]
        print("DEBUG: IN EXCEPTION!! %s" % (e))
        c = RequestContext(request, {})
        t = loader.get_template("add_asn.html")
        return HttpResponse(t.render(c))
    return

def addsource(request):
    try:
        source = request.POST["source"]
        reliability = request.POST["reliability"]
        contactdb.envinfo.addSource(source, reliability)
        c = RequestContext(request, {'source' : source, 'reliability' : reliability})
        t = loader.get_template("index.html")
        return HttpResponse(t.render(c))
    except:
        e = sys.exc_info()[0]
        tb = sys.exc_info()[2]
        traceback.print_tb(tb)
        print("DEBUG: IN EXCEPTION!! %s" % (e))
        c = RequestContext(request, {})
        t = loader.get_template("add_source.html")
        return HttpResponse(t.render(c))
    return

