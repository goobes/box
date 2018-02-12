
from base.models import Profile

def has_profile(user):
    if not user.is_authenticated:
        return False
    if Profile.objects.filter(user=user).first() is None:
        return False
    else:
        return True
