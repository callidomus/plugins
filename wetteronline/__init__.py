import lib.plugin

from wetteronline.WetterOnline import WetterOnline

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
    
    for keyword, item in self.items.items():
      try:
        (wol_idx, wol_key) = keyword.split('__')
        value = wol_data['weather'][int(wol_idx)][wol_key]
        item(value, trigger=self.get_trigger())
      except:
        self.logger.exception('Unable to update item %s with value %s' % (item, value))

