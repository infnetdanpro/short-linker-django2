from .models import Links
from random import randint

def generate_redirect_url():
    count = Links.objects.count()
    rand = randint(0, int(count)*1000)
    success = False

    while success is False:
        try:
            link_exists = Links.objects.get(link_redirect=rand)
            success = False
        except:
            success = True
    return rand