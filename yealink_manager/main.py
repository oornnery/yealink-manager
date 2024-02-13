import logging
from PIL import Image
from io import BytesIO
from httpx import Client


logging.basicConfig(level=logging.INFO)


class YealinkController:
    URL_BASE = 'http://{username}:{password}@{ip}/'
    def __init__(self, username: str, password: str, ip: str) -> None:
        """Yealink Controller Actions

        Args:
            username (str): Username on Yealink IP Phone
            password (str): Password on Yealink IP Phone
            ip (str): IP Address of Yealink IP Phone
        
        https://www.manualslib.com/manual/1260800/Yealink-Sip-T2-Series.html?page=755#manual
        """
        self.client = Client(
            base_url=self.URL_BASE.format(username=username, password=password, ip=ip)
            )
        self.url = 'servlet'

    def dial(self, number: str):
        req = self.client.get(url=self.url, params={'number': number, 'outgoing_uri': 'URI'})
        req.raise_for_status()

    def hangup(self):
        req = self.client.get(url=self.url, params={'key': 'X'})
        req.raise_for_status()

    def answer(self):
        req = self.client.get(url=self.url, params={'key': 'ENTER'})
        req.raise_for_status()

    def mute(self):
        req = self.client.get(url=self.url, params={'key': 'MUTE'})
        req.raise_for_status()

    def set_line(self, line: int):
        req = self.client.get(url=self.url, params={'key': f'L{line}'})
        req.raise_for_status()
    
    def redial(self):
        req = self.client.get(url=self.url, params={'key': 'RD'})
        req.raise_for_status()
    
    def speaker(self):
        req = self.client.get(url=self.url, params={'key': 'SPEAKER'})
        req.raise_for_status()
    
    def headset(self):
        req = self.client.get(url=self.url, params={'key': 'HEADSET'})
        req.raise_for_status()

    def hold(self):
        req = self.client.get(url=self.url, params={'key': 'HOLD'})
        req.raise_for_status()
    
    def cancel(self):
        req = self.client.get(url=self.url, params={'key': 'CANCEL'})
        req.raise_for_status()

    def volume_up(self):
        req = self.client.get(url=self.url, params={'key': 'VOLUME_UP'})
        req.raise_for_status()
    
    def volume_down(self):
        req = self.client.get(url=self.url, params={'key': 'VOLUME_DOWN'})
        req.raise_for_status()

    def send_dtmf(self, dtmf: str):
        req = self.client.get(url=self.url, params={'key': dtmf})
        req.raise_for_status()
    
    def reboot(self):
        req = self.client.get(url=self.url, params={'key': 'Reboot'})
        req.raise_for_status()

    def auto_provisioning(self):
        req = self.client.get(url=self.url, params={'key': 'AutoP'})
        req.raise_for_status()

    def dnd_on(self):
        req = self.client.get(url=self.url, params={'key': 'DNDOn'})
        req.raise_for_status()

    def dnd_off(self):
        req = self.client.get(url=self.url, params={'key': 'DNDOff'})
        req.raise_for_status()

    def get_status(self):
        req = self.client.get(url=self.url, params={'phonecfg': 'get','accounts': 1,'dnd': 1,'fw': 1})
        req.raise_for_status()
        return req.content.decode('utf-8')

    def screenshot(self):
        # https://manualzz.com/doc/o/sqfrn/yealink-sip-t2-series-administrator-s-manual-action-uri?__cf_chl_tk=BPuqld5Wj6ZDdeBi5IdduVyNQC1nzvUh5E07ujBubas-1707845161-0-4261
        req = self.client.get(url=self.url, params={'command': 'screenshot'})
        req.raise_for_status()
        return req.content

if __name__ == "__main__":
    import time
    
    # Program parameters
    username = 'admin'
    password = '1d7pa55brasil'
    phone_ip = '192.168.15.10'
    try:
        yl = YealinkController(username, password, phone_ip)
        yl.set_line(1)
        yl.get_status()
        yl.dial('1234')
        yl.screenshot()
        time.sleep(5)
        yl.hangup()
        yl.screenshot()
    except Exception as e:
        logging.error(e)