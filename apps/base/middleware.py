""" Middleware """

from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Profile
from utils import has_profile

class CheckProfileMiddleware(object):
    """
    Checks for whether a user has a profile or not. If a logged in user does not have a profile created,
    then they are redirected to the profile create page.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if ( not request.path.startswith("/admin") and 
             not request.path.startswith("/api") and 
             request.path != reverse('profile-create') and
             request.user.is_authenticated
             ):
            if not has_profile(request.user):
                return HttpResponseRedirect(reverse('profile-create'))
        return self.get_response(request)
