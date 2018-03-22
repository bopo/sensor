#!/usr/bin/env python
# coding:utf-8
# weilib/plugin/who_the_spy.py - 'Who is the spy' plugin for weilib
# ver 0.1 by winkidney 2014.05.10
import re

from django.core.cache import cache

try:
    import pickle as pickle
except ImportError:
    import pickle


class WeiSession(object):
    """ Helper Class to store info by session ID(Default: OpenID),
        Because of its usage of pickle, some type of data can't be stored correctly.
    """

    def __init__(self, session_id):
        if not isinstance(session_id, (str, int)):
            raise TypeError("Argument openid [%s] must be a str/unicode/int object!")

        self.session_id = session_id
        self._get_session()

    def _get_session(self):
        session = cache.get(self.session_id)

        if not session:
            self.session = {}
        else:
            self.session = pickle.loads(session)

    def _save(self):
        session_storage = pickle.dumps(self.session)
        cache.set(self.session_id, session_storage, 6000)

    def set_key(self, key, value):
        self.session[key] = value
        self._save()

    def get_key(self, key):
        return self.session.get(key)


def processor(recv_msg):
    """A processor must return a dict.
       If not ,program will throw the returned result.
    """
    session = None

    if '谁是卧底' in recv_msg.content:
        if re.search('/d'):
            session = WeiSession()

    if session.get_key('created') == 'yes':
        return session.get_key('')

    # recv_msg.content
    return {'test_plugin': 'only_the test plugin output'}
