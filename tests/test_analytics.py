import unittest
import sys
import os
currentdir = os.getcwd()

sys.path.append('{}/..'.format(currentdir))
from log_analyse import extract_entity, get_stats
class AnalyticsTest(unittest.TestCase):

    def test_extract_entity(self):
        pattern = '(?<=\s/\w{8}/\w{8}/)\w{8}'
        str = '10.10.6.90 - - 15/Aug/2016:23:59:20 -0500 "GET /ecf8427e/b443dc7f/71f28176/174ef735/1dd4d421 HTTP/1.0" 200 - "-" "-" 7 "10.10.1.231, 10.10.6.90" -'
        user = extract_entity(str, pattern)
        self.assertEqual(user,'71f28176')
    
    def test_stats(self):
        stats = get_stats('../tests/testdata/*')
        self.assertIsNotNone(stats)
        self.assertEqual(stats['71f28176'].total_pages, 3)


if __name__ == '__main__':
    tester = AnalyticsTest()
    tester.test_extract_entity()
    tester.test_stats()
    print('All tests passed')