mapper - Simple URL-Scheme resolver
===================================
[![Build Status](https://travis-ci.org/linuxwhatelse/mapper.svg?branch=master)](https://travis-ci.org/linuxwhatelse/mapper)
[![pypi](https://img.shields.io/pypi/v/lwe-mapper.svg)](https://pypi.python.org/pypi/lwe-mapper)

**mapper** is a small side-project which I created while working on other *stuff* and was in the need for a super simple url-reslover.  
The idea was to keep the footprint as small as possible **without** relying on none-python modules.

What you use it for is up to you.  

If you f.e. need a simple JSON Server, check out [mjs](https://github.com/linuxwhatelse/mjs) as it follows the
same principle.  
Small footprint, easy to use, and only one dependency - mapper (obviously).

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
* Python 2.7 or up

## Installation
You have two options:

1. Install via pypi `pip install lwe-mapper`
2. Download [mapper.py](https://github.com/linuxwhatelse/mapper/blob/master/mapper.py) and place it into the root directory of your project

## Usage

### Registering functions

#### The very basic
``` python
import mapper

mpr = mapper.Mapper()

# Note: A path will ALWAYS end with a "/" regardless
# if your URL contains a trailing "/" or not

# Choose one of the two decorators
@mpr.url('^/some/path/$')  # Regex pattern
@mpr.s_url('/some/path/')  # Simple path
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
@mpr.s_url('/some/path/')
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
@mpr.s_url('/some/path/', type_cast={'a_int' : int, 'a_float' : float, 'a_bool' : bool})
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
# We can use a simplified url as well though.
# Not that type-casting works as well.
@mpr.url('^/some/path/(?P<param1>[^/]*)/(?P<param2>[0-9]*)/$', type_cast={'param2':int}) # Regex pattern
@mpr.s_url('/some/path/<param1>/<param2>/', type_cast={'param2':int})                    # Simple path
def func(param1, param2):
    print(param1, param2)

mpr.call('http://some.url/some/path/abc/456/')
```

#### Pythons kwargs
``` python
import mapper

mpr = mapper.Mapper()

# It's pretty simple and type-casting works as well
@mpr.s_url('/some/path/', type_cast={'param1' : int, 'param2' : float, 'param3' : bool})
def func(param1, **kwargs):
    print(param1, kwargs)

mpr.call('http://some.url/some/path?param1=123&param2=1.0&param3=true')
```

#### Return values
``` python
import mapper

mpr = mapper.Mapper()

# Whatever you return will be returned by mapper
@mpr.s_url('/some/path/')
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
# The only difference is, that we have to specify the function ourselves.
mpr.add('^/some/path/(?P<param1>[0-9]*)/$', func, type_cast={'param1' : int, 'param2' : int})
mpr.s_add('/some/path/<param1>/', func, type_cast={'param1' : int, 'param2' : int})

mpr.call('http://some.url/some/path/123?param2=456')
```
