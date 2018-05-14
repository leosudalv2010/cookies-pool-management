# !/usr/bin/python3
# -*- coding: utf-8 -*-

from redis import StrictRedis, ConnectionPool
from settings import HOST, PORT, DB, PASSWORD, WEBSITE


class Redis(object):
    def __init__(self, category):
        self.category = category
        self.pool = ConnectionPool(host=HOST, port=PORT, db=DB, password=PASSWORD)
        self.redis = StrictRedis(connection_pool=self.pool)

    def name(self):
        # create the name of Redis hash mapping table
        # category should be 'account' or 'cookies'
        return '{}:{}'.format(self.category, WEBSITE)

    def write(self, key, value):
        self.redis.hset(self.name(), key, value)

    def read(self, key):
        return self.redis.hget(self.name(), key)

    def delete(self, key):
        self.redis.hdel(self.name(), key)

    def key_valued_pairs(self):
        return self.redis.hgetall(self.name())