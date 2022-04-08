from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import News,Category
from django.contrib.auth.models import User

class NewsTest(APITestCase):

    def test_view_posts(self):

        url = reverse('kmo_api:listcreate')
        response = self.client.get(url,format='json') #client == browser

        self.assertEqual(response.status_code,status.HTTP_200_OK)

    
    def create_news(self):
        self.test_category = Category.objects.create(name='django')

        self.testuser1 = User.objects.create_user(username='testuser1',password='123456')

        data = {
            "title":"new", "excerpt": "new", "content":"new"
        }

        url = reverse('kmo_api:listcreate')
        response = self.client.post(url,data,format='json')

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


