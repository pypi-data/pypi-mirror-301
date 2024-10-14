#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from typing import Optional, Set, Type, TypeVar

from scrapy.http.request import Request
from scrapy.settings import BaseSettings
from scrapy.spiders import Spider
from scrapy.dupefilters import BaseDupeFilter
from elasticsearch import Elasticsearch
from http import HTTPStatus
from gsoft_py_utils.esclient import ESClient

ESDupeFilterTV = TypeVar("ESDupeFilterTV", bound="ESDupeFilter")

logger = logging.getLogger(__name__)

class ESDupeFilter(BaseDupeFilter):
    """Request ES duplicates filter"""

    def __init__(self, settings) -> None:
        self.logdupes = True
        self.debug = settings.getbool('DUPEFILTER_DEBUG', False)
        self.es_client = ESClient.from_settings(settings)
        if self.es_client is None:
            logger.error("es_client init failed, disable es dup filter")

    @classmethod
    def from_settings(cls: Type[ESDupeFilterTV], settings: BaseSettings) -> ESDupeFilterTV:
        return cls(settings)

    def is_request_dup(self, request: Request, res) -> bool:
        return res and "found" in res and res["found"]

    def request_seen(self, request: Request) -> bool:
        fp = self.request_fingerprint(request)
        if fp and self.es_client:
            try:
                res = self.es_client.get(id=fp, ignore=[HTTPStatus.NOT_FOUND])
                return self.is_request_dup(request, res)
            except Exception as e:
                logger.error('request %s failed, exception: %s', fp, e)
                return False
        else:
            return False

    def request_fingerprint(self, request: Request) -> str:
        if request.cb_kwargs and 'id' in request.cb_kwargs:
            return request.cb_kwargs['id']
        elif request.cb_kwargs and 'item' in request.cb_kwargs and 'id' in request.cb_kwargs['item']:
            return request.cb_kwargs['item']['id']
        else:
            logger.warning(f'Request[{request.url}] cb_kwargs not found "id" or "item" argument, do not filter.')
            return ''

    def close(self, reason: str) -> None:
        pass

    def log(self, request: Request, spider: Spider) -> None:
        unique_id = self.request_fingerprint(request)
        if self.debug:
            msg = "Filtered duplicate request: %(request)s (unique_id: %(unique_id)s)"
            args = {'request': request, 'unique_id': unique_id}
            spider.logger.info(msg, args, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request: %(request)s (unique_id: %(unique_id)s)"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            spider.logger.info(msg, {'request': request, 'unique_id': unique_id}, extra={'spider': spider})
            self.logdupes = False

        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)
