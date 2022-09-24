#
# python3 manage.py create_view "myapp" "user" "User" "/users/[User:id]{user_id}"
#

import re
import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from myapp.models import UserAddress, User

class Command(BaseCommand):
    help = 'Create Buyer.'

    def add_arguments(self, parser):
        parser.add_argument('name')
        parser.add_argument('email')
        parser.add_argument('password')
        parser.add_argument('address_line1')
        parser.add_argument('address_line2')
        parser.add_argument('address_line3')

    def handle(self, *args, **options):

        print()

        name = options['name']
        email = options['email']
        password = options['password']

        address_line1 = options['address_line1']
        address_line2 = options['address_line2']
        address_line3 = options['address_line3']

        if User.objects.filter(email=email).first() is None:
            user = User()
            user.email = email
            user.first_name = name
            user.is_buyer = True
            user.is_active = True
            user.set_password(password)
            user.save()

            user_address = UserAddress()
            user_address.address_line1 = address_line1
            user_address.address_line2 = address_line2
            user_address.address_line3 = address_line3
            user_address.user = user
            user_address.save()
            user.save()
            print('Done.')
        else:
            print ( 'Sorry...!!! Email address already existing.')

        print()