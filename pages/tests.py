import django.core.urlresolvers
import django.utils
import django.test
import json
import pages.models

def create_page(page_title, page_url, page_content):
    pages.models.WikiPage(title=page_title, page_url=page_url, page_content=page_content, created_date=django.utils.timezone.now(), last_modified=django.utils.timezone.now()).save()

class WikiPageModelTest(django.test.TestCase):
    def setUp(self):
        self.page_title = "TestPage"
        self.page_content = "This is a test page"
        self.page_url = 'an-explicit-page-url'
        self.created_date = django.utils.timezone.now()
        self.last_modified = django.utils.timezone.now()
        self.test_page = pages.models.WikiPage(title=self.page_title, page_url=self.page_url, page_content=self.page_content, created_date=self.created_date, last_modified=self.last_modified)

    def test_str(self):
        '''
            Ensure that the __str__ method is working
           '''
        self.assertEquals(self.page_title, str(self.test_page))
        
    def test_unicode(self):
        '''
            Ensure that the __unicode__ method is working
           '''
        self.assertEquals(unicode(self.page_title), unicode(self.test_page))
        
    def test_model_variables_no_url(self):
        '''
            Ensure all model variables are set properly if no explicit url is set
           '''
        self.assertEquals(self.page_title, self.test_page.title)
        self.assertEquals(self.page_url, self.test_page.page_url)
        self.assertEquals(self.page_content, self.test_page.page_content)
        self.assertEquals(self.created_date, self.test_page.created_date)
        self.assertEquals(self.last_modified, self.test_page.last_modified)
        
    def test_model_variables_url(self):
        '''
            Ensures that the page_url property is set if explicit url is set
           '''
        test_page = pages.models.WikiPage(title=self.page_title, page_url=self.page_url, page_content=self.page_content, created_date=self.created_date, last_modified=self.last_modified)
        
        self.assertEquals(self.page_url, test_page.page_url)

    def test_created_date_not_null(self):
        '''
             Ensure that the created date is set when object is created
            '''
        new_wiki_page = pages.models.WikiPage()
        self.assertIsNotNone(new_wiki_page.created_date)
        
    def test_model_page_url_save_and_load(self):
        '''
            Ensure that a model with different title and url can be saved and loaded
           '''
        page_url = u'update-page'
        create_page('UpdatePageTest', page_url, 'This is a test page for updating a wiki page')
        #pages.models.WikiPage(title='UpdatePageTest', page_url=page_url, page_content="This is a test", created_date=django.utils.timezone.now(), last_modified=django.utils.timezone.now()).save()
        # Will throw exception if page doesn't exist
        update_page_url = pages.models.WikiPage.objects.get(page_url=page_url)
        self.assertEquals(page_url, update_page_url.page_url)
        
class WikiPageDetailView(django.test.TestCase):
    def setUp(self):
        self.edit_link = 'href="edit/"'

    def test_detail_view_renders_page(self):
        '''
            Ensure that the test project page loads
           '''
        page_title = "TestProject"
        page_content = u"This is a test project."
        create_page(page_title, page_title, page_content)
        
        response = self.client.get(django.core.urlresolvers.reverse('pages:detail', args=(page_title,)))
        self.assertContains(response, page_title, status_code=200)
        self.assertContains(response, page_content, status_code=200)
        self.assertContains(response, self.edit_link, status_code=200)
        
    def test_detail_view_renders_page_with_separate_url_from_title(self):
        '''
            Ensure that the a page with different titles and url
           '''
        page_title = "URLTestProject"
        page_url = "url-test-project"
        page_content = u"This is to test that a project with a separate title and url renders"
        create_page(page_title, page_url, page_content)
        
        response = self.client.get(django.core.urlresolvers.reverse('pages:detail', args=(page_url,)))
        self.assertContains(response, page_title, status_code=200)
        self.assertContains(response, page_content, status_code=200)
        self.assertContains(response, self.edit_link, status_code=200)
        
class WikiPageNewView(django.test.TestCase):
    def test_new_view_renders_page(self):
        '''
            Ensure that the new page renders that new page form
           '''
        response = self.client.get(django.core.urlresolvers.reverse('pages:new'))
        self.assertContains(response, '<h1>Create New Wiki Page</h1>', status_code=200)
        self.assertContains(response, '<label>Page Title</label>', status_code=200)
        self.assertContains(response, "<input type='text' name='title' />", status_code=200)
        self.assertContains(response, "<label>Page URL Suffix</label>", status_code=200)
        self.assertContains(response, "<input type='text' name='page_url' />", status_code=200)
        self.assertContains(response, '<label>Page Content</label>', status_code=200)
        self.assertContains(response, "<textarea name='page_content'>", status_code=200)
        
