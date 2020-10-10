from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client, TestCase
from friendreq.models import ItemRequest

URL_LIST = ['/friend/feed']
URL_NAME_LIST = ['requestItem']


class FriendPageTests_views_GET(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    # check the status code when navigate to the given url

    def test_request_status_code(self):
        for url in URL_LIST:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    # check url name
    def test_request_url_name(self):
        for url_name in URL_NAME_LIST:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)

    # check if the correct template is being rendered

    def test_feed_correct_tamplate(self):
        response = self.client.get(reverse('requestItem'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')


class ItemRequest_test(TestCase):
    def setUp(self):
        testEmail = 'testUser@Test.com'
        testPassword = 'top_secret_test'
        self.test_user = User.objects.create_user(
            username='TestUser!', email=testEmail, password=testPassword)
        ItemRequest.objects.create(
            special_req="this is a Test", friend_id=self.test_user)

    def test_text(self):
        # check insersion of request to the ItemRequest table
        req = ItemRequest.objects.get(friend_id=self.test_user)
        temp_special_request = req.special_req
        self.assertEqual(temp_special_request, "this is a Test")
