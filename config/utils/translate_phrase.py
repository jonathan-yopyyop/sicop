from django.contrib.auth.models import Permission
from django.utils.translation import gettext as _


def translate_phrase(phrase):
    splited_phrase = phrase.split()
    for word in splited_phrase:
        print(word)


def translate_permissions():
    permissions = Permission.objects.all()
    for permission in permissions:
        permission_name = _(str(permission.name))
        print(permission_name)
