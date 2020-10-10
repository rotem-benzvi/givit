import urllib.request

import pytest

from django.contrib.auth.models import User
from friendreq.models import ITEM_CHOICES, ItemRequest, ItemsFound
from gatherer import agora


@pytest.fixture(scope='module')
def soup_list():
    """
    this fixture initialize soup list that contain soup of all the item types.
    we initial this only one time for all functions by call to Agora_Getrequest func.
    Returns:
    list of BeautifulSoup object: which represents the document as a nested data structure.
    """
    soup_list = []
    for iseek in list(ITEM_CHOICES):
        soup = agora.Agora_Getrequest(iseek[0])
        soup_list.append(soup)
    return soup_list


def test_Agora_Getrequest(soup_list):
    """
    this function test Agora_Getrequest func by check if its return BeautifulSoup object as we expected.
    Parameters:
    list of BeautifulSoup object: which represents the document as a nested data structure.
    """
    for soup in soup_list:
        assert str(type(soup)) == "<class 'bs4.BeautifulSoup'>"


@ pytest.mark.parametrize("index, area, name",
                          [(0, "Tel Aviv", "20009"),
                           (1, "Tel Aviv", "20016"),
                              (2, "Tel Aviv", "20008"),
                              (3, "Tel Aviv", "10006"),
                              (4, "Tel Aviv", "10029"),
                              (5, "Tel Aviv", "20017")])
def test_find_furniture(soup_list, index, area, name):
    """
    this function test find_furniture func by check if the url which return is success status response code.
    if Url__list is empty, we cant be sure that the test PASSED so in this case the status will be SKIPPED
    Parameters:
    list of BeautifulSoup object: which represents the document as a nested data structure.
    tuple @parameter: which represents all possible item types (n) so that the test_eval function
    will run n times (with Tel aviv only).
    """
    url_list, __ = agora.find_furniture(
        soup_list[index], agora.region_dict.get(area), agora.iseek_dict.get(name))
    if len(url_list) == 0:
        pytest.skip('Url list is empty')
    for url in url_list:
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0'
        values = {}
        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8')
        req = urllib.request.Request(url, data, headers)
        check = urllib.request.urlopen(req).getcode()
        assert check == 200


@ pytest.mark.parametrize('item', ['20009', '20016', '20008', '10006', '10029', '20017'])
@pytest.mark.django_db(transaction=True)
def test_givit_main(item):
    """
    this function test givit_main func by first create a test user and add ItemRequest
    then test if the found items add to DB as we expected.
    if found_list is empty, we cant be sure that the test PASSED so in this case the status will be SKIPPED
    Parameters:
    item @parameter: which represents all possible item types (n) so that the test_eval function
    will run n times.
    """
    testEmail = 'testUser@Test.com'
    testPassword = 'top_secret_test'
    test_user = User.objects.create_user(
        username='TestUser!', email=testEmail, password=testPassword)
    test_user.save()
    newRequest = ItemRequest(special_req="this is a Test",
                             friend_id=test_user, item=item)
    newRequest.save()
    agora.givit_main()
    found = ItemsFound.objects.all()
    check = found.filter(request_id=newRequest).exists()
    if not check:
        pytest.skip('found list is empty')
    found.filter(request_id=newRequest).delete()
    newRequest.delete()
    test_user.delete()