class WikiPageCreateView(django.test.TestCase):
    def test_create_view_valid_request(self):
        '''
             Ensure that the create view creates a wiki page
            '''
        page_title = "CreatePageTest"
        page_content = "This is a test create page view"
        page_data = {
            'title': page_title,
            'page_content': page_content
        }
        response = self.client.post(django.core.urlresolvers.reverse('pages:create'), data=json.dumps(page_data), content_type='application/json')
        
        response_json = {
            'wikiPage': page_title
        }
        self.assertContains(response, json.dumps(response_json), status_code=200)
        
        create_wiki_page = pages.models.WikiPage.objects.get(page_url=page_title)
        self.assertEquals(page_title, create_wiki_page.title)
        self.assertEquals(page_content, create_wiki_page.page_content)
        
    def test_create_view_valid_request_with_url(self):
        '''
            Ensure that a page can be created with a url
           '''
        page_url = 'a-page-url'
        page_creation_obj = {
            'title': 'URLPageTest',
            'page_url': page_url,
            'page_content': 'This is testing the creation of a page using the page_url attribute'
        }
        response = self.client.post(django.core.urlresolvers.reverse('pages:create'), data=json.dumps(page_creation_obj), content_type='application/json')
        
        page_creation_response_obj = {
            'wikiPage': page_url
        }
        self.assertContains(response, json.dumps(page_creation_response_obj), status_code=200)
        
    def test_create_view_valid_request_with_empty_string_url(self):
        '''
            Ensures that a page created with an empty string as a url uses the title as url
           '''
        page_title = "EmptyPageURL"
        page_creation_obj = {
            'title': page_title,
            'page_url': '',
            'page_content': 'This is testing the creation of a page using an empty string as the page_url attribute'
        }
        response = self.client.post(django.core.urlresolvers.reverse('pages:create'), data=json.dumps(page_creation_obj), content_type='application/json')
        
        page_creation_response_obj = {
            'wikiPage': page_title
        }
        self.assertContains(response, json.dumps(page_creation_response_obj), status_code=200)
        
    def test_create_view_should_return_error_if_not_post_request(self):
        '''
            Ensure that the create view only responds to post requests
           '''
        response = self.client.get(django.core.urlresolvers.reverse('pages:create'), data={"title": "AnotherTest", "page_content": "This test should not create a page"}, content_type='application/json')
        
        self.assertEquals(405, response.status_code)
        self.assertTrue('errors' in json.loads(response.content))
        
    def test_create_view_should_not_allow_duplicate_pages(self):
        '''
            Ensures that duplicate pages cannot be created
           '''
        page_url = 'duplicate-page'
        page_data = {
            'title': "DuplicatePageTest",
            'page_url': page_url,
            'page_content': "This is a test to ensure duplicate pages cannot be created"
        }
        self.client.post(django.core.urlresolvers.reverse('pages:create'), data=json.dumps(page_data), content_type='application/json')
        response = self.client.post(django.core.urlresolvers.reverse('pages:create'), data=json.dumps(page_data), content_type='application/json')
        
        self.assertContains(response, '{"errors": ["Page %s already exists"]}' % (page_url), status_code=403)
        
class WikiPageEditView(django.test.TestCase):
    def test_edit_view_renders_page(self):
        '''
            Ensure that the edit view renders the edit page form
           '''
        page_title = "EditPageTest"
        page_content = "This is a test of the edit page"
        create_page(page_title, page_title, page_content)
        response = self.client.get(django.core.urlresolvers.reverse('pages:edit', args=(page_title,)))
        
        response_page_title = '<title>Wiki: Editting %s</title>' % (page_title)
        self.assertContains(response, response_page_title, status_code=200)
        
        response_page_heading = '<h1>Editting %s</h1>' % (page_title)
        self.assertContains(response, response_page_heading, status_code=200)
        
        response_page_title_input = "<input type='text' name='title' value='%s' />" % (page_title)
        self.assertContains(response, '<label>Page Title</label>', status_code=200)
        self.assertContains(response, response_page_title_input, status_code=200)
        
        response_page_content = "<textarea name='page_content'>%s</textarea>" % (page_content)
        self.assertContains(response, '<label>Page Content</label>', status_code=200)
        self.assertContains(response, response_page_content, status_code=200)
        
    def test_edit_view_returns_404_if_no_matching_page(self):
        '''
            Ensure that the edit view returns a 404 error if a matching page cannot be found
           '''
        page_url = 'should-not-exist'
        response = self.client.get(django.core.urlresolvers.reverse('pages:edit', args=(page_url,)))
        self.assertEquals(404, response.status_code)
        
class WikiPageUpdateView(django.test.TestCase):
    def setUp(self):
        self.updated_title = 'UpdatedPageTest'
        self.updated_content = "This is the updated page content of the page"
        self.page_data = {
            'title': self.updated_title,
            'page_content': self.updated_content
        }
    
    def test_update_view_valid_request(self):
        '''
            Ensure that update view updates a wiki page
           '''
        page_url = 'update-page'
        create_page('UpdatePageTest', page_url, 'This is a test page for updating a wiki page')
        
        response = self.client.post(django.core.urlresolvers.reverse('pages:update', args=(page_url,)), data=json.dumps(self.page_data), content_type='application/json')
        
        response_json = {
            'wikiPage': page_url
        }
        self.assertContains(response, json.dumps(response_json), status_code=200)
        
        updated_page = pages.models.WikiPage.objects.get(page_url=page_url)
        self.assertEquals(self.updated_title, updated_page.title)
        self.assertEquals(self.updated_content, updated_page.page_content)
        
    def test_update_view_no_page(self):
        '''
            Ensure that update view returns error if there is no wiki page associated with url
           '''
        page_url = 'update-no-page'
        
        response = self.client.post(django.core.urlresolvers.reverse('pages:update', args=(page_url,)), data=json.dumps(self.page_data), content_type='application/json')
        
        self.assertEquals(404, response.status_code)
        self.assertTrue('errors' in json.loads(response.content))
        
    def test_update_view_non_post_request(self):
        '''
            Ensure that update view throws errors a non post request
           '''
        page_url = 'update-no-page'
        
        response = self.client.get(django.core.urlresolvers.reverse('pages:update', args=(page_url,)), data=self.page_data, content_type='application/json')
        
        self.assertEquals(405, response.status_code)
        self.assertTrue('errors' in json.loads(response.content))