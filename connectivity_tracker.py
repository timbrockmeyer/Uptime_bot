import time
import threading

try:
    import httplib
except:
    print('Failed import \'httplib\' \nImporting \'http.client\'')
    import http.client as httplib


class ConnectivityTracker(threading.Thread):

    def __init__(self):

        self.up_since = self.current_time()
        self.uptime = 0
        self.downtime = 0

        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def current_time(self):
        return time.strftime("%H:%M:%S", time.localtime())

    def run(self):
        url = 'google.com'
        conn = httplib.HTTPConnection(url, timeout=3)
        t = time.time()
        while True:
            try:
                conn.request("HEAD", "/")
                conn.close()
                self.uptime += (time.time() - t)
            except Exception as e:
                print(e)
                self.downtime += (time.time() - t)

            t = time.time()
            time.sleep(1)
