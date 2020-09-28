from accounts.views import get_user_profile_data
# from django.contrib.auth.models import User
from django.shortcuts import render


def home(request):
    if request.user.is_authenticated:
        user_profile = get_user_profile_data(request.user)
        render_dict = {'user_profile': user_profile}
        return render(request, 'home.html', render_dict)
    else:
        return render(request, 'home.html')
