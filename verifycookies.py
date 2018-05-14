# !/usr/bin/python3
# -*- coding: utf-8 -*-

from redisdatabase import Redis
from settings import VERIFY_URL
import requests
from lxml import etree
import json


class DoubanVerifyCookies(object):
    def __init__(self):
        self.cookies_db = Redis('cookies')
        self.verify_url = VERIFY_URL

    def run(self):
        for pair in self.cookies_db.key_valued_pairs().items():
            username, cookies = pair
            if cookies:
                self.verify(username.decode(), json.loads(cookies))

    def verify(self, username, cookies):
        """
        Add cookies to a requests session and verify if it is valid or not
        """
        print('Now verifying cookies of:{}'.format(username))
        headers = {
            'Host': 'www.douban.com',
            'User-Agent': 'Mozilla/5.0',
        }
        session = requests.Session()
        requests.utils.add_dict_to_cookiejar(session.cookies, cookies)
        response = session.get(self.verify_url, headers=headers)
        selector = etree.HTML(response.text)
        if not selector.xpath('//input[@value="更新设置"]'):
            print('Cookies of:{} is expired'.format(username))
            self.cookies_db.delete(username)
            print('Delete cookies of:{}'.format(username))
        else:
            print('Cookies of {} is valid'.format(username))


if __name__ == '__main__':
    DoubanVerifyCookies().run()


