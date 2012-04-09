# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest
import mock
from . import api
from .compat import urlparse

class ApiTest(unittest.TestCase):
    def assertUrlQueryEqual(self, url1, url2):
        data1 = urlparse.urlsplit(url1)
        data2 = urlparse.urlsplit(url2)
        q1 = urlparse.parse_qs(data1.query)
        q2 = urlparse.parse_qs(data2.query)
        self.assertEqual(q1, q2)

    def test_binary_encode(self):
        self.assertEqual(api.encode_to_binary('привет'), b'043f04400438043204350442')

    def test_phone_normalize(self):
        self.assertEqual(api.normalize_phone('79991234567'), '79991234567')
        self.assertEqual(api.normalize_phone('+7 (999) 1234567'), '79991234567')
        self.assertEqual(api.normalize_phone('8(999)1234-567'), '79991234567')
        self.assertEqual(api.normalize_phone('89991234567'), '79991234567')

    @mock.patch('imobis.api.urlopen')
    def test_send_sms(self, urlopen):
        urlopen.return_value.read.return_value = b'124'

        url = b'http://gate.sms-manager.ru/_getsmsd.php?user=login&password=password&sender=Pan%20Gurman&binary=043f04400438043204350442&GSM=79991234567&messageId=5'
        res = api.sms_send('login', 'password', 'Pan Gurman', '8 (999) 1234-567', 'привет', 5)

        request_url = urlopen.call_args[0][0]
        self.assertUrlQueryEqual(request_url, url)

        self.assertEqual(res, 124)

    @mock.patch('imobis.api.urlopen')
    def test_sms_send_str(self, urlopen):
        urlopen.return_value.read.return_value = b'124'
        url = b'http://gate.sms-manager.ru/_getsmsd.php?user=login&password=password&sender=Pan%20Gurman&binary=043f04400438043204350442&GSM=79991234567'
        res = api.sms_send(b'login', b'password', b'Pan Gurman', '8 (999) 1234-567', 'привет')

        request_url = urlopen.call_args[0][0]
        self.assertUrlQueryEqual(request_url, url)

        self.assertEqual(res, 124)
