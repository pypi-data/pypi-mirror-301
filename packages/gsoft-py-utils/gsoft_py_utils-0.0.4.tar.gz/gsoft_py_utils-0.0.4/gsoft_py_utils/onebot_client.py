#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import logging
import http
import atexit
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class OnebotClient:
    OK = 0

    def __init__(self, api_key, api_url='http://localhost:8080/'):
        self.api_url = api_url
        if not api_url.endswith("/"):
            self.api_url += "/"
        self.verify = True
        self.api_key = api_key
        self.session = ''
        self.send_private_msg_url = urljoin(self.api_url, 'send_private_msg')

    @classmethod
    def from_settings(cls, settings):
        client = cls(
            api_key=settings.get('ONEBOT_API_KEY'),
            api_url=settings.get('ONEBOT_API_URL', 'http://localhost:8080/')
        )
        return client

    def process_res(self, res):
        if res.status_code != http.HTTPStatus.OK:
            logger.error(f'request {res.url} failed, status: {res.status_code}')
            return None
        try:
            res_json = res.json()
            if res_json['retcode'] != self.OK:
                logger.error(f'request {res.url} failed, {res_json}')
                return None
            else:
                logger.debug(f'request {res.url} success, {res_json}')
                return res_json
        except Exception as e:
            logger.error(f'request {res.url} failed, exception: {e}')
            return None

    def send_text_msg(self, recipients, msg):
        if type(recipients) is int or type(recipients) is str:
            self._send_text_msg(recipients, msg)
            return
        for recipient in recipients:
            self._send_text_msg(recipient, msg)

    def _send_text_msg(self, recipient, msg):
        res = requests.post(self.send_private_msg_url, headers={
            "Authorization": f"Bearer {self.api_key}"
        }, json={
            "user_id": int(recipient),
            "message": msg
        }, verify=self.verify)
        res_json = self.process_res(res)
        logger.info(f'client_send_text_msg({msg}) to ({recipient}) {res_json}')


if __name__ == '__main__':
    sh = logging.StreamHandler()  # 往屏幕上输出
    logger.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    sender = 0
    api_key = 'a123456789'
    api_url = "http://localhost:8080/"
    recipients = [0]
    client = OnebotClient(api_key, api_url)
    client.send_text_msg(recipients, 'hello world')
