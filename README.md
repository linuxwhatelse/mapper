mapper - Simple URL-Scheme resolver
===================================
**mapper** is a small side-project which I created while working on a [Kodi](https://kodi.tv/) add-on.

As it is very generic, you can use it for everything that's somewhat based on URL-Schemes (be it Kodi add-ons, for (RESTful) APIs, ...)

How it works? It's super simple.  
Check [The very basic](#the-very-basic) and go from there.

## Table of Contents
* [Requirements](#requirements)
* [Usage](#usage)
    * [Available functions and their arguments](#available-functions-and-their-arguments)
    * [Registering functions](#registering-functions)
        * [The very basic](#the-very-basic)
        * [URL with a query](#url-with-a-query)
        * [Query value type cast](#query-value-type-cast)
        * [Extracting values from a URLs path](#extracting-values-from-a-urls-path)
        * [Pythons kwargs](#pythons-kwargs)
        * [Using the "add" function instead of the decorator](#using-the-add-function-instead-of-the-decorator)

## Requirements
What you need:
* Python 3.4 and up

## Usage

### Available functions and their arguments
```
url(pattern, method=None, type_cast=None)
    Decorator for registering a path pattern.

    Args:
        pattern (str): Regex pattern to match a certain path
        method (Optional[str]): Usually used to define one of
            GET, POST, PUT, DELETE (However, you can use whatever you want)
            Defaults to None
        type_cast (Optional[dict]): Mapping between the param name and
            one of int, float, bool

add(pattern, function, method=None, type_cast=None)
    Function for registering a path pattern.

    Args:
        pattern (str): Regex pattern to match a certain path
        function (function): Function to associate with this path
        method (Optional[str]): Usually used to define one of
            GET, POST, PUT, DELETE (However, you can use whatever you want)
            Defaults to None
        type_cast (Optional[dict]): Mapping between the param name and
            one of int, float, bool

call(url, method=None, args=None)
    Calls the first function matching the urls pattern and method (if any)

    Args:
        url (str): Url where a matching function should be called
        method (Optional[str]): Method used while registering a function.
            Defaults to None
        args (Optional[dict]): Additional args in form of a dict
            which should be passed to the matching function

    Returns:
        Returns the functions return value, None if it didn't return anything.
        Also, it will return None if no matching function was called.

clear()
    Clears all data associated with the mappers data store

build_url(url, paths=None, queries=None, r_path=False, r_query=False)
    Build new urls by adding/overwriting path-fragments and/or queries

    Args:
        url (str): Existing url where new path-fragments and/or queries need to be appended
            or existing ones overwritten
        paths (Optional[list]): list of path-fragments to append to the url
        queries (Optional[dict]): dict which will be used as query for the url
        r_path (Optional[bool]): If the existing path of ``url``
            should be replaced with the ``paths``
        r_query (Optional[bool]): If the existing query of ``url``
            should be replaced with the new ``queries``
```

### Registering functions
#### The very basic
``` python
import mapper

# Note: A path will ALWAYS end with a "/" regardless
# if your URL contains a trailing "/" or not
@mapper.url('^/some/path/$')  # Regex pattern
def func():
    print('func called')

# What e.g. your webserver would do...
mapper.call('http://some.url/some/path')
```

#### URL with a query
``` python
import mapper

# Note: Adding a query does NOT change the fact that
# the path will end with a "/" for the regex pattern
@mapper.url('^/some/path/$')
def func(param1, param2='default'):
    print(param1, param2)

# We don't supply "param2" and "param3" which will result in "param2" being None and param3 being 'default'
mapper.call('http://some.url/some/path?param1=123')

# Following would cause a:
# TypeError: func() missing 1 required positional argument: 'param1'
mapper.call('http://some.url/some/path')
```

#### Query value type cast
``` python
import mapper

# By default all parameters will be of type "string".
# You can change the type by supplying a dict where the key matches your parameters name and the value is one of:
# int, float, bool
#
# Note for bool:
#  1. Casting is case-insensitive.
#  2. 1 and 0 can be casted as well
@mapper.url('^/some/path/$', type_cast={'a_int' : int, 'a_float' : float, 'a_bool' : bool})
def func(a_int, a_float, a_bool):
    print(a_int, a_float, a_bool)

mapper.call('http://some.url/some/path?a_int=123&a_float=1.0&a_bool=true')
```

#### Extracting values from a URLs path
``` python
import mapper

# In pure python regex fashion we define a named capture group within our pattern to
# match whatever we want.
@mapper.url('^/some/path/(?P<param1>.*)/(?P<param2>[0-9]*)/$', type_cast={'param2':int})
def func(param1, param2):
    print(param1, param2)

mapper.call('http://some.url/some/path/abc/456/')
```

#### Pythons kwargs
``` python
import mapper

# It's pretty simple and type-casting works as well
@mapper.url('^/some/path/$', type_cast={'param1' : int, 'param2' : float, 'param3' : bool})
def func(param1, **kwargs):
    print(param1, kwargs)

mapper.call('http://some.url/some/path?param1=123&param2=1.0&param3=true')
```

#### Using the "add" function instead of the decorator
Sometimes you might have to register a function with the mapper at a later point. This can easily be achieved by using the mappers "add" function.
``` python
import mapper

def func(param1, param2):
    print(param1, param2)

# It works the same way as the decorator.
# The only difference is, that we to specify the function ourselves.
mapper.add('^/some/path/(?P<param1>[0-9]*)/$', func, type_cast={'param1' : int, 'param2' : int})

mapper.call('http://some.url/some/path/123?param2=456')
```
