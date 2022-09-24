#
# python3 manage.py create_serializer "myapp" "User" "UserSerializer"
#

import re, json, os, importlib, inspect, pprint, random

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Model
from django.contrib.admin.models import LogEntryManager
from django.db.models import *

from .utils import view
from .utils import serializer

class Command(BaseCommand):
    help = 'Create serializer based on information.'

    def add_arguments(self, parser):
        parser.add_argument('app_name')
        parser.add_argument('option', type=str, nargs='?', default='makemigrations')

    def handle(self, *args, **options):

        print()

        pp = pprint.PrettyPrinter(indent=4)
        models_details = []
        
        index = 0
        _models = []
        app_name = options['app_name']
        module = importlib.import_module(str(app_name)+'.models')
        models = inspect.getmembers(module, inspect.isclass)
        for m in models:
            _models.append([
                inspect.findsource(m[1])[1],
                m[0],
                m[1]
            ])
        _models = sorted(_models, key=lambda x: (x[0]))
        models = _models
        for lno, name, obj in models:
            try:
                try:
                    model_fields = obj._meta.get_fields()
                    fields = []
                    for full_field_name in model_fields:
                        field = (str(full_field_name).split('.'))[-1]
                        obj_field = full_field_name

                        if isinstance(obj_field, ManyToManyField):
                            continue
                        
                        if isinstance(obj_field, AutoField):
                            continue

                        if isinstance(obj_field, DateTimeField):
                            _field = field
                            _get_value = 'get_rand_datetime(from_datetime="today", to_datetime="+10 days")'
                            fields.append({ _field: _get_value })
                            continue

                        if isinstance(obj_field, DateField):
                            _field = field
                            _get_value = 'get_rand_date(from_date="today", to_date="+10 days")'
                            fields.append({ _field: _get_value })
                            continue
                        
                        if isinstance(obj_field, FileField):
                            _field = field
                            _get_value = 'get_rand_file()'
                            fields.append({ _field: _get_value })
                            continue

                        if isinstance(obj_field, ImageField):
                            _field = field
                            _get_value = 'get_rand_image()'
                            fields.append({ _field: _get_value })
                            continue
                        
                        if isinstance(obj_field, BooleanField):
                            _field = field
                            _get_value = 'True if random.random() > 0.5 else False'
                            fields.append({ _field: _get_value })
                            continue
                        
                        if isinstance(obj_field, CharField):
                            _field = field
                            _get_value = 'get_rand_char()'
                            fields.append({ _field: _get_value })
                            continue
                        
                        if isinstance(obj_field, TextField):
                            _field = field
                            _get_value = 'get_rand_text()'
                            fields.append({ _field: _get_value })
                            continue

                        if isinstance(obj_field, ForeignKey):
                            _field = field
                            _get_value = 'get_rand_model("' + _model_name + '")'
                            fields.append({ _field: _get_value })
                            continue

                    _model_name = self.fullname(full_field_name.__dict__['model'])
                                
                    models_details.append(
                        [
                            100,
                            _model_name,
                            fields
                        ]
                    )
                    index = index + 1
                except Exception as e:
                    print (e)
            except Exception as e:
                pass

        pp.pprint(models_details)

    def fullname(self, o):
        return o.__module__ + "." + o.__name__
