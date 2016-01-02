# -*- coding: utf-8 -*-

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
    
@lettuce.step(u'[And ]{0,1}[G|g]iven that I view the ([^\s]+) ([^\s]+) operation page')
def given_i_view_pages_operation(step, page_title, page_operation):
    page_operation = 'pages:%s' % (page_operation)
    lettuce.world.current_response = lettuce.world.test_client.get(django.core.urlresolvers.reverse(page_operation, args=(page_title,)))
    
@lettuce.step(u'[And ]{0,1}[G|g]iven that I save the ([^\s]+) changes')
def given_that_i_save_edits(step, page_url):
    lettuce.world.current_response = lettuce.world.test_client.post(django.core.urlresolvers.reverse('pages:update', args=(page_url,)), data=json.dumps(lettuce.world.form), content_type='application/json')
    
@lettuce.step(u'[And ]{0,1}I should receive a message stating that the ([^\s]+) page has been saved')
def should_receive_message_that_page_was_saved(step, page_url):
    response = '{"wikiPage": "%s"}' % (page_url)
    assert(response == lettuce.world.current_response.content)
    
@lettuce.step(u'[And ]{0,1}[I|i]t should have a link to the ([^\s]+) operation page')
def should_have_link_to_page_operation(step, page_operation):
    page_link = 'href="%s/"' % (page_operation)
    assert(page_link in lettuce.world.current_response.content)