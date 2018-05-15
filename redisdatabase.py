# !/usr/bin/python3
# -*- coding: utf-8 -*-

from redis import StrictRedis, ConnectionPool
from settings import HOST, PORT, DB, PASSWORD, WEBSITE
import random
import json


class Redis(object):
    def __init__(self, category):
        self.category = category
        self.pool = ConnectionPool(host=HOST, port=PORT, db=DB, password=PASSWORD)
        self.redis = StrictRedis(connection_pool=self.pool)

    def name(self):
        """
        Create the name of Redis hash mapping table, category should be 'account' or 'cookies'
        """
        return '{}:{}'.format(self.category, WEBSITE)

    def write(self, key, value):
        self.redis.hset(self.name(), key, value)

    def read(self, key):
        return self.redis.hget(self.name(), key)

    def delete(self, key):
        self.redis.hdel(self.name(), key)

    def key_valued_pairs(self):
        return self.redis.hgetall(self.name())

    def count(self):
        return len(list(self.key_valued_pairs().values()))

    def random(self):
        """
        Fetch a random cookies from the database
        """
        cookies_list = list(self.key_valued_pairs().values())
        random_cookies = random.choice(cookies_list)
        return random_cookies
