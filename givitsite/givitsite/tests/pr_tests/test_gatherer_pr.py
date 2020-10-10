import urllib.request

import pytest
from bs4 import BeautifulSoup
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
    url0 = "givitsite/tests/html/bed.html"
    soup0 = BeautifulSoup(open(url0).read(), features="html.parser")
    soup_list.append(soup0)
    url1 = "givitsite/tests/html/closet.html"
    soup = BeautifulSoup(open(url1).read(), features="html.parser")
    soup_list.append(soup)
    return soup_list


@ pytest.mark.parametrize("index, area, name",
                          [(0, "Tel Aviv", "20016"), (1, "Tel Aviv", "20009")])
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
    assert len(url_list) > 0
