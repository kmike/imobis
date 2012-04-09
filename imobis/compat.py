# -*- coding: utf-8 -*-
from __future__ import absolute_import

try:
    from urllib.request import urlopen
    import urllib.parse as urlparse
    from urllib.parse import urlencode
except ImportError:
    import urlparse
    from urllib2 import urlopen
    from urllib import urlencode
