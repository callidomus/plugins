#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Copyright 2013 KNX-User-Forum e.V.           http://knx-user-forum.de/
#########################################################################
#  DLMS plugin for SmartHome.py.         http://mknx.github.io/smarthome/
#
#  This plugin is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This plugin is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this plugin. If not, see <http://www.gnu.org/licenses/>.
#########################################################################

import time
import serial
import re
from threading import Semaphore

import lib.plugin


class DLMS(lib.plugin.Plugin):

    def __init__(self, core, conf):
        lib.plugin.Plugin.__init__(self, core, conf)
        self._core = core
        self._obis_codes = {}
        self._init_seq = bytes('/?!\r\n', 'ascii')
        self._request = bytearray('\x06000\r\n', 'ascii')

        self._baudrate = conf.get('baudrate', 'auto')
        if self._baudrate == 'auto':
            self._baudrate = -1
        else:
            pow2 = int(self._baudrate / 600)
            self._request[2] = 0x30
            while (pow2 > 0):
                pow2 >>= 1
                self._request[2] += 1

        self._update_cycle = conf.get('update_cycle', 60)
        self._use_checksum = conf.get('use_checksum', True)
        self._reset_baudrate = conf.get('reset_baudrate', True)
        self._no_waiting = conf.get('no_waiting', False)
        self._serial = serial.Serial(
            conf.get('serialport', 'UNKNOWN'),
            300,
            bytesize=serial.SEVENBITS,
            parity=serial.PARITY_EVEN,
            timeout=2)
        self._sema = Semaphore()
        core.scheduler.add(
            'DLMS',
            self._save_update_values,
            prio=5,
            cycle=self._update_cycle)

    def start(self):
        self.alive = True

    def stop(self):
        self.alive = False
        try:
            self._serial.close()
        except:
            pass

    def _update_values(self):
        self.logger.debug("dlms: update")
        start = time.time()
        try:
            if self._reset_baudrate:
                self._serial.baudrate = 300
                self.logger.debug("dlms: (re)set baudrate to 300 Baud")
            self._serial.write(self._init_seq)
            self._serial.flush()  # self._serial.drainOutput()
            self._serial.reset_input_buffer()  # self._serial.flushInput()
            response = bytes()
            prev_length = 0
            while self.alive:
                response += self._serial.read()
                length = len(response)
                # break if timeout or newline-character
                if (response[-1] == 0x0a):
                    break
                if (length == prev_length):
                    self.logger.warning(
                        "dlms: read timeout! - response={}".format(response))
                    return
                prev_length = length
        except Exception as e:
            self.logger.warning("dlms: {0}".format(e))
        # self.logger.warning("dlms: response={}".format(response))
        if (len(response) < 5) or ((response[4] - 0x30) not in range(6)):
            self.logger.warning(
                "dlms: malformed response to init seq={}".format(response))
            return

        if (self._baudrate == -1):
            self._baudrate = 300 * (1 << (response[4] - 0x30))
            self.logger.debug(
                "dlms: meter returned capability for {} Baud".format(
                    self._baudrate))
            self._request[2] = response[4]
        try:
            if not self._no_waiting:
                time.sleep(0.5)
            self._serial.write(self._request)
            if not self._no_waiting:
                time.sleep(0.25)

            self._serial.flush()  # self._serial.drainOutput()
            self._serial.reset_input_buffer()  # self._serial.flushInput()
            if (self._baudrate != self._serial.baudrate):
                # change request to set higher baudrate
                self.logger.debug(
                    "dlms: switching to {} Baud".format(
                        self._baudrate))
                self._serial.baudrate = self._baudrate
            response = bytes()
            prev_length = 0
            while self.alive:
                response += self._serial.read()
                length = len(response)
                if (not self._use_checksum and (
                        response[-1] == 0x03)) or ((length > 1) and (response[-2] == 0x03)):
                    break
                if (length == prev_length):
                    self.logger.warning(
                        "dlms: read timeout! - response={}".format(response))
                    return
                prev_length = length
        except Exception as e:
            self.logger.warning("dlms: {0}".format(e))
            return

        self.logger.debug("dlms: reading took: {:.2f}s".format(time.time() - start))
        if self._use_checksum:
            # perform checks (start with STX, end with ETX, checksum match)
            checksum = 0
            for i in response[1:]:
                checksum ^= i
            if (len(response) < 5) or (response[0] != 0x02) or (
                    response[-2] != 0x03) or (checksum != 0x00):
                self.logger.warning(
                    "dlms: checksum/protocol error: response={} checksum={}".format(
                        ' '.join(
                            hex(i) for i in response),
                        checksum))
                return
        # print(str(response[1:-4], 'ascii'))
        for line in re.split('\r\n', str(response[1:-4], 'ascii')):
            # if re.match('[0-9]+\.[0-9]\.[0-9](.+)', line): # allows only
            # x.y.z(foo)
            if re.match('[0-9]+\.[0-9].+(.+)', line):  # allows also x.y(foo)
                try:
                    # data = re.split('[(*)]', line)
                    data = line.split('(')
                    data[1:3] = data[1].strip(')').split('*')
                    if (len(data) == 2):
                        self.logger.debug("dlms: {} = {}".format(data[0], data[1]))
                    else:
                        self.logger.debug(
                            "dlms: {} = {} {}".format(
                                data[0], data[1], data[2]))
                    if data[0] in self._obis_codes:
                        for item in self._obis_codes[data[0]]['items']:
                            item(data[1], caller='DLMS', 'OBIS'=data[0])
                except Exception as e:
                    self.logger.warning(
                        "dlms: line={} exception={}".format(
                            line, e))

    def _save_update_values(self, value=None, trigger=None):
        if(self._sema.acquire(blocking=False)):
            self._update_values()
            self._sema.release()
        else:
            self.logger.debug("update is alrady running nothing todo")

    def pre_stage(self):
        for node in self._core.config.query_nodes('dlms_obis_code'):
            obis_code = node.attr['dlms_obis_code']
            if obis_code not in self._obis_codes:
                self._obis_codes[obis_code] = {'items': [node], 'logics': []}
            else:
                self._obis_codes[obis_code]['items'].append(node)
        return None
