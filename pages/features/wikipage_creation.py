# -*- coding: utf-8 -*-

import django.core.urlresolvers
import django.test.client
import lettuce

@lettuce.before.all
def setUp():
    lettuce.world.test_client = django.test.client.Client()

@lettuce.step(u'[And ]{0,1}[G|g]iven that I view the new page form')
def view_the_new_page_form(step):
    lettuce.world.last_response = lettuce.world.test_client.get(django.core.urlresolvers.reverse('pages:new'))
    
@lettuce.step(u'[And ]{0,1}[T|t]he page should have a place to enter the ([^\s]+) of the page')
def should_have_form_element(step, form_element):
    assert(lettuce.world.last_response is not None)
    
    page_content = lettuce.world.last_response.content
    
    form_element = "<input name='%s'>" % (form_element)
    assert(form_element in page_content)