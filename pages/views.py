import json
import models
import django.core.exceptions
import django.http
import django.template
import django.utils

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
        response_json = json.dumps({u'errors': ["Only allowed method is %s" % ("POST")]})
        return django.http.HttpResponseNotAllowed(['POST'], response_json, content_type="application/json")
    
    new_page_content = json.loads(request.body)
    new_page_title = new_page_content[u'title']
    new_page_url = new_page_content[u'page_url'] if u'page_url' in new_page_content and str(new_page_content[u'page_url']) != '' else new_page_title
    try:
        models.WikiPage.objects.get(page_url=new_page_url)
        response_json = json.dumps({u'errors': ["Page %s already exists" % (new_page_url)]})
        return django.http.HttpResponseForbidden(response_json, content_type="application/json")
    except django.core.exceptions.ObjectDoesNotExist as odne:
        pass
    
    new_page = models.WikiPage(title=new_page_title, page_url=new_page_url, page_content=new_page_content[u'page_content'])
    new_page.last_modified = new_page.created_date
    new_page.save()
    response_json = json.dumps({u"wikiPage": new_page.page_url})
    return django.http.HttpResponse(response_json, content_type="application/json")
    
def edit(request, page_url):
    edit_page = None
    try:
        edit_page = models.WikiPage.objects.get(page_url=page_url)
    except django.core.exceptions.ObjectDoesNotExist as odne:
        return django.http.HttpResponseNotFound("Page %s does not exist" % (page_url))

    edit_page_template = django.template.loader.get_template('pages/wiki_page_edit.html')
    context = django.template.RequestContext(request, {
        "page_title": edit_page.title,
        "page_content": edit_page.page_content
    })
    return django.http.HttpResponse(edit_page_template.render(context))
    
def update(request, page_url):
    update_page = None
    try:
        update_page = models.WikiPage.objects.get(page_url=page_url)
    except django.core.exceptions.ObjectDoesNotExist as odne:
        response_json = json.dumps({u'errors': ["Page %s does not exist" % (page_url)]})
        return django.http.HttpResponseNotFound(response_json, content_type='application/json')
    
    updated_page_content = json.loads(request.body)
    
    update_page.title = updated_page_content[u'title']
    update_page.page_content = updated_page_content[u'page_content']
    update_page.last_modified = django.utils.timezone.now()
    update_page.save()
    response_json = json.dumps({u'wikiPage': page_url})
    return django.http.HttpResponse(response_json, content_type='application/json')