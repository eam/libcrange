"""
  Library for querying the range webservice - http://github.com/ytoolshed/range
"""

import urllib2
import sys

class RangeException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Range(object):
    def __init__(self, host):
        self.host = host

    def expand(self, expr):
        url = 'http://%s/range/list?%s' % (self.host,
                                           urllib2.quote(expr))
        req = urllib2.urlopen(url)
        code = req.getcode()
        if code != 200:
            raise RangeException("Got %d response code from %s" %
                                 (code, url))
        reqinfo = req.info()
        exception = reqinfo.getheader('RangeException')
        if exception:
            raise RangeException(exception)
        expansion = []
        for line in req.readlines():
            expansion.append(line.rstrip())
        return expansion

if __name__ == '__main__':
    try:
        r = Range("localhost:80")
    except RangeException as e:
        print e
        sys.exit(1)
    print r.expand(sys.argv[1])
