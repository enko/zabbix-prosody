#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2010 Christoph Heer (Christoph.Heer@googlemail.com)
# Copyright (c) 2015 Tim Schumacher (tim@datenknoten.me)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the \"Software\"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys
import os
import telnetlib
import re
from subprocess import Popen, PIPE, STDOUT
import urllib
from pprint import pprint

config = {
    'zabbix': {
        'sender': '/usr/bin/zabbix_sender',
        'server': 'monitor.int.datenknoten.me',
        'host' : 'xmpp.int.datenknoten.me'
    },
    'prosody': {
        'host': 'localhost',
        'port': 5782
    },
    'collect_vhost_users': True,
    'debug' : False
}

def zabbix_write(item,value):
    send_str = "%s %s %s" % (config['zabbix']['host'],item,value)
    proc = Popen([config['zabbix']['sender'],'--zabbix-server',config['zabbix']['server'],'--input-file','-'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    output = proc.communicate(input=send_str)[0]
    if (config['debug']):
        print(send_str)
        print(output)

def main():
    host = config['prosody']['host']
    port = config['prosody']['port']

    telnet = telnetlib.Telnet(host, port)
    telnet_response = telnet.read_until("\n\n",5).split("\n")

    for line in telnet_response:        
        elements = line.split(" ")
        if (len(elements) > 2):
            key = elements[1].replace('"','')
            if (key == 'version'):
                value = elements[2].replace('(','').replace(')','').replace('"','')
            else:
                value = int(elements[2].replace('(','').replace(')','').replace('"',''))
            key = "prosody." + key
            zabbix_write(key,value)


    if (config['collect_vhost_users']):
        base_dir = os.environ.get('internal_storage_path', "/var/lib/prosody")
        if os.path.isdir(base_dir):
            vhosts = listdirs(base_dir)
            for vhost in vhosts:
                account_dir = os.path.join(base_dir, vhost, "accounts")
                if os.path.isdir(account_dir):
                    vhost = urllib.unquote(vhost)
                    munin_var = vhost.replace(".","_")
                    accounts = len(list(listfiles(account_dir)))
                    zabbix_write("prosody.%s.users" % (munin_var),accounts)

def listdirs(folder):
    for x in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, x)):
            yield x

def listfiles(folder):
    for x in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, x)):
            yield x

if __name__ == '__main__':
    main()
