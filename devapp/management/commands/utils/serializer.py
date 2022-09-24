import re, os, importlib

from django.template import Context, Template
    
def underscore_to_camel(in_str):
    _return = ""
    _force_next_ch_has_upper = True
    for ch in in_str:
        if _force_next_ch_has_upper == True:
            _return = _return + ch.upper()
            _force_next_ch_has_upper = False
        elif ch != "_":
            _return = _return + ch.lower()
        if ch == "_":
            _force_next_ch_has_upper = True
    return _return

def get_model_fields( app_name,  model_name ):
    models = importlib.import_module( '.models', package=app_name )
    model = getattr( models, model_name )
    model_fields = model._meta.get_fields()
    
    fields = []
    for full_field_name in model_fields:
        field = (str(full_field_name).split('.'))[-1]
        fields.append( field )
    
    readonly_fields = []

    for i, field in enumerate(fields):
        if field == 'created_at':
            readonly_fields.append( 'created_at' )
        if field == 'modified_at':
            readonly_fields.append( 'modified_at' )

    return fields, readonly_fields

def get_serializer_class_as_string( context_dict ):
    file_path = "./devapp/management/commands/templates/serializer_class.html.py"
    
    template = render(file_path, context_dict)

    return template

def get_serializer_imports_as_string():
    file_path = "./devapp/management/commands/templates/serializer_imports.html.py"
    
    template = render(file_path)

    return template

def mergeAsText(*args, **options):
    return ("\n".join(args))

def render(file_path, context_data = {}):
    if not os.path.exists(file_path):
        print (' Sorry: Template file not exist.')
    else:
        with open(file_path, 'r') as myfile:
            data = myfile.read()
            t = Template(data)

            c = Context(context_data, autoescape=False)
            return t.render(c)
