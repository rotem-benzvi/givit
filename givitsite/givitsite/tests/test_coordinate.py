from coordinate.models import CoordinatedItems
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client, TestCase
from friendreq.models import ItemRequest, ItemsFound

ENTRY_URL = '/coordinate/'
URL_NAME_LIST = ['coordinator_create_view']
HTML_TEMPLATE_NAME = 'coordinator.html'
DEFAULT_ITEM_VALUE = '20009'
DEFAULT_REGION_VALUE = 'Tel Aviv'
DEFAULT_STUDENT_PHONE_NUMBER = '0544445556'
MOCK_ITEMS_LIST = [
    {
        'request_id': 'request 1',
        'city': 'Test City 1',
        'item': 'Test Item 1',
        'matched': True
    },
    {
        'request_id': 'request 2',
        'city': 'Test City 2',
        'item': 'Test Item 2',
        'matched': True
    },
    {
        'request_id': 'request 3',
        'city': 'Test City 3',
        'item': 'Test Item 3',
        'matched': False
    }
]


def prepareDB(self):
    for request in MOCK_ITEMS_LIST:
        item_request = ItemRequest.objects.create(
            friend_id=self.test_user, status="in_process")
        ItemsFound.objects.create(
            request_id=item_request, match=request.get('matched'),
            city=request.get('city'), title=request.get('item'))


class CoordinatePageTests_views_GET(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='TestUser!')
        prepareDB(self)

    # check the status code when navigate to the given url
    def test_request_status_code(self):
        response = self.client.get(ENTRY_URL)
        self.assertEqual(response.status_code, 200)

    # check url name
    def test_request_url_name(self):
        for url_name in URL_NAME_LIST:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)

    # check that the template is being rendered with all the mathced item
    def test_matched_items_tamplate(self):
        matchedItem = ItemsFound.objects.filter(match=True)
        unMatchedItems = ItemsFound.objects.filter(match=False)
        response = self.client.get(ENTRY_URL)
        self.assertTemplateUsed(HTML_TEMPLATE_NAME)
        for item in matchedItem:
            self.assertContains(response, item.title)
        for item in unMatchedItems:
            self.assertNotContains(response, item.title)

    # test that only items that match the item filter are being rendered
    def test_view_filters(self):
        allMatchedItems = ItemsFound.objects.filter(match=True)

        # Test the 'pickup city' filter
        cityFilter = allMatchedItems.first().city
        filterCityResponse = self.send_filter_get_request(city=cityFilter)
        self.assertContains(filterCityResponse, cityFilter, status_code=200)
        for item in allMatchedItems.exclude(city=cityFilter):
            self.assertNotContains(filterCityResponse, item.city)

        # Test the 'item type' filter
        itemFilter = allMatchedItems.first().title
        filterItemResponse = self.send_filter_get_request(item=itemFilter)
        self.assertContains(filterItemResponse, itemFilter, status_code=200)
        for item in allMatchedItems.exclude(title=itemFilter):
            self.assertNotContains(filterItemResponse, item.title)

    # Util function to send get request with specific filters
    def send_filter_get_request(self, city='', item=''):
        response = self.client.get(
            ENTRY_URL, {'city_pickup': city, 'item': item})
        return response


class CoordinatePageTests_views_POST(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='TestUser!')
        prepareDB(self)

    def test_post_request_status_code(self):
        response = self.client.post(ENTRY_URL)
        self.assertEqual(response.status_code, 302)

    def test_post_coordination_data(self):
        matchedItems = ItemsFound.objects.filter(match=True)
        for item in matchedItems:
            formData = {
                "item": DEFAULT_ITEM_VALUE,
                "transfer_date": '2020-09-25',
                "request_id": item.request_id.id,
                "pickup_location": DEFAULT_REGION_VALUE,
                "drop_off_location": DEFAULT_REGION_VALUE,
                "student_phone_number": DEFAULT_STUDENT_PHONE_NUMBER,
                "pickup_time": '19:00',
                "drop_off_time": '19:30'
            }

            # post data & verify the item request status changed to 'closed'
            self.client.post(ENTRY_URL, formData)
            self.assertEqual(ItemRequest.objects.get(
                id=item.request_id.id).status, 'closed')
        coordinated = CoordinatedItems.objects.all()
        self.assertEqual(len(coordinated),
                         len(matchedItems))
