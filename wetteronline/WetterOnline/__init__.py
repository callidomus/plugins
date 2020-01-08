import logging
import urllib.parse
import requests

from lxml import html

class WetterOnline:
    def __init__(self, location):
        self.logger = logging.getLogger(__name__)
        self.api = 'http://api.wetteronline.de'
        self.location = None
        self.weather = None
        self.url = self.get_url(location)

    def get_url(self, location):
        try:
            url = '{}/search?name={}'.format(self.api, urllib.parse.quote(location))
            rq = self._fetch_data(url, headers={'content-type': 'application/json'})
            res = rq.json()
        except Exception:
            self.logger.exception('Failed searching location %s', location)
        
        for x in res:
            if 'match' in x and x['match'] == 'yes':
                self.location = res[0]

        if not self.location:
            raise Exception("Location not found!")

        return '{}/wetterwidget?gid={}&modeid={}&locationname={}'.format(self.api, self.location['geoID'], 'FC3', self.location['locationName'])

    def get(self):
        try:
            rq = self._fetch_data(self.url)
            tree = html.fromstring(rq.content)
            weather = self._parse_tree(tree)
        except Exception:
            self.logger.exception('Failed getting weather')

        return {
            'location': self.location,
            'weather': weather
        }

    def _fetch_data(self, url, headers=None):
        try:
            self.logger.debug('Fetching: %s', url)
            rq = requests.get(url, headers=headers, verify=False)
        except Exception:
            self.logger.exception('Failed fetching data')
            return
        return rq

    def _parse_tree(self, tree):
        weather = []
        try:
            for day in tree.xpath('//div[@class="forecast_day"]'):
                w = {
                    'day': day.xpath('.//div[1]/text()')[0],
                    'date': day.xpath('.//div[2]/text()')[0],
                    'temp_max': float(day.xpath('.//div[4]/text()')[0].replace('°', '')),
                    'temp_min': float(day.xpath('.//div[5]/text()')[0].replace('°', '')),
                    'sunhours': float(day.xpath('.//div[8]/text()')[0].replace('h', '')),
                    'rain_probability': float(day.xpath('.//div[9]/text()')[0].replace('%', '')),
                    'img': day.xpath('.//div[@class="weathersymbol"]/img/@src')[0],
                    'title': day.xpath('.//div[@class="weathersymbol"]/img/@title')[0],
                }

                if w['day'] == 'heute':
                    w['temp_now'] = float(tree.xpath('//div[@id="temperature"]/text()')[0].replace('°', ''))

                weather.append(w)
        except Exception:
            self.logger.exception('Failed parsing data')
            return
        return weather
