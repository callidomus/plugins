import logging
import urllib.parse
import re
import requests

from lxml import html

class WetterOnline:
    def __init__(self, location):
        self.logger = logging.getLogger(__name__)
        self.location = None
        self.weather = None
        self.url = self.get_url(location)

    def get_url(self, location):
        try:
            url = 'http://api.wetteronline.de/search?name={}'.format(urllib.parse.quote(location.lower()))
            rq = self._fetch_data(url, headers={'content-type': 'application/json'})
            res = rq.json()
        except Exception:
            self.logger.exception('Failed searching location %s', location)

        for x in res:
            if 'match' in x and x['match'] == 'yes':
                self.location = res[0]['geoName']

        if not self.location:
            raise Exception("Location not found!")

        return 'http://www.wetteronline.de/{}/'.format(self.location)

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
           for day in range(1, 4):
               daystr = tree.xpath(f'//table[@id="daterow"]/tbody/tr/th[{day}]/text()')[-1].strip()
               # Workaround 'today' becoming 'tomorrow' too early on the site
               if day == 1 and daystr.lower() != 'heute':
                   continue
                w = {
                    'day': daystr,
                    'date': re.search(r"(\d+\.\d+\.)", tree.xpath(f'//table[@id="daterow"]/tbody/tr/th[{day}]/span/text()')[-1].strip()).group(0),
                    'temp_max': float(tree.xpath(f'//table[@id="weather"]/tbody/tr[@class="Maximum Temperature"]/td[{day}]/div/span[2]/text()')[-1].replace('°', '')),
                    'temp_min': float(tree.xpath(f'//table[@id="weather"]/tbody/tr[@class="Minimum Temperature"]/td[{day}]/div/span[2]/text()')[-1].replace('°', '')),
                    'sunhours': float(re.search(r"(\d+)", tree.xpath(f'//tr[@id="sun_teaser"]/td[{day}]/span[1]/text()')[-1]).group(0)),
                    'rain_probability': float(re.search(r"(\d+)", tree.xpath(f'//tr[@id="precipitation_teaser"]/td[{day}]/span[1]/text()')[-1]).group(0)),
                    'src': tree.xpath(f'//tr[@id="wwdaysymbolrow"]/td[{day}]/img/@src')[-1],
                    'img': 'question',
                    'title': tree.xpath(f'//tr[@id="wwdaysymbolrow"]/td[{day}]/@data-tt-args')[-1].split(',')[2].replace('"', ''),
                }
                if day == 1:
                    w['temp_now'] = float(tree.xpath('//div[@id="nowcast-card-temperature"]/div[1]/text()')[-1])

                weather.append(w)
        except Exception:
            self.logger.exception('Failed parsing data')
            return
        return weather
