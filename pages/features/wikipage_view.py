# -*- coding: utf-8 -*-

import django.core.urlresolvers
import django.test.client
import django.test.runner
import django.utils
import lettuce
import pages.models
import socket
import urllib

from lettuce import step, before, after, world

EXIT_MESSAGE = "sock_exit"

# Should look for a way of pulling these automatically from Django
host_name = 'localhost'
port = 8000
site = "http://"
wiki_pages = 'pages'

@lettuce.before.all
def setUp():
    # This is a hack pulled from django test runner DiscoverRunner.run_tests, since lettuce is not setup to handle creating a test database
    lettuce.world.test_runner = django.test.runner.DiscoverRunner()
    lettuce.world.old_config = lettuce.world.test_runner.setup_databases()
    try: 
        lettuce.world.debug_socket = socket.socket()
        lettuce.world.debug_socket.connect(('127.0.0.1', 16543))
    except:
        lettuce.world.debug_socket.close()
    
    lettuce.world.test_client = django.test.client.Client()
    
@lettuce.after.all
def tearDown(*args):
    # End of hack
    lettuce.world.test_runner.teardown_databases(lettuce.world.old_config)
    try:
        lettuce.world.debug_socket.send(EXIT_MESSAGE)
    except:
        pass
    finally:
        lettuce.world.debug_socket.close()

@lettuce.step(u'[And ]{0,1}[G|g]iven that the ([^\s]+) page exists')
def given_that_the_page_exists(step, page_name):
    try:
        response = lettuce.world.test_client.get(django.core.urlresolvers.reverse('pages:detail', args=(page_name,)))
        if "Wiki: %s" % (page_name) not in response.content:
            pages.models.WikiPage(title=page_name, page_content="This is a test project", last_modified=django.utils.timezone.now()).save()
    except:
        pages.models.WikiPage(title=page_name, page_content="This is a test project", last_modified=django.utils.timezone.now()).save()

@lettuce.step(u'[And ]{0,1}[G|g]iven that I view the ([^\s]+) page')
def given_that_i_view_the_page(step, page_name):
    lettuce.world.current_response = lettuce.world.test_client.get(django.core.urlresolvers.reverse('pages:detail', args=(page_name,)))
    
@lettuce.step(u'[And ]{0,1}[T|t]he page should have the title ([^\s]+)')
def the_page_should_have_title(step, page_title):
    assert(lettuce.world.current_response is not None)
    
    page_content = lettuce.world.current_response.content
    
    assert(("<title>Wiki: " + page_title + "</title>") in page_content)
    
@lettuce.step(u"[And ]{0,1}[T|t]he page's main heading should be \"([^\"]+)")
def the_pages_main_heading(step, main_heading):
    assert(lettuce.world.current_response is not None)
    
    page_content = lettuce.world.current_response.content
    
    assert(("<h1>%s</h1>" % (main_heading)) in page_content)
    
@lettuce.step(u"[And ]{0,1}[I|i]t should contain the text \"([^\"]+)")
def it_should_contain_text(step, text):
    assert(lettuce.world.current_response is not None)
    
    page_content = lettuce.world.current_response.content
    
    assert(text in page_content)
