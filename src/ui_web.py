import os
import configparser
import signal
import string
import json
from bottle import Bottle, template, static_file, error, request, response, view
from Database import ACNTBootDatabase
from queues import ui_webq

'''
command codes
'''

class UIWeb(Bottle):
    _db = None
    _games = None
    _prefs = None

    def __init__(self, name, gameslist, prefs):
        super(UIWeb, self).__init__()
        self.name = name
        self._games = gameslist
        self._prefs = prefs
        #set up routes
        self.route('/', method="GET", callback=self.index)
        self.route('/static/<filepath:path>', method="GET", callback=self.serve_static)
        self.route('/config', method="GET", callback=self.appconfig)
        self.route('/load/<node>/<fhash>', method="GET", callback=self.load)

    def start(self):
        self.db = ACNTBootDatabase('db.sqlite')
        self.run(host='0.0.0.0', port=8000, debug=False)

    def serve_static(self, filepath):
        if 'images/' in filepath and not os.path.isfile('static/'+filepath):
            return static_file('images/0.jpg', 'static')

        return static_file(filepath, 'static')

    def index(self):
        #FIXME
        filter_groups = self.db.getAttributes()
        filter_values = []
        filters = []
        if self._games != None:
            return template('index', games=self._games, filter_groups=filter_groups, filter_values=filter_values, activefilters=filters)
        else:
            return template('index')

    def appconfig(self):        
        #ugh why is html so poopy for integrating with
        if self._prefs['Main']['skip_checksum'] == 'True':
            skip_checksum = 'checked'
        else:
            skip_checksum =  ''

        if self._prefs['Main']['gpio_reset'] == 'True':
            gpio_reset = 'checked'
        else:
            gpio_reset =  ''

        #TODO: default settings are stupid
        eth0_ip = self._prefs['Network']['eth0_ip'] or '192.168.0.1'
        eth0_netmask = self._prefs['Network']['eth0_netmask'] or '255.255.255.0'

        wlan0_ip = self._prefs['Network']['wlan0_ip'] or '10.0.0.1'
        wlan0_netmask = self._prefs['Network']['wlan0_netmask'] or '255.255.255.0'

        dimm_ip = self._prefs['Network']['dimm_ip'] or '192.168.0.2'

        games_directory = self._prefs['Games']['directory'] or 'games'

        #render
        return template('config', skip_checksum=skip_checksum, gpio_reset=gpio_reset, eth0_ip=eth0_ip, eth0_netmask=eth0_netmask, wlan0_ip=wlan0_ip, wlan0_netmask=wlan0_netmask, dimm_ip=dimm_ip, games_directory=games_directory)

    def load(self, node, fhash):
        #TODO: load on target node
        ui_webq.put(["LOAD", fhash])

    #TODO: other routes