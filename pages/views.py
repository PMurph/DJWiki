import json
import models
import django.http
import django.template

# Create your views here.
def detail(request, page_url):
    wiki_page = models.WikiPage.objects.get(page_url=page_url)
    page_template = django.template.loader.get_template('pages/wiki_page_details.html')
    context = django.template.RequestContext(request, {
        "page_title": wiki_page.title,
        "page_content": wiki_page.page_content
    })
    return django.http.HttpResponse(page_template.render(context))
    
def new(request):
    new_page_template = django.template.loader.get_template('pages/wiki_page_new.html')
    return django.http.HttpResponse(new_page_template.render())
    
def create(request):
    if(request.method != "POST"):
        return django.http.HttpResponseNotAllowed(['POST'])
    
    new_page_content = json.loads(request.body)
    new_page_title = new_page_content[u'title']
    new_page_url = new_page_content[u'page_url'] if u'page_url' in new_page_content else new_page_title
    try:
        models.WikiPage.objects.get(page_url=new_page_url)
        response_json = json.dumps({u'errors': ["Page %s already exists" % (new_page_url)]})
        return django.http.HttpResponseForbidden(response_json, content_type="application/json")
    except:
        pass
    
    new_page = models.WikiPage(title=new_page_title, page_content=new_page_content[u'page_content'])
    if u'page_url' in new_page_content and new_page_content[u'page_url'] != '':
        new_page.page_url = new_page_content[u'page_url']
    new_page.last_modified = new_page.created_date
    new_page.save()
    response_json = json.dumps({u"wikiPage": new_page.page_url})
    return django.http.HttpResponse(response_json, content_type="application/json")
    
def edit(request, page_url):
    edit_page = models.WikiPage.objects.get(page_url=page_url)

    edit_page_template = django.template.loader.get_template('pages/wiki_page_edit.html')
    context = django.template.RequestContext(request, {
        "page_title": edit_page.title,
        "page_content": edit_page.page_content
    })
    return django.http.HttpResponse(edit_page_template.render(context))