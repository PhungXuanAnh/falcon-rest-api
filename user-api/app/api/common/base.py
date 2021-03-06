# -*- coding: utf-8 -*-

import falcon
import json

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict

import logging
from app.utils.database import new_alchemy_encoder
from app.config import BRAND_NAME, POSTGRES_HOST
from app.utils.database import engine
from app.utils.errors import NotSupportedError

LOG = logging.getLogger('app')


class BaseResource(object):
    HELLO_WORLD = {
        'server': '%s' % BRAND_NAME,
        'database': '%s (%s)' % (engine.name, POSTGRES_HOST)
    }

    def to_json(self, body_dict):
        return json.dumps(body_dict)

    def from_db_to_json(self, db):
        return json.dumps(db, cls=new_alchemy_encoder())

    def on_error(self, res, error=None):
        res.status = error['status']
        meta = OrderedDict()
        meta['code'] = error['code']
        meta['message'] = error['message']

        obj = OrderedDict()
        obj['meta'] = meta
        res.body = self.to_json(obj)

    def on_success(self, res, data=None):
        res.status = falcon.HTTP_200
        meta = OrderedDict()
        meta['code'] = 200
        meta['message'] = 'OK'

        obj = OrderedDict()
        obj['meta'] = meta
        obj['data'] = data
        res.body = self.to_json(obj)

    def on_get(self, req, res):
        if req.path == '/':
            res.status = falcon.HTTP_200
            res.body = self.to_json(self.HELLO_WORLD)
        else:
            raise NotSupportedError(method='GET', url=req.path)

    def on_post(self, req, res):
        raise NotSupportedError(method='POST', url=req.path)

    def on_put(self, req, res):
        raise NotSupportedError(method='PUT', url=req.path)

    def on_delete(self, req, res):
        raise NotSupportedError(method='DELETE', url=req.path)
