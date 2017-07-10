from context import mapper

import unittest
import threading

mpr = mapper.Mapper()


class TestMapper(unittest.TestCase):

    def test_instances(self):
        inst1 = mapper.Mapper.get('inst1')
        inst2 = mapper.Mapper.get('inst2')
        self.assertNotEqual(inst1, inst2)

        inst1_2 = mapper.Mapper.get('inst1')
        inst2_2 = mapper.Mapper.get('inst2')
        self.assertNotEqual(inst1_2, inst2_2)

        self.assertEqual(inst1, inst1_2)
        self.assertEqual(inst2, inst2_2)

        def _async():
            inst1_3 = mapper.Mapper.get('inst1')
            inst2_3 = mapper.Mapper.get('inst2')
            self.assertNotEqual(inst1_3, inst2_3)

            self.assertEqual(inst1, inst1_2, inst1_3)
            self.assertEqual(inst2, inst2_2, inst2_3)

        threading.Thread(target=_async).start()

    def test_decorator_simple(self):
        @mpr.s_url('/index/')
        def _index():
            return True

        self.assertTrue(mpr.call('http://some.url/index'))

        mpr.clear()

    def test_decorator_query(self):
        @mpr.url('^/index/$')
        def _index(param1, param2):
            return '%s %s' % (param1, param2)

        self.assertEqual('123 456', mpr.call('http://some.url/index'
                                             '?param1=123&param2=456'))

        mpr.clear()

    def test_decorator_typecast(self):
        @mpr.url('^/index/$', type_cast={'a_int': int, 'a_float': float,
                                         'a_bool': bool})
        def _index(a_int, a_float, a_bool):
            if (isinstance(a_int, int) and
                    isinstance(a_float, float) and
                    isinstance(a_bool, bool)):
                return True

            else:
                return False

        self.assertTrue(mpr.call('http://some.url/index'
                                 '?a_int=123&a_float=1.0&a_bool=true'))

        mpr.clear()

    def test_decorator_dynamic_url(self):
        @mpr.url('^/index/(?P<some_path>[^/]*)/(?P<some_id>[0-9]*)/$',
                 type_cast={'some_id': int})
        def _index(some_path, some_id):
            return (some_path, some_id)

        self.assertEqual(('abc', 123),
                         mpr.call('http://some.url/index/abc/123/'))

        # Will not match because the regex expects :some_id: to be [0-9]*
        self.assertIsNone(None, mpr.call('http://some.url/index/abc/def/'))

        mpr.clear()

    def test_decorater_dynamic_simple_url(self):
        @mpr.s_url('/index/<some_id>/', type_cast={'some_id': int})
        def _index(some_id):
            return ('main', some_id)

        @mpr.s_url('/index/<some_id>/sub/', type_cast={'some_id': int})
        def _index(some_id):
            return ('sub', some_id)

        self.assertEqual(('main', 123),
                         mpr.call('http://some.url/index/123/'))

        self.assertEqual(('sub', 456),
                         mpr.call('http://some.url/index/456/sub'))

        mpr.clear()

    def test_decorator_method(self):
        @mpr.url('^/index/$', 'GET')
        def _index():
            return 'GET'

        @mpr.url('^/index/$', 'POST')
        def _index():
            return 'POST'

        self.assertEqual('GET',  mpr.call('http://some.url/index/',
                         method='GET'))
        self.assertEqual('POST', mpr.call('http://some.url/index/',
                         method='POST'))

        mpr.clear()

    def test_decorator_arguments(self):
        @mpr.url('^/index/$')
        def _index(param1, param2):
            return '%s %s' % (param1, param2)

        self.assertEqual('123 456', mpr.call('http://some.url/index/',
                         args={'param1': '123', 'param2': '456'}))

        mpr.clear()

    def test_decorator_default_value(self):
        @mpr.s_url('/index/')
        def _index(param1, param2=456):
            return '%s %s' % (param1, param2)

        self.assertEqual('123 456', mpr.call('http://some.url/index/',
                         args={'param1': '123'}))

        mpr.clear()

    def test_decorator_default_value_overwrite(self):
        @mpr.s_url('/index/')
        def _index(param1, param2=456):
            return '%s %s' % (param1, param2)

        self.assertEqual('123 789', mpr.call('http://some.url/index/',
                         args={'param1': '123', 'param2': '789'}))

        mpr.clear()

    def test_decorator_kwargs(self):
        @mpr.url('^/index/$')
        def _index(**kwargs):
            return kwargs

        response = mpr.call('http://some.url/index?param1=123&param2=456')

        self.assertIn('param1', response)
        self.assertIn('param2', response)

        mpr.clear()

    def test_decorator_list(self):
        @mpr.url('^/index/$', type_cast={'param1': int})
        def _index(param1):
            if (not isinstance(param1, list) and
                    param1[0] == 123 and param1[1] == 456):
                return False

            else:
                return True

        self.assertTrue(
            mpr.call('http://some.url/index?param1=123&param1=456'))

        mpr.clear()

    def test_decorator_blank_value(self):
        @mpr.url('^/index/$')
        def _index(param1, param2):
            return '%s-%s' % (param1, param2)

        self.assertEqual('-',
                         mpr.call('http://some.url/index?param1=&param2='))

        mpr.clear()

    def test_add_function(self):
        # Uses the same logic as the decorator apart from adding it to the
        # internal store.
        # If this test-case works, everything else (type-cast etc.)
        # will work as well
        def _index():
            return True

        mpr.add('^/index/$', _index)

        self.assertTrue(mpr.call('http://some.url/index/'))

        mpr.clear()

    def test_simple_add_function(self):
        # Uses the same logic as the decorator apart from adding it to the
        # internal store.
        # If this test-case works, everything else (type-cast etc.)
        # will work as well
        def _index():
            return True

        mpr.add('/index/', _index)

        self.assertTrue(mpr.call('http://some.url/index/'))

        mpr.clear()

    def test_data_store(self):
        self.assertIsNotNone(mpr._data_store)

        mpr.clear()

        self.assertEqual([], mpr._data_store)


if __name__ == '__main__':
    unittest.main()
