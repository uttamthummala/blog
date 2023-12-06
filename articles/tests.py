from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from .models import Article

class articlesViewsTests(TestCase):
    def setUp(self):
        self.user = mixer.blend(User, username='testuser')
        self.client.force_login(self.user)

    def test_dashboard_view(self):
        mixer.blend(Article, author=self.user, title='Test Article')

        url = reverse('dashboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertContains(response, b'Test Article')

    def test_edit_article_view(self):
        article = mixer.blend(Article, author=self.user)

        url = reverse('edit_article', args=[article.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_article.html')
        self.assertContains(response, b'Edit Article')

    def test_article_detail_view(self):
        article = mixer.blend(Article, author=self.user, title='Test Article', content='Test Content')

        url = reverse('article_detail', args=[article.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_detail.html')
        self.assertContains(response, b'Test Article')
        self.assertContains(response, b'Test Content')

    def test_delete_article_view(self):
        article = mixer.blend(Article, author=self.user)

        url = reverse('delete_article', args=[article.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_article.html')

        # Test the actual deletion
        response = self.client.post(url)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertFalse(Article.objects.filter(id=article.id).exists())
    def test_dashboard_view_with_no_articles(self):
        url = reverse('dashboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertContains(response, b'No articles available.')

    def test_dashboard_view_pagination(self):
        # Create more than the default pagination count (assuming it's set to 3)
        mixer.cycle(5).blend(Article, author=self.user)

        url = reverse('dashboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertContains(response, b'Page 1 of 2')  # Assuming there are 5 articles, and pagination is set to 3 per page

    def test_edit_article_view_post_request(self):
        article = mixer.blend(Article, author=self.user)

        url = reverse('edit_article', args=[article.id])
        data = {'title': 'Updated Title', 'content': 'Updated Content', 'tags': 'updated, tags'}
        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_detail.html')
    

    def test_delete_article_view_confirmation(self):
        article = mixer.blend(Article, author=self.user)

        url = reverse('delete_article', args=[article.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_article.html')
        response=self.client.post(url)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertFalse(Article.objects.filter(id=article.id).exists())

    def test_search_articles(self):
        mixer.blend(Article, author=self.user, title='Search Test', tags='search, test')
        url = reverse('dashboard')

        # Search by title
        
        response = self.client.get(url, {'q': 'Search Test', 'filter_option': 'title'})
        self.assertContains(response, b'Search Test')

        # Search by tags
        response = self.client.get(url, {'q': 'search', 'filter_option': 'tags'})
        self.assertContains(response, b'Search Test')

        mixer.blend(Article, author=self.user, title='Search Test', content="hai test",tags='search, test')
        response = self.client.get(url, {'q': 'test', 'filter_option': 'content'})
        self.assertContains(response,b'test')


