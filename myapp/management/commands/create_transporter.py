#
# python3 manage.py create_view "myapp" "user" "User" "/users/[User:id]{user_id}"
#

import re
import json
import os
from xmlrpc.client import Transport
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from myapp.models import Transporter, User

class Command(BaseCommand):
    help = 'Create transporter.'

    def add_arguments(self, parser):
        parser.add_argument('name')
        parser.add_argument('email')
        parser.add_argument('password')

    def handle(self, *args, **options):

        print()

        name = options['name']
        email = options['email']
        passwrod = options['password']

        if User.objects.filter(email=email).first() is None:
            user = User()
            user.email = email
            user.first_name = name
            user.is_transporter = True
            user.is_active = True
            user.set_password(passwrod)
            user.save()

            transporter = Transporter()
            transporter.name = name
            transporter.save()

            user.transporter = transporter
            user.save()
            print('Done.')
        else:
            print ( 'Sorry...!!! Email address already existing.')

        print()