##############################################################################
# Copyright 2017 KNX-User-Forum e.V.                https://knx-user-forum.de/
##############################################################################

import logging
import requests
import json

logger = logging.getLogger('')
logging.getLogger("requests").setLevel(logging.WARNING)

class SMA():

    def __init__(self, core, ip, username, password, cycle, **kwargs):
        self._cd = core
        self.url_login = 'http://{}/dyn/login.json'.format(ip)
        self.url_logout = 'http://{}/dyn/logout.json'.format(ip)
        self.url_values = 'http://{}/dyn/getValues.json'.format(ip)
        self.username = username
        self.password = password
        self._session = None
        self.items = {}
        core.scheduler.add('_sma_wr', self.update, cycle=int(cycle))

    def run(self):
        self._login()
        self.alive = True

    def stop(self):
        self._logout()
        self.alive = False

    def _fetch_json(self, url, payload, params=None):
        headers = {'content-type': 'application/json'}
        res = requests.post(url, data=json.dumps(payload), headers=headers, params=params, timeout=5)
        return res.json()

    def _fetch_value(self, value):
        payload = {'destDev': [], 'keys': [value]}
        params = {'sid': self._session}
        return self._fetch_json(self.url_values, payload, params)

    def _login(self):
        try:
            payload = {'right': self.username, 'pass': self.password}
            res = self._fetch_json(self.url_login, payload)
            self._session = res['result']['sid']
        except KeyError as e:
            self._session = None
            if str(res.get('err', '')) == '503':
                logger.warning("Max amount of sesions reached")
            else:
                logger.warning("Session ID expected ['result']['sid'], got %s", res)

    def _logout(self):
        if self._session is None:
            return
        self._fetch_json(self.url_logout, {}, params={'sid': self._session})
        self._session = None

    def parse_item(self, item):
        if 'sma_wr' in item.conf:
            keyword = item.conf['sma_wr']
            self.items[keyword] = item

    def update(self):
        for keyword, item in self.items.items():
            try:
                res = self._fetch_value(keyword)
                _, value = res['result'].popitem()
                _, value = value[keyword].popitem()
                item(value[0]['val'], caller='SMA')
            except (KeyError, TypeError) as e:
                logger.warning(e)
                pass
