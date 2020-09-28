from accounts.views import get_user_profile_data
from django.db import transaction
from django.shortcuts import render

from .forms import itemRequestForm
from .models import ItemRequest, ItemsFound


def itemRequest_create_view(request):
    user_profile = user_profile = get_user_profile_data(request.user)
    form = itemRequestForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            fs = form.save(commit=False)
            fs.friend_id = request.user
            fs.save()
        context = {
            'form': form,
            'user_profile': user_profile
        }
        return render(request, "demandDB.html", context)
    else:
        context = {
            'form': form,
            'user_profile': user_profile
        }
        return render(request, 'itemRequestform.html', context)


def requestItem(request):
    # on match
    user_profile = user_profile = get_user_profile_data(request.user)
    if request.method == 'POST':
        with transaction.atomic():
            item_id = request.POST["item_id"]
            ItemsFound.objects.filter(
                pk=item_id).update(match=True)
            req_id = request.POST["req_id"]
            ItemRequest.objects.filter(
                pk=req_id).update(status='in_process')

    founditems = ItemsFound.objects.all()
    allrequests = ItemRequest.objects.filter(status='open')
    context = {'founds': founditems, 'allRequests': allrequests,
               'user_profile': user_profile}
    return render(request, 'feed.html', context)
