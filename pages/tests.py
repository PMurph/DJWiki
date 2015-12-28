import django.core.urlresolvers
import django.utils
import django.test
import pages.models

class WikiPageModelTest(django.test.TestCase):
    def setUp(self):
        self.page_title = "TestPage"
        self.page_content = "This is a test page"
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
        
    def test_model_variables(self):
        '''
            Ensure all model variables are set properly
           '''
        self.assertEquals(self.page_title, self.test_page.title)
        self.assertEquals(self.page_content, self.test_page.page_content)
        self.assertEquals(self.created_date, self.test_page.created_date)
        self.assertEquals(self.last_modified, self.test_page.last_modified)
        
    def test_created_date_not_null(self):
        '''
             Ensure that the created date is set when object is created
            '''
        newWikiPage = pages.models.WikiPage()
        self.assertIsNotNone(newWikiPage.created_date)
        
class WikiPageDetailView(django.test.TestCase):
    def setUp(self):
        self.page_title = "TestProject"
        self.page_content = u"This is a test project."
        
    def create_page(self, page_title, page_content):
        pages.models.WikiPage.objects.create(title=page_title, page_content=page_content, created_date=django.utils.timezone.now(), last_modified=django.utils.timezone.now())

    def test_detail_view_renders_page(self):
        '''
            Ensure that the test project page loads
           '''
        self.create_page(self.page_title, self.page_content)
        
        response = self.client.get(django.core.urlresolvers.reverse('pages:detail', args=(self.page_title,)))
        self.assertContains(response, self.page_title, status_code=200)
        self.assertContains(response, self.page_content, status_code=200)
        
class WikiPageNewView(django.test.TestCase):
    def test_new_view_renders_page(self):
        '''
            Ensure that the new page renders that new page form
           '''
        response = self.client.get(django.core.urlresolvers.reverse('pages:new'))
        self.assertContains(response, '<h1>Create New Wiki Page</h1>', status_code=200)
        self.assertContains(response, '<label>Page Title</label>', status_code=200)
        self.assertContains(response, "<input type='text' name='title' />", status_code=200)
        self.assertContains(response, '<label>Page Content</label>', status_code=200)
        self.assertContains(response, "<textarea name='page_content'>", status_code=200)
        
class WikiPageCreateView(django.test.TestCase):
    def test_create_view_valid_request(self):
        '''
             Ensure that the create view creates a wiki page
            '''
        response = self.client.post(django.core.urlresolvers.reverse('pages:create'), data='{"title": "CreatePageTest", "page_content": "This is a test for create page view"}', content_type='application/json')
        
        self.assertContains(response, '{"wikiPage": "CreatePageTest"}', status_code=200)
        
    def test_create_view_should_return_error_if_not_post_request(self):
        '''
            Ensure that the create view only responds to post requests
           '''
        response = self.client.get(django.core.urlresolvers.reverse('pages:create'), data={"title": "AnotherTest", "page_content": "This test should not create a page"}, content_type='application/json')
        
        self.assertEquals(405, response.status_code)