======
imobis
======

Python interface to http://sms-manager.ru/ (aka http://www.imobis.ru/ ).

Installation
============

::

    $ pip install imobis

Usage
=====

::

    >>> from imobis.api import Imobis
    >>> im = Imobis('login', 'password')

Send sms::

    >>> im.send_sms('Sender', '79991234567', u'привет', message_id=5234)
    12836

Get balance::

    >>> im.get_balance()
    100

Check if phone number is valid::

    >>> im.is_valid_phone('234234')
    False


Development
-----------

Development happens at bitbucket and github:

* https://bitbucket.org/kmike/imobis/
* https://github.com/kmike/imobis/

The issue tracker is at bitbucket: https://bitbucket.org/kmike/imobis/issues/new