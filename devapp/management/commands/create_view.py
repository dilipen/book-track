#
# python3 manage.py create_view "myapp" "user" "User" "/users/[User:id]{user_id}"
#

import re
import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from .utils import view

class Command(BaseCommand):
    help = 'Create views based on given url.'

    def add_arguments(self, parser):
        parser.add_argument('app_name')
        parser.add_argument('file_name')
        parser.add_argument('class_name')
        parser.add_argument('urls', nargs='+')

    def handle(self, *args, **options):
        self.url_details = view.url_details(options)

        # print (json.dumps(self.url_details, indent=4, sort_keys=True))

        print()

        app_name = self.url_details['app_name']
        url_name = self.url_details['file_name']

        if not os.path.exists(app_name +'/views/'+url_name+'.py'):

            text = view.mergeAsText(
                view.general_imports(self.url_details) ,
                view.get_create_list(self.url_details) ,
                view.get_update_delete_view(self.url_details)
            )

            with open(app_name +'/views/'+url_name+'.py', 'a') as f:
                f.write( text )

            urls_string = view.get_urls(self.url_details)
            urls_file = './' + app_name +'/urls.py'

            if not os.path.exists(urls_file):
                text = view.get_urls_general_imports()
                with open(urls_file, 'a') as f:
                    f.write( text )
            
            with open(urls_file, 'a') as f:
                    f.write( urls_string )

        else:
            print ( 'Sorry...!!! File already existing.')

        print()