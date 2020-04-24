from time import time

import clearbit
from django.conf import settings
from django.utils.text import slugify

from pyhunter import PyHunter

hunter = PyHunter(settings.EMAIL_HUNTER_API_KEY)
clearbit.key = settings.CLEARBIT_API_KEY


def clearbit_signup(email):
    person = clearbit.Person.find(email=email, stream=True)
    if person is not None:
        first_name = str(person['name']['givenName'])
        last_name = str(person['name']['familyName'])
        return first_name, last_name
    return '', ''


def custom_slugify(slug):
    new_slug = slugify(slug, allow_unicode=True)
    return new_slug + '-' + str(int(time()))
