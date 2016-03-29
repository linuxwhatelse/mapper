mapper - Simple URL-Scheme resolver
===================================
[![Build Status](https://travis-ci.org/linuxwhatelse/mapper.svg?branch=master)](https://travis-ci.org/linuxwhatelse/mapper)

**mapper** is a small side-project which I created while working on a [Kodi](https://kodi.tv/) add-on.

As it is very generic, you can use it for everything that's somewhat based on URL-Schemes (be it Kodi add-ons, for (RESTful) APIs, ...)

How it works? It's super simple.  
Check [The very basic](#the-very-basic) and go from there.

## Table of Contents
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
    * [Registering functions](#registering-functions)
        * [The very basic](#the-very-basic)
        * [URL with a query](#url-with-a-query)
        * [Query value type cast](#query-value-type-cast)
        * [Extracting values from a URLs path](#extracting-values-from-a-urls-path)
        * [Pythons kwargs](#pythons-kwargs)
        * [Return values](#return-values)
        * [Using the "add" function instead of the decorator](#using-the-add-function-instead-of-the-decorator)

## Requirements
What you need:
* Python 3.4 and up

## Installation
As this is a single file module without any dependencies other than the default
python libraries, you have two choices:

1. Download [mapper.py](https://raw.githubusercontent.com/linuxwhatelse/mapper/master/mapper.py) and place it into the root directory of your project
2. Install it via setup.py
 * `git clone https://github.com/linuxwhatelse/mapper`
 * `cd mapper`
 * `python3 setup.py install`

## Usage

### Registering functions

#### The very basic
``` python
import mapper

mpr = mapper.Mapper()

# Note: A path will ALWAYS end with a "/" regardless
# if your URL contains a trailing "/" or not
@mpr.url('^/some/path/$')  # Regex pattern
def func():
    print('func called')

# What e.g. your webserver would do...
mpr.call('http://some.url/some/path')
```

#### URL with a query
``` python
import mapper

mpr = mapper.Mapper()

# Note: Adding a query does NOT change the fact that
# the path will end with a "/" for the regex pattern
@mpr.url('^/some/path/$')
def func(param1, param2='default'):
    print(param1, param2)

# We don't supply "param2" and "param3" which will result in "param2" being None and param3 being 'default'
mpr.call('http://some.url/some/path?param1=123')

# Following would cause a:
# TypeError: func() missing 1 required positional argument: 'param1'
mpr.call('http://some.url/some/path')
```

#### Query value type cast
``` python
import mapper

mpr = mapper.Mapper()

# By default all parameters will be of type "string".
# You can change the type by supplying a dict where the key matches your parameters name and the value is one of:
# int, float, bool
#
# Note for bool:
#  1. Casting is case-insensitive.
#  2. 1 and 0 can be casted as well
@mpr.url('^/some/path/$', type_cast={'a_int' : int, 'a_float' : float, 'a_bool' : bool})
def func(a_int, a_float, a_bool):
    print(a_int, a_float, a_bool)

mpr.call('http://some.url/some/path?a_int=123&a_float=1.0&a_bool=true')
```

#### Extracting values from a URLs path
``` python
import mapper

mpr = mapper.Mapper()

# In pure python regex fashion we define a named capture group within our pattern to
# match whatever we want.
@mpr.url('^/some/path/(?P<param1>.*)/(?P<param2>[0-9]*)/$', type_cast={'param2':int})
def func(param1, param2):
    print(param1, param2)

mpr.call('http://some.url/some/path/abc/456/')
```

#### Pythons kwargs
``` python
import mapper

mpr = mapper.Mapper()

# It's pretty simple and type-casting works as well
@mpr.url('^/some/path/$', type_cast={'param1' : int, 'param2' : float, 'param3' : bool})
def func(param1, **kwargs):
    print(param1, kwargs)

mpr.call('http://some.url/some/path?param1=123&param2=1.0&param3=true')
```

#### Return values
``` python
import mapper

mpr = mapper.Mapper()

# Whatever you return will be returned by mapper
@mpr.url('^/some/path/$')
def func():
    return ('str', 1, 1.0, True)

a_str, a_int, a_float, a_bool = mpr.call('http://some.url/some/path')
```

#### Using the "add" function instead of the decorator
Sometimes you might have to register a function with the mapper at a later point. This can easily be achieved by using the mappers "add" function.
``` python
import mapper

mpr = mapper.Mapper()

def func(param1, param2):
    print(param1, param2)

# It works the same way as the decorator.
# The only difference is, that we to specify the function ourselves.
mpr.add('^/some/path/(?P<param1>[0-9]*)/$', func, type_cast={'param1' : int, 'param2' : int})

mpr.call('http://some.url/some/path/123?param2=456')
```
