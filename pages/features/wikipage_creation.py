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

@lettuce.step(u'[And ]{0,1}[G|g]iven that I view the new page form')
def view_the_new_page_form(step):
    lettuce.world.last_response = lettuce.world.test_client.get(django.core.urlresolvers.reverse('pages:new'))
    
@lettuce.step(u'[And ]{0,1}[I|i]t should have a place to enter the ([^\s]+) of the page')
def should_have_form_element(step, form_element):
    assert(lettuce.world.last_response is not None)
    
    page_content = lettuce.world.last_response.content
    
    input_form_element = "<input type='text' name='%s' />" % (form_element)
    textarea_form_element = "<textarea name='%s'>" % (form_element)
    assert(input_form_element in page_content or textarea_form_element in page_content)
    
@lettuce.step(u'[And ]{0,1}[G|g]iven that the ([^\s]+) page does not exist')
def given_page_does_not_exist(step, page_name):
    found_page = None
    try:
        found_page = pages.models.WikiPage.objects.get(title=page_name)
    except:
        pass
    assert(found_page is None)
    
@lettuce.step(u'[And ]{0,1}[G|g]iven that I enter "([^"]+)" as the ([^\s]+)')
def given_that_I_enter_a_value(step, input, key):
    try:
        lettuce.world.form
    except AttributeError as e:
        lettuce.world.form = {}
    
    lettuce.world.form[key] = input
    
@lettuce.step(u'[And ]{0,1}[G|g]iven that I create the page')
def given_that_I_create_the_page(step):
    lettuce.world.current_response = lettuce.world.test_client.post(django.core.urlresolvers.reverse('pages:create'), data=json.dumps(lettuce.world.form), content_type='application/json')
    
@lettuce.step(u'[And ]{0,1}I should receive a message stating the ([^\s]+) page was created')
def should_receive_message_stating_page_was_created(step, page_name):
    assert('{"wikiPage": "NewProject"}' == lettuce.world.current_response.content)
    
@lettuce.step(u'[And ]{0,1}I should see the "([^"]+)" page')
def should_see_the_page(step, page_name):
    assert("<title>Wiki: %s</title>" % (page_name) in lettuce.world.current_response.content) 
    
@lettuce.step(u'[And ]{0,1}I should receive a message stating there was an error creating the page')
def should_receive_message_stating_there_was_an_error_creating_the_page(step):
    response_json = json.loads(lettuce.world.current_response.content)
    assert(len(response_json['errors']) > 0)