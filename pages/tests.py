import django.core.urlresolvers
import django.utils
import django.test
import json
import pages.models

class WikiPageModelTest(django.test.TestCase):
    def setUp(self):
        self.page_title = "TestPage"
        self.page_content = "This is a test page"
        self.page_url = 'an-explicit-page-url'
        self.created_date = django.utils.timezone.now()
        self.last_modified = django.utils.timezone.now()
        self.test_page = pages.models.WikiPage(title=self.page_title, page_content=self.page_content, created_date=self.created_date, last_modified=self.last_modified)

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
        self.assertEquals(self.page_title, self.test_page.page_url)
        self.assertEquals(self.page_content, self.test_page.page_content)
        self.assertEquals(self.created_date, self.test_page.created_date)
        self.assertEquals(self.last_modified, self.test_page.last_modified)
        
    def test_model_variables_url(self):
        '''
            Ensures that the page_url property is set if explicit url is set
           '''
        test_page = pages.models.WikiPage(title=self.page_title, page_url=self.page_url, page_content=self.page_content, created_date=self.created_date, last_modified=self.last_modified)
        
        self.assertEquals(self.page_url, test_page.page_url)
        
    def test_model_variables_url_is_None(self):
        '''
            Ensures that if the page_url property is specified to be None, the functionality is the same as if no url was specified
           '''
        test_page = pages.models.WikiPage(title=self.page_title, page_url=None, page_content=self.page_content, created_date=self.created_date, last_modified=self.last_modified)
        
        self.assertEquals(self.page_title, test_page.page_url)
        
    def test_created_date_not_null(self):
        '''
             Ensure that the created date is set when object is created
            '''
        newWikiPage = pages.models.WikiPage()
        self.assertIsNotNone(newWikiPage.created_date)
        
class WikiPageDetailView(django.test.TestCase):
    def create_page(self, page_title, page_url, page_content):
        pages.models.WikiPage.objects.create(title=page_title, page_url=page_url, page_content=page_content, created_date=django.utils.timezone.now(), last_modified=django.utils.timezone.now())

    def test_detail_view_renders_page(self):
        '''
            Ensure that the test project page loads
           '''
        page_title = "TestProject"
        page_content = u"This is a test project."
        self.create_page(page_title, page_title, page_content)
        
        response = self.client.get(django.core.urlresolvers.reverse('pages:detail', args=(page_title,)))
        self.assertContains(response, page_title, status_code=200)
        self.assertContains(response, page_content, status_code=200)
        
    def test_detail_view_renders_page_with_separate_url_from_title(self):
        '''
            Ensure that the a page with different titles and url
           '''
        page_title = "URLTestProject"
        page_url = "url-test-project"
        page_content = u"This is to test that a project with a separate title and url renders"
        self.create_page(page_title, page_url, page_content)
        
        response = self.client.get(django.core.urlresolvers.reverse('pages:detail', args=(page_url,)))
        self.assertContains(response, page_title, status_code=200)
        self.assertContains(response, page_content, status_code=200)
        
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
        response = self.client.post(django.core.urlresolvers.reverse('pages:create'), data='{"title": "CreatePageTest", "page_content": "This is a test for create page view"}', content_type='application/json')
        
        self.assertContains(response, '{"wikiPage": "CreatePageTest"}', status_code=200)
        
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
        
    def test_create_view_should_not_allow_duplicate_pages(self):
        '''
            Ensures that duplicate pages cannot be created
           '''
        page_name = "DuplicatePageTest"
        page_data = '{"title": "%s", "page_content": "This is a test to ensure duplicate pages cannot be created"}' % (page_name)
        self.client.post(django.core.urlresolvers.reverse('pages:create'), data=page_data, content_type='application/json')
        response = self.client.post(django.core.urlresolvers.reverse('pages:create'), data=page_data, content_type='application/json')
        
        self.assertContains(response, '{"errors": ["Page %s already exists"]}' % (page_name), status_code=403)