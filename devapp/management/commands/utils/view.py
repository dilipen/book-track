import re, os

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

def url_details(options):
    app_name = options['app_name']
    file_name = options['file_name']
    class_name = options['class_name']
    routes_count = 0
    routes_details_dict = []
    for url in iter(options['urls']):
        if url[0] == '/':
            _routes = url.split('/')
            if _routes[0] == '':
                for _route in iter(_routes):
                    if _route == '':
                        pass
                    
                    patten = '\[([A-Za-z0-9_\.]+)\]\{([A-Za-z0-9_\.]+)\}'
                    if re.search(patten, _route):
                        result = (re.split(patten, _route))
                        _entity = result[1]
                        _argument = result[2]
                        routes_details_dict.append({
                            'type': 'entity',
                            'entity': _entity,
                            'serializer': _entity + "Serializer",
                            'primary_key': 'pk',
                            'argument': _argument,
                        })
                        routes_count = routes_count + 1
                        continue
                    
                    patten = '\[([A-Za-z0-9_\.]+)\:([A-Za-z0-9_\.]+)\]\{([A-Za-z0-9_\.]+)\}'
                    if re.search(patten, _route):
                        result = (re.split(patten, _route))
                        _entity = result[1]
                        _id = result[2]
                        _argument = result[3]
                        routes_details_dict.append({
                            'type': 'entity',
                            'entity': _entity,
                            'serializer': _entity + "Serializer",
                            'primary_key': _id,
                            'argument': _argument,
                        })
                        routes_count = routes_count + 1
                        continue
                    
                    patten = '\[([A-Za-z0-9_\.]+)\<([A-Za-z0-9_\.]+)\>\:([A-Za-z0-9_\.]+)\]\{([A-Za-z0-9_\.]+)\}'
                    if re.search(patten, _route):
                        result = (re.split(patten, _route))
                        _entity = result[1]
                        _serializer = result[2]
                        _id = result[3]
                        _argument = result[4]
                        routes_details_dict.append({
                            'type': 'entity',
                            'entity': _entity,
                            'serializer': _serializer,
                            'primary_key': _id,
                            'argument': _argument,
                        })
                        routes_count = routes_count + 1
                        continue
                    
                    patten = '\{([A-Za-z0-9_\.]+)\}'
                    if re.search(patten, _route):
                        result = (re.split(patten, _route))
                        _argument = result[1]
                        routes_details_dict.append({
                            'type': 'argument',
                            'argument': _argument,
                        })
                        routes_count = routes_count + 1
                        continue
                    
                    if not _route == '':
                        routes_details_dict.append({
                            'type': 'plain',
                            'text': _route,
                        })
                        routes_count = routes_count + 1
                        continue

    return {
        'app_name': app_name,
        'file_name': file_name,
        'class_name': class_name,
        'routes_count': routes_count,
        'routes_details_dict': routes_details_dict,
    }   

def general_imports(details):
    file_path = "./devapp/management/commands/templates/view_imports.html.py"
    
    template = render(file_path, {
        'app_name': details['app_name'],
    })

    return template

def get_last_entity_route( details ):
    last_route = None
    for _route in details['routes_details_dict']:
        if 'argument' in _route:
            last_route = _route
    return last_route

def get_last_entity_name( details ):
    last_route = get_last_entity_route( details )
    return last_route['entity']

def get_last_serializer_name( details ):
    last_route = get_last_entity_route( details )
    return last_route['serializer']

def get_arguments_as_list( details ):
    arguments = []
    for _route in details['routes_details_dict']:
        if 'argument' in _route:
            arguments.append(_route['argument'])
    return arguments

def get_parameters_as_string( details ):
    arguments = get_arguments_as_list( details )
    if len(arguments) == 0:
        return ""
    return   (", ".join(arguments))

def get_arguments_as_string( details, defaultNone = False):
    arguments = get_arguments_as_list( details )
    if len(arguments) == 0:
        return ""
    if defaultNone == True:
        return ", " + ("=None, ".join(arguments)) + "=None";
    return   ", " + (", ".join(arguments))
    
def get_arguments_as_list_without_last( details ):
    arguments = []
    for _route in details['routes_details_dict']:
        if 'argument' in _route:
            arguments.append(_route['argument'])
    if len(arguments) != 0:
        del arguments[-1]
    return arguments

def get_arguments_as_string_without_last( details, defaultNone = False):
    arguments = get_arguments_as_list_without_last( details )
    if len(arguments) == 0:
        return ""
    if defaultNone == True:
        return ", " + ("=None, ".join(arguments)) + "=None";
    return   ", " + (", ".join(arguments))

