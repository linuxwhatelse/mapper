from context import mapper

import unittest

class TestBuildUrl(unittest.TestCase):

    def test_path_append(self):
        url_static  = 'http://some.url/with/some/path/'
        url_dynamic = mapper.build_url(url='http://some.url/with/', paths=['some', 'path'])

        self.assertEqual(url_static , url_dynamic)

    def test_path_r(self):
        url_static  = 'http://some.url/with/some/path/'
        url_dynamic = mapper.build_url(url='http://some.url/other/path/', paths=['with', 'some', 'path'], r_path=True)

        self.assertEqual(url_static , url_dynamic)

    def test_query_append(self):
        url_static  = 'http://some.url?param1=abc'
        url_dynamic = mapper.build_url(url='http://some.url', queries={'param1':'abc'})

        self.assertEqual(url_static , url_dynamic)

    def test_query_r(self):
        url_static  = 'http://some.url?param1=abc'
        url_dynamic = mapper.build_url(url='http://some.url', queries={'param1':'abc'}, r_query=True)

        self.assertEqual(url_static , url_dynamic)

if __name__ == '__main__':
    unittest.main()
