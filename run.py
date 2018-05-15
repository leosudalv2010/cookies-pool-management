# !/usr/bin/python3
# -*- coding: utf-8 -*-

from createcookies import DoubanCreateCookies
from verifycookies import DoubanVerifyCookies
from api import app
from settings import APIHOST, APIPORT


class Scheduler(object):
    @staticmethod
    def create_cookies():
        try:
            creater = DoubanCreateCookies()
            creater.run()
            print('All the cookies have been created')
            del creater
        except Exception as e:
            print(e.args)

    @staticmethod
    def verify_cookies():
        try:
            verifier = DoubanVerifyCookies()
            verifier.run()
            print('All the cookies have been verified')
            del verifier
        except Exception as e:
            print(e.args)

    @staticmethod
    def api():
        app.run(host=APIHOST, port=APIPORT)
        print('CookiesPool API has been started')

    @staticmethod
    def run():
        Scheduler.verify_cookies()
        Scheduler.create_cookies()
        Scheduler.api()


if __name__ == '__main__':
    Scheduler.run()

