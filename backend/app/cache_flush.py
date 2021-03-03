from app.common.conn_varnish import VarnishManager

import requests

class Cache_flush(object):

    def __init__(self, host):
        self.host = host

