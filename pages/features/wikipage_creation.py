# -*- coding: utf-8 -*-

import django.test.client
import lettuce

@lettuce.before.all
def setUp():
    lettuce.world.test_client = django.test.client.Client()

@lettuce.step(u'[And ]{0,1}[G|g]iven that I view the new page form')
def view_the_new_page_form(step):
    pass