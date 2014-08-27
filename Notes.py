# -*- coding:utf-8 -*-
import pymongo


def get(environment, service):
    mongo = pymongo.Connection('localhost')['trust']['notes']
    # will raise StopIteration if not found
    return mongo.find({'environment': environment, 'service': service}, {'_id': False}).limit(1).next()


def put(environment, service, note):
    mongo = pymongo.Connection('localhost')['trust']['notes']
    spec = {'environment': environment, 'service': service}
    doc = {'note': note}
    doc.update(spec)
    mongo.update(spec, doc, upsert=True, multi=False)


def all(environment):
    return Notes(environment)


class Notes(dict):
    def __init__(self, env):
        mongo = pymongo.Connection('localhost')['trust']['notes']
        for doc in mongo.find({'environment': env}, {'service': 1, 'note': 1}):
            self[doc['service']] = doc['note']
