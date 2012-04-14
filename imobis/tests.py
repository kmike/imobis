# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest
import mock
from . import api
from .compat import urlparse

class UtilsTest(unittest.TestCase):
    def test_binary_encode(self):
        self.assertEqual(api.encode_to_binary('привет'), b'043f04400438043204350442')

    def test_phone_normalize(self):
        self.assertEqual(api.normalize_phone('79991234567'), '79991234567')
        self.assertEqual(api.normalize_phone('+7 (999) 1234567'), '79991234567')
        self.assertEqual(api.normalize_phone('8(999)1234-567'), '79991234567')
        self.assertEqual(api.normalize_phone('89991234567'), '79991234567')


@mock.patch('imobis.api.urlopen')
class ApiTest(unittest.TestCase):

    def setUp(self):
        self.im = api.Imobis('login', 'password')

    def assertUrlQueryEqual(self, url1, url2):
        data1 = urlparse.urlsplit(url1)
        data2 = urlparse.urlsplit(url2)
        q1 = urlparse.parse_qs(data1.query)
        q2 = urlparse.parse_qs(data2.query)
        self.assertEqual(q1, q2)


    def test_send_sms(self, urlopen):
        urlopen.return_value.read.return_value = b'124'
        url = b'http://gate.sms-manager.ru/_getsmsd.php?user=login&password=password&sender=Pan%20Gurman&binary=043f04400438043204350442&GSM=79991234567&messageId=5'

        res = self.im.send_sms('Pan Gurman', '8 (999) 1234-567', 'привет', 5)

        request_url = urlopen.call_args[0][0]
        self.assertUrlQueryEqual(request_url, url)

        self.assertEqual(res, 124)

    def test_sms_send_str(self, urlopen):
        urlopen.return_value.read.return_value = b'124'
        url = b'http://gate.sms-manager.ru/_getsmsd.php?user=login&password=password&sender=Pan%20Gurman&binary=043f04400438043204350442&GSM=79991234567'

        im = api.Imobis(b'login', b'password')
        res = im.send_sms(b'Pan Gurman', '8 (999) 1234-567', 'привет')

        request_url = urlopen.call_args[0][0]
        self.assertUrlQueryEqual(request_url, url)

        self.assertEqual(res, 124)

    def test_errors(self, urlopen):
        urlopen.return_value.read.return_value = b'-1'

        raised = False
        try:
            self.im.send_sms('Pan Gurman', '8 (999) 1234-567', 'привет')
        except api.ImobisError as e:
            self.assertEqual(e._code, -1)
            self.assertEqual(e.message(), 'Ошибка отправки')
            raised = True
        self.assertTrue(raised)

    def test_balance(self, urlopen):
        urlopen.return_value.read.return_value = b'100'
        self.assertEqual(self.im.get_balance(), 100.0)

    def test_is_valid_phone(self, urlopen):
        urlopen.return_value.read.return_value = b'OK'
        self.assertTrue(self.im.is_valid_phone('1234234234'))

    def test_is_valid_phone_error_format(self, urlopen):
        urlopen.return_value.read.return_value = b'-9'
        self.assertFalse(self.im.is_valid_phone('1234234234'))

    def test_is_valid_phone_error(self, urlopen):
        urlopen.return_value.read.return_value = b'-10'

        def fetch():
            return self.im.is_valid_phone('123423412')

        self.assertRaises(api.ImobisError, fetch)

