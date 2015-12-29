import django.core.urlresolvers
import django.test.client
import django.test.runner
import django.utils.timezone
import lettuce
import pages.models

@lettuce.before.all
def setUp():
    lettuce.world.test_runner = django.test.runner.DiscoverRunner()
    lettuce.world.old_config = lettuce.world.test_runner.setup_databases()
    lettuce.world.test_client = django.test.client.Client()
    
@lettuce.after.all
def tearDown(*args):
    lettuce.world.test_runner.teardown_databases(lettuce.world.old_config)
    
@lettuce.step(u'[And ]{0,1}[G|g]iven that the ([^\s-]+)-([^\s]+) page exists')
def given_the_url_based_exists(step, url_prefix, url_suffix):
    page_url = "%s-%s" % (url_prefix, url_suffix)
    try:
        response = lettuce.world.test_client.get(django.core.urlresolvers.reverse('pages:detail', args=(page_url,)))
        if "Wiki: %s" % (url_prefix) not in response.content:
            pages.models.WikiPage(title=url_prefix, page_url=page_url, page_content="This is a test project", last_modified=django.utils.timezone.now()).save()
    except:
        pages.models.WikiPage(title=url_prefix, page_url=page_url, page_content="This is a test project", last_modified=django.utils.timezone.now()).save()