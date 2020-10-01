import lib.plugin
import re
from pprint import pformat
from wetteronline.WetterOnline import WetterOnline

icons = {
  'so': 'sun',
  'mo': 'moon',
  'ns': 'weather.fog',
  'nm': 'weather.fog',
  'nb': 'weather.fog',
  'wb': 'weather.partlysunny',
  'mb': 'weather.partlysunny_n',
  'bd': 'weather.cloudy',
  'wbs1': 'weather.partlysunny',
  'mbs1': 'weather.partlysunny_n',
  'bdr1': 'weather.rain1',
  'wbr1': 'weather.rain2_shower',
  'wbr2': 'weather.rain2_shower',
  'wbs2': 'weather.rain2_shower',
  'mbs2': 'weather.rain2',
  'bdr2': 'weather.rain2',
  'bdr3': 'weather.rain3',
  'wbr3': 'weather.rain3_shower',
  'wbsrs1': 'weather.snowrain2_shower',
  'mbsrs1': 'weather.snowrain1',
  'bdsr1': 'weather.snowrain1',
  'wbsrs2': 'weather.snowrain3_shower',
  'mbsrs2': 'weather.snowrain2',
  'bdsr2': 'weather.snowrain2',
  'bdsr3': 'weather.snowrain3',
  'wbsns1': 'weather.snow2_shower',
  'mbsns1': 'weather.snow1',
  'bdsn1': 'weather.snow1',
  'wbsns2': 'weather.snow3_shower',
  'mbsns2': 'weather.snow2',
  'bdsn2': 'weather.snow2',
  'bdsn3': 'weather.snow3',
  'wbsg': 'weather.storm1',
  'mbsg': 'weather.storm1',
  'bdsg': 'weather.storm1',
  'wbg1': 'weather.storm1',
  'mbg1': 'weather.storm1',
  'bdg1': 'weather.storm1',
  'wbg2': 'weather.storm2',
  'mbg2': 'weather.storm2',
  'bdg2': 'weather.storm2',
  'bdgr1': 'weather.graupel2',
  'bdgr2': 'weather.graupel3',
}

class WetterOnlinePlugin(lib.plugin.Plugin):
  def __init__(self, core, conf):
    lib.plugin.Plugin.__init__(self, core, conf)
    self.location = '{}'.format(conf.get('location'))
    self.items = {}
    core.scheduler.add('_wetteronline', self.update, cycle=int(conf.get('cycle', 900)))

  def start(self):
    self.wol = WetterOnline(self.location)
    self.alive = True

  def stop(self):
    self.alive = False

  def pre_stage(self):
    for node in self._core.config.query_nodes('wetteronline'):
      keyword = node.attr['wetteronline']
      self.items[keyword] = node

  def update(self, value=None, trigger=None):
    try:
      wol_data = self.wol.get()
      self.logger.info("Successfully fetched WetterOnline data")
    except Exception:
      self.logger.exception('Failed getting WetterOnline data')
      return

    # Map native icons
    for wd in wol_data['weather']:
      img = re.search(r"/([^/_]+)_+\.svg$", wd['img']).group(1)
      if img in icons:
        wd['img'] = icons[img]
      else:
        wd['img'] = 'question'
      
    
    for keyword, item in self.items.items():
      try:
        (wol_idx, wol_key) = keyword.split('__')
        value = wol_data['weather'][int(wol_idx)][wol_key]
        item(value, trigger=self.get_trigger())
      except:
        self.logger.exception('Unable to update item %s with value %s' % (item, value))

