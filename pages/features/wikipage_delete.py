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