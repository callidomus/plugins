################################################################################
#  Copyright 2017  Jürgen Heckmann                     heckmannju (at) gmail.com
################################################################################
#
#   EM300 plugin for Callidomus.                      https://www.callidomus.com
#
#   This plugin is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This Plugin is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
#   EM300 plugin für Callidomus.                      https://www.callidomus.com
#
#   Diese Plugin ist Freie Software: Sie können es unter den Bedingungen
#   der GNU General Public License, wie von der Free Software Foundation,
#   Version 3 der Lizenz oder (nach Ihrer Wahl) jeder späteren
#   veröffentlichten Version, weiterverbreiten und/oder modifizieren.
#
#   Dises Plugin wird in der Hoffnung, dass es nützlich sein wird, aber
#   OHNE JEDE GEWÄHRLEISTUNG, bereitgestellt; sogar ohne die implizite
#   Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
#   Siehe die GNU General Public License für weitere Details.
#
#   Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
#   Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.
#
################################################################################

import lib.plugin
import requests
import time

class EM300LR(lib.plugin.Plugin):

    def __init__(self, core, conf):
        lib.plugin.Plugin.__init__(self, core, conf)
        self.ip =  str(conf.get('host'))
        self.items = {}
        self.sessioncookie = None
        core.scheduler.add('EM300:'+self.id, self.update, cycle=int(conf.get('cycle', 300)))

    def start(self):
        self.alive = True

    def stop(self):
        self.alive = False

    def pre_stage(self):
        if self.instances > 1:
            for node in self._core.config.query_nodes('em300', children=self.path):
                self.parse_node(node)
            for node in self._core.config.query_nodes('em300', em300_node=self.path):
                self.parse_node(node)
        else:
            for node in self._core.config.query_nodes('em300'):
                self.parse_node(node)
                
    def parse_node(self, node):
        value = node.attr['em300']
        self.items[value] = node
    
    def update(self, value=None, trigger=None):
        #start = time.time()
        urlstart = 'http://{}/start.php'.format(self.ip)
        urldata =  'http://{}/mum-webservice/data.php'.format(self.ip)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        if self.sessioncookie == None:
            self.logger.debug("collectiong session cookie...")
            r = requests.get(urlstart, headers=headers)
            response =  r.json()
            serial = response['serial']
            authentication = response['authentication']

            if( authentication != True):
                self.logger.error("Support only EM300LRs without password")
                return
               
            PHPSESSID = r.cookies['PHPSESSID']
            self.sessioncookie = dict(PHPSESSID=PHPSESSID)
            self.logger.debug("Session Cookie {} for {} serial {} found".format(PHPSESSID,self.ip,serial))
        
        r = requests.get(urldata, cookies=self.sessioncookie, headers=headers)
        if r.status_code == 200:
            response = r.json()
            for keyword, item in self.items.items():
                try:
                    value = response[keyword]
                    item(value, trigger=self.get_trigger())
                except:
                    self.logger.warning("keyword {} not in json response".format(keyword))
            #self.logger.debug("EM300: reading took: {:.4f}s".format(time.time() - start))
        else:
            self.sessioncookie = None # hoffentlich klappts dann beim nächsten mal