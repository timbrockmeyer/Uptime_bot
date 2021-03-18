from time import time, sleep
from threading import Thread

try:
    import httplib
except:
    import http.client as httplib


class ConnectivityTracker(Thread):

    def __init__(self):

        Thread.__init__(self)
        self.daemon = True
        self.reset()
        self.start()

    def _display_str(self, t):
        h, r = divmod(round(t),3600)
        d, h = divmod(h, 24)
        m, r = divmod(r, 60)
        s = int(round(r))

        values = [d, h, m, s]
        words = ['day', 'hour', 'minute', 'second']
        for i, val in enumerate(values):
            if val > 0:
                words[i] = ''.join([f'{val} ', words[i], str(('s' if val > 1 else ''))])
            else:
                words[i] = ''
        return ', '.join(string for string in words if string) if any(words) else 'None'

    def reset(self):
        self.uptime = 0
        self.downtime = 0

    def report(self):
        uptime = self._display_str(self.uptime)
        downtime = self._display_str(self.downtime)
        return uptime, downtime

    def run(self):
        url = 'google.com'
        conn = httplib.HTTPConnection(url, timeout=3)
        t = time()
        while True:
            try:
                conn.request('HEAD', '/')
                conn.close()
                self.uptime += (time() - t)
            except Exception as e:
                print(e)
                self.downtime += (time() - t)

            t = time()
            sleep(1)
