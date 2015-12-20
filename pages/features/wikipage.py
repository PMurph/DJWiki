# -*- coding: utf-8 -*-

import django.test.client
import lettuce
import socket
import urllib

from lettuce import step, before, after, world

EXIT_MESSAGE = "sock_exit"

# Should look for a way of pulling these automatically from Django
host_name = 'localhost'
port = 8000
site = "http://"
wiki_pages = 'pages'

def get_wiki_page_url(page_name):
    return '/'.join([site, ':'.join([host_name, str(port)]), wiki_pages, urllib.quote(page_name)])

@lettuce.before.all
def setUp():
    try: 
        lettuce.world.debug_socket = socket.socket()
        lettuce.world.debug_socket.connect(('127.0.0.1', 16543))
    except:
        lettuce.world.debug_socket.close()
    
    lettuce.world.test_client = django.test.client.Client()
    
@lettuce.after.all
def tearDown(*args):
    try:
        lettuce.world.debug_socket.send(EXIT_MESSAGE)
    except:
        pass
    finally:
        lettuce.world.debug_socket.close()

@lettuce.step(u'[And ]{0,1}[G|g]iven that the ([^\s]+) page exists')
def given_that_the_page_exists(step, page_name):
    page_url = get_wiki_page_url(page_name)
    
    response = lettuce.world.test_client.get(page_url)
    
    assert(response.status_code == 200)

@lettuce.step(u'[And ]{0,1}[G|g]iven that I view the ([^\s]+) page')
def given_that_i_view_the_page(step, page_name):
    page_url = get_wiki_page_url(page_name)
    
    lettuce.world.current_response = lettuce.world.test_client.get(page_url)
    
@lettuce.step(u'[And ]{0,1}[T|t]he page should have the title ([^s]+)')
def the_page_should_have_title(step, page_title):
    assert(lettuce.world.current_response is not None)
    
    page_content = lettuce.world.current_response.content
    
    assert(("<title> Wiki: " + page_title + "</title>") in page_content)
    
@lettuce.step(u"[And ]{0,1}[T|t]he page's main heading should be \"([^\"]+)")
def the_pages_main_heading(step, main_heading):
    assert(lettuce.world.current_response is not None)
    
    page_content = lettuce.world.current_response.content
    
    assert(("<h1>" + main_heading + "</h1>") in page_content)
    
@lettuce.step(u"[And ]{0,1}[I|i]t should contain the text \"([^\"]+)")
def it_should_contain_text(step, text):
    assert(lettuce.world.current_response is not None)
    
    page_content = lettuce.world.current_response.content
    
    assert(text in page_content)
