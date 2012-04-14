# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import re
import binascii
from xml.etree import ElementTree
from .compat import urlopen, urlencode

REMOVE_RE = re.compile(r'[\s\(\)\-]', re.U)

class ImobisError(Exception):
    ERRORS = {
        -1: 'Ошибка отправки',
        -2: 'Не достаточно средств на балансе для отправки сообщения',
        -3: 'Неизвестный номер',
        -4: 'Внутренняя ошибка',
        -5: 'Неверный логин или пароль',
        -6: 'Отсутствует номер получателя',
        -7: 'Отсутствует текст сообщения',
        -8: 'Отсутствует имя отправителя',
        -9: 'Неверный формат номера получателя',
        -10: 'Отсутствует логин',
        -11: 'Отсутствует пароль',
        -12: 'Неверный формат внешнего (external) Id',
    }

    def __init__(self, code):
        self._code = code

    def __str__(self):
         return "ImobisError %s" % self._code

    def message(self):
        return self.ERRORS.get(self._code, 'unknown error %s' % self._code)


def encode_to_binary(text):
    return binascii.hexlify(text.encode('UTF-16BE'))

def normalize_phone(phone):
    phone = re.sub(REMOVE_RE, '', phone).replace('+7', '7')
    if phone.startswith('8'):
        phone = '7'+phone[1:]
    return phone


class Imobis(object):
    GATE_URL = 'http://gate.sms-manager.ru/_getsmsd.php'
    BALANCE_URL = 'http://gate.sms-manager.ru/_balance.php'
    CHECK_URL = 'http://gate.sms-manager.ru/_checkgsm.php'

    def __init__(self, user, password, timeout=10):
        self.user = user
        self.password = password
        self.timeout = timeout

    def send_sms(self, sender, phone, message, message_id=None):
        """
        Sends SMS. Returns internal_id.
        """
        data = {
            'sender': sender,
            'GSM': normalize_phone(phone),
            'binary': encode_to_binary(message)
        }
        if message_id is not None:
            data['messageId'] = message_id

        result = int(self._http_get(self.GATE_URL, data))

        if result < 0:
            raise ImobisError(result)

        return result

    def get_balance(self):
        """
        Returns current balance.
        """
        return self._http_get(self.BALANCE_URL, {}).decode('utf8')

    def is_valid_phone(self, phone):
        """
        Checks if phone is valid and returns True or False.
        """
        res = self._http_get(self.CHECK_URL, {
            'GSM': normalize_phone(phone),
            'mode': 'brief',
        }).decode('utf8')

        if res == 'OK':
            return True
        if res == 'noBindingDetected':
            return False

        try:
            code = int(res)
            raise ImobisError(code)
        except ValueError:
            raise ImobisError(res)

# TODO:
#    def get_phone_info(self, phone):
#        """
#        Returns phone info: dict(
#            region='Санкт-Петербург',
#            operator='ОАО "Мобильные Телесистемы"',
#            issuedate='2001-10-18'
#        )
#
#        or None if phone is invalid.
#        """
#
#        res = self._http_get(self.CHECK_URL, {
#            'GSM': normalize_phone(phone),
#            'mode': 'full',
#        }).decode('utf8')
#
#        xml = ElementTree.fromstring(res)
#        return xml


    def _http_get(self, url, data):
        _data = {'user': self.user, 'password': self.password}
        _data.update(data)
        url = url + '?' + urlencode(_data)
        return urlopen(url.encode('utf8'), timeout=self.timeout).read()