def get_last_argument_as_string( details ):
    argument = None
    for _route in details['routes_details_dict']:
        if 'argument' in _route:
            argument = _route['argument']
    if argument == None:
        return ""
    return argument

def get_last_primary_key( details ):
    primary_key = None
    for _route in details['routes_details_dict']:
        if 'primary_key' in _route:
            primary_key = _route['primary_key']
    if primary_key == None:
        return ""
    return primary_key

def get_url_details_to_routes( details ):
    routes = []
    for _route in details['routes_details_dict']:
        if 'type' in _route:
            if _route['type'] == 'plain':
                routes.append( _route['text'] )
            if _route['type'] == 'entity':
                if _route['primary_key'] == 'uuid':
                    routes.append( "(?P<" + _route['argument'] + ">[0-9a-f-]+)" )
                elif _route['primary_key'] == 'id':
                    routes.append( "(?P<" + _route['argument'] + ">\d)" )
                else:
                    routes.append( "(?P<" + _route['argument'] + ">.*)" )
            if _route['type'] == 'argument':
                    routes.append( "(?P<" + _route['argument'] + ">.*)" )
    return routes

def get_urls_raw_url_for_create_list( details ):
    routes = get_url_details_to_routes( details )
    del routes[-1]
    return "/".join(routes)

def get_urls_raw_url_for_view_update_delete_view( details ):
    routes = get_url_details_to_routes( details )
    return "/".join(routes)

def get_urls(details):
    app_name = details['app_name']
    file_name = details['file_name']
    class_name = details['class_name']
    entity = get_last_entity_name(details)
    raw_url1 = get_urls_raw_url_for_create_list(details)
    raw_url2 = get_urls_raw_url_for_view_update_delete_view(details)
    _return = (
        "", "",
        "from .views." + file_name + " import " +  class_name+"CreateList, "+  class_name+"RetriveUpdateDelete",
        "",
        "urlpatterns.append(url(r'^"+raw_url1+"$', "+ class_name+"CreateList.as_view()))",
        "urlpatterns.append(url(r'^"+raw_url2+"$', "+ class_name+"RetriveUpdateDelete.as_view()))",
    )
    
    return ("\n".join(_return))


"""
def get_filters_as_string(arguments):
    _return = ()
    for argument in arguments:
        _return = _return + ("\t\t#if '" + argument + "' in self.request.query_set:",)
        _return = _return + ("\t\t\t#q &= Q(" + argument + "=self.request.query_set['" + argument + "'])",)
    
    return "\n".join(str(i) for i in _return)   
"""

def get_create_list(details):

    file_path = "./devapp/management/commands/templates/view_create_list.html.py"
    
    template = render(file_path, {
        'app_name': details['app_name'],
        'file_name': details['file_name'],
        'class_name': details['class_name'],
        'entity': get_last_entity_name( details ),
        'serializer': get_last_serializer_name( details ),
        'raw_url': get_urls_raw_url_for_create_list( details ),
        'arguments_as_list_without_last': get_arguments_as_list_without_last( details ),
        'arguments_as_string_without_last': get_arguments_as_string_without_last( details ),
        'arguments_as_string_without_last_with_default_none_value': get_arguments_as_string_without_last( details, True ),
    })

    return template


def get_update_delete_view(details):
    file_path = "./devapp/management/commands/templates/view_update_delete.html.py"
    
    template = render(file_path, {
        'app_name': details['app_name'],
        'file_name': details['file_name'],
        'class_name': details['class_name'],
        'entity': get_last_entity_name( details ),
        'serializer': get_last_serializer_name( details ),
        'last_argument': get_last_argument_as_string( details ),
        'last_primary_key': get_last_primary_key( details ),
        'raw_url': get_urls_raw_url_for_view_update_delete_view( details ),
        'arguments_as_list': get_arguments_as_list( details ),
        'arguments_as_list_without_last': get_arguments_as_list_without_last( details ),
        'arguments_as_string': get_arguments_as_string( details ),
        'arguments_as_string_with_default_none_value': get_arguments_as_string( details, True),
        'arguments_as_string_without_last': get_arguments_as_string_without_last( details ),
        'arguments_as_string_without_last_with_default_none_value': get_arguments_as_string_without_last( details, True ),
        'parameters_as_string': get_parameters_as_string( details ),
    })

    return template

def get_urls_general_imports():
    file_path = "./devapp/management/commands/templates/urls_imports.html.py"
    
    template = render(file_path, {})

    return template

def mergeAsText(*args, **options):
    return ("\n".join(args))

def render(file_path, context_data):
    if not os.path.exists(file_path):
        print (' Sorry: Template file not exist.')
    else:
        with open(file_path, 'r') as myfile:
            data = myfile.read()
            t = Template(data)

            c = Context(context_data, autoescape=False)
            return t.render(c)