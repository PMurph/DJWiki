import models
import django.http
import django.template

# Create your views here.
def detail(request, page_title):
    wiki_page = models.WikiPage.objects.get(title=page_title)
    page_template = django.template.loader.get_template('pages/wiki_page_details.html')
    context = django.template.RequestContext(request, {
        "page_title": wiki_page.title,
        "page_content": wiki_page.page_content
    })
    return django.http.HttpResponse(page_template.render(context))