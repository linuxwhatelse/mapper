from context import mapper

import unittest

mpr = mapper.Mapper()

class TestMapper(unittest.TestCase):

    def test_decorator_simple(self):
        @mpr.url('^/index1/$')
        def _index():
            return True

        self.assertTrue(mpr.call('http://some.url/index1'))

    def test_decorator_query(self):
        @mpr.url('^/index2/$')
        def _index2(param1, param2):
            return '%s %s' % (param1, param2)

        self.assertEqual('123 456', mpr.call('http://some.url/index2?param1=123&param2=456'))

    def test_decorator_typecast(self):
        @mpr.url('^/index3/$', type_cast={'a_int' : int, 'a_float' : float, 'a_bool' : bool})
        def _index3(a_int, a_float, a_bool):
            if (isinstance(a_int, int) and
                    isinstance(a_float, float) and
                    isinstance(a_bool, bool)):
                return True

            else:
                return False

        self.assertTrue(mpr.call('http://some.url/index3?a_int=123&a_float=1.0&a_bool=true'))

    def test_decorator_dynamic_url(self):
        @mpr.url('^/index4/(?P<some_path>.*)/(?P<some_id>[0-9]*)/$', type_cast={'some_id' : int})
        def _index4(some_path, some_id):
            return (some_path, some_id)

        self.assertEqual(('abc', 123), mpr.call('http://some.url/index4/abc/123/'))

        # Will not match because the regex expects :some_id: to be [0-9]*
        self.assertIsNone(None, mpr.call('http://some.url/index4/abc/def/'))

    def test_decorator_method(self):
        @mpr.url('^/index5/$', 'GET')
        def _index5():
            return 'GET'

        @mpr.url('^/index5/$', 'POST')
        def _index5():
            return 'POST'

        self.assertEqual('GET',  mpr.call('http://some.url/index5/', method='GET'))
        self.assertEqual('POST', mpr.call('http://some.url/index5/', method='POST'))

    def test_decorator_arguments(self):
        @mpr.url('^/index6/$')
        def _index6(param1, param2):
            return '%s %s' % (param1, param2)

        self.assertEqual('123 456', mpr.call('http://some.url/index6/', args={'param1': '123', 'param2': '456'}))

    def test_decorator_kwargs(self):
        @mpr.url('^/index7/$')
        def _index7(**kwargs):
            return kwargs

        response = mpr.call('http://some.url/index7?param1=123&param2=456')

        self.assertIn('param1', response)
        self.assertIn('param2', response)

    def test_decorator_list(self):
        @mpr.url('^/index8', type_cast={'param1' : int})
        def _index8(param1):
            if (not isinstance(param1, list) and
                    param1[0] == 123 and parm[1] == 456):
                return False

            else:
                return True


        self.assertTrue(mpr.call('http://some.url/index8?param1=123&param1=456'))

    def test_decorator_blank_value(self):
        @mpr.url('^/index9/$')
        def _index9(param1, param2):
            return '%s-%s' % (param1, param2)

        self.assertEqual('-', mpr.call('http://some.url/index9?param1=&param2='))

    def test_add_function(self):
        # Uses the same logic as the decorator apart from adding it to the
        # internal store.
        # If this test-case works, everything else (type-cast etc.)
        # will work as well
        def _index10():
            return True

        mpr.add('^/index10/$', _index10)

        self.assertTrue(mpr.call('http://some.url/index10/'))

    def test_data_store(self):
        self.assertIsNotNone(mpr._data_store)

        mpr.clear()

        self.assertEqual([], mpr._data_store)


if __name__ == '__main__':
    unittest.main()
