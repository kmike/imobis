# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import re
import binascii
from .compat import urlopen, urlencode

GATE_URL = 'http://gate.sms-manager.ru/_getsmsd.php'
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


def sms_send(user, password, sender, phone, message, message_id=None, timeout=10, gate_url=GATE_URL):
    """
    Sends SMS. Returns internal_id.
    """
    data = {
        'user': user,
        'password': password,
        'sender': sender,
        'GSM': normalize_phone(phone),
        'binary': encode_to_binary(message)
    }
    if message_id:
        data['messageId'] = message_id

    query = urlencode(data)
    url = gate_url+'?'+query
    result = int(urlopen(url.encode('utf8'), timeout=timeout).read())

    if result < 0:
        raise ImobisError(result)

    return int(result)


