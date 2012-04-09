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

Only sms sending is implemented in imobis 0.1.

::

    >>> from imobis.api import sms_send
    >>> res = api.sms_send('login', 'password', 'Sender', '79991234567', u'привет', message_id=5234)
    12836

Development
-----------

Development happens at bitbucket and github:

* https://bitbucket.org/kmike/imobis/
* https://github.com/kmike/imobis/

The issue tracker is at bitbucket: https://bitbucket.org/kmike/imobis/issues/new