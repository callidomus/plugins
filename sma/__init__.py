##############################################################################
# Copyright 2017 KNX-User-Forum e.V.                https://knx-user-forum.de/
# Version 1.1
##############################################################################

import logging
import requests
import json

logger = logging.getLogger('')
logging.getLogger("requests").setLevel(logging.WARNING)

class SMA():

    def __init__(self, core, ip, username, password, cycle, **kwargs):
        self._cd = core
        self._username = username
        self._password = password
        self._session = None
        self.url_login = 'http://{}/dyn/login.json'.format(ip)
        self.url_logout = 'http://{}/dyn/logout.json'.format(ip)
        self.url_values = 'http://{}/dyn/getValues.json'.format(ip)
        self.sma_objects = json.loads(open('/data/callidomus/local/plugins/sma/sma_objects.json').read())
        self.sma_strings = json.loads(open('/data/callidomus/local/plugins/sma/sma_strings_de.json').read())
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
            payload = {'right': self._username, 'pass': self._password}
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
                if res == {'err': 401}:
                    raise Warning('No valid session, starting new')
            except Warning as e:
                logger.warning(e)
                self._login()

            try:
                _, value = res['result'].popitem()
                _, value = value[keyword].popitem()

                # return value
                if self.sma_objects[keyword]['Typ'] == 0:
                    if value[0]['val'] == None:
                        value = 0
                    else:
                        value = value[0]['val'] * self.sma_objects[keyword]['Scale']

                # return strings
                if self.sma_objects[keyword]['Typ'] == 1:
                    value = self.sma_strings[str(value[0]['val'][0]['tag'])]

                item(value, caller='SMA')
            except:
                logger.warning('Unable to update item %s with value %s' % (item, value))
