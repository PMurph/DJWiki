# -*- coding: utf-8 -*-

import django.core.exceptions
import django.core.urlresolvers
import django.test.client
import django.test.runner
import django.utils
import json
import pages.models
import lettuce

@lettuce.before.all
def setUp():
    # Hack. See wikipage_view.py for more details
    lettuce.world.test_runner = django.test.runner.DiscoverRunner()
    lettuce.world.old_config = lettuce.world.test_runner.setup_databases()
    lettuce.world.test_client = django.test.client.Client()
    
@lettuce.after.all
def tearDown(*args):
    lettuce.world.test_runner.teardown_databases(lettuce.world.old_config)
    
@lettuce.step(u'[And ]{0,1}[I|i]t should have a "([^"]+)" button')
def it_should_have_button(step, button_name):
    html = "%s</button>" % (button_name)
    assert(html in lettuce.world.current_response.content)
    
@lettuce.step(u'[And ]{0,1}[G|g]iven that I delete the ([^\s]+) page')
def given_that_i_delete_the_page(step, page_url):
    lettuce.world.test_client.post(django.core.urlresolvers.reverse('pages:delete', args=(page_url,)))
    
@lettuce.step(u'[And ]{0,1}[T|t]he ([^\s]+) page should no longer exist')
def the_page_should_no_longer_exist(step, page_url):
    try:
        pages.models.WikiPage.objects.get(page_url=page_url)
        assert(False)
    except django.core.exceptions.ObjectDoesNotExist as odne:
        pass