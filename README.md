# Prosody statistics for Zabbix

This code enables you to track your prosody instance in Zabbix. These metrics are supported:

* Connected Clients
* Connected Components
* Connected Users
* Incoming server connections
* Memory allocated
* Memory returnable
* Memory unused
* Memory used
* Memory used by Lua
* Outgoing server connections
* Prosody Version

This is all due to the work of [mod_statistics](https://code.google.com/p/prosody-modules/source/browse/mod_statistics/), which exports all these metrics.

## Install

* Install [mod_statistics](https://code.google.com/p/prosody-modules/source/browse/mod_statistics/).
* Import prosody_template.xml into zabbix.
* Assign the new Prosody Template to your xmpp host.
* Edit the head of prosody.py to reflect your setup.
* Setup a cronjob to call prosody.py.
