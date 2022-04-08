from django.test import TestCase
from django.contrib.auth.models import User
from core.models import News,Category

class Test_Create_Post(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_category = Category.objects.create(name='django')
        testuser1= User.objects.create_user(
            username='testuser1',password='123456')

        test_news = News.objects.create(
            category_id=1,title='Test Title',excerpt='Test excerpt', content='Test content',slug='test-title',status='published'
        )

    def test_news_content(self):
        news = News.newsobjects.get(id=1)
        cat =  Category.objects.get(id=1)
        excerpt = f'{news.excerpt}'   
        title= f'{news.title}'
        content= f'{news.content}'
        status= f'{news.status}'    

        #testing

        self.assertEqual(content,'Test content')
        self.assertEqual(status,'published')
        self.assertEqual(title,'Test Title')
        self.assertEqual(str(news),"Test Title") #checking string method(return self.title) of the news object to make sure its string method returns the correct value
        self.assertEqual(str(cat),"django")