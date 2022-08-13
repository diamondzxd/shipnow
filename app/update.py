# File for working with a 3rd Party API in a Django System.
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shipnow.settings")
import django
django.setup()

from main.models import Address
addresses=Address.objects.all()
for a in addresses:
    print(a.name)
