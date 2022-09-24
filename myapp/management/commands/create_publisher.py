#
# python3 manage.py create_view "myapp" "user" "User" "/users/[User:id]{user_id}"
#

import re
import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from myapp.models import Publisher, User

class Command(BaseCommand):
    help = 'Create publisher.'

    def add_arguments(self, parser):
        parser.add_argument('name')
        parser.add_argument('email')
        parser.add_argument('password')

    def handle(self, *args, **options):

        print()

        name = options['name']
        email = options['email']
        password = options['password']

        if User.objects.filter(email=email).first() is None:
            user = User()
            user.email = email
            user.first_name = name
            user.is_publisher = True
            user.is_active = True
            user.set_password(password)
            user.save()

            publisher = Publisher()
            publisher.name = name
            publisher.save()

            user.publisher = publisher
            user.save()
            print('Done.')
        else:
            print ( 'Sorry...!!! Email address already existing.')

        print()