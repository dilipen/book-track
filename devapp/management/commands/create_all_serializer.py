#
# python3 manage.py create_serializer "myapp" "User" "UserSerializer"
#

import os
import sys
import inspect
from ast import ClassDef, parse

from django.apps import apps
from django.core.management.base import BaseCommand

from .utils import view
from .utils import serializer


class Command(BaseCommand):
    help = 'Create serializer based on information.'

    def add_arguments(self, parser):
        parser.add_argument('app_name')

    def handle(self, *args, **options):

        print()

        app_name = options['app_name']
        serializer_module = sys.modules[app_name + '.' + 'serializers']
        pack = parse(inspect.getsource(serializer_module))
        serializer_names = [kls.name for kls in pack.body if isinstance(kls, ClassDef)]  # NOQA

        models = apps.all_models[app_name]
        
        for k, v in models.items():
            model_name = v.__name__
            serializer_name = model_name + 'Serializer'
            if model_name in ['User_groups', 'User_user_permissions']:
                continue
            if not serializer_name in serializer_names:
                model_path = './' + ( model_name.replace('.', '/') ) + '.py'
                serializer_path = './' + app_name + '/' +  'serializers.py'

                fields_list, readonly_fields_list = serializer.get_model_fields( app_name, model_name )
                
                context_dict = {
                    'model_name': model_name,
                    'fields_list': fields_list,
                    'readonly_fields_list': readonly_fields_list,
                    'serializer_name': serializer_name,
                }
                
                text = ''
                
                if not os.path.exists( serializer_path ):
                    serializer_imports_string = serializer.get_serializer_imports_as_string( )
                    serializer_class_string = serializer.get_serializer_class_as_string( context_dict )
                    text = view.mergeAsText(
                        serializer_imports_string,
                        serializer_class_string
                    )
                else:
                    serializer_class_string = serializer.get_serializer_class_as_string( context_dict )
                    text = serializer_class_string
                
                with open( serializer_path, 'a') as f:
                    f.write( text )
        
        print('Done')
        print()
