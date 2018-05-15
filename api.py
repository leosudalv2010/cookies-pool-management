# !/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, g
from redisdatabase import Redis
from settings import WEBSITE

__all__ = ['app']
app = Flask(__name__)


def conn():
    if not hasattr(g, 'db'):
        g.db = Redis('cookies')
    return g.db


@app.route('/')
def hello():
    return '<h2>This is Cookies Pool System</h2>'


@app.route('/{}/count'.format(WEBSITE))
def get_count():
    count = conn().count()
    return '<h2>Number of cookies in Redis: {}</h2>'.format(count)


@app.route('/{}/random'.format(WEBSITE))
def get_cookies():
    cookies = conn().random()
    return cookies


if __name__ == '__main__':
    app.run()