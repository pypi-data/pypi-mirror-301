#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
import logging
from elasticsearch import Elasticsearch
import pkgutil


logger = logging.getLogger(__name__)


class ESClient(Elasticsearch):
    def __init__(self, es_index_name, es_urls = ['http://localhost:9200'], index_mapping_file = 'mapping.json', package_name = '', *args, **kwargs):
        super().__init__(es_urls, *args, **kwargs)
        self.es_urls = es_urls
        self.es_index_name = es_index_name
        self.index_mapping_file = index_mapping_file
        self.package_name = package_name
        self.create_index()

    @classmethod
    def from_settings(cls, settings):
        es_url = settings.get('ES_URL', 'http://localhost:9200')
        es_index_name = settings.get('ES_INDEX_NAME')
        index_mapping_file = settings.get('ES_INDEX_MAPPING_FILE_NAME', 'mapping.json')
        es_user = settings.get('ES_USER', '')
        es_password = settings.get('ES_PASSWORD', '')
        es_api_key_id = settings.get('ES_API_KEY_ID', '')
        es_api_key = settings.get('ES_API_KEY', '')
        api_key_auth = None
        if es_api_key_id and es_api_key:
            api_key_auth = (es_api_key_id, es_api_key)
        http_auth = None
        if es_user or es_password:
            http_auth = (es_user, es_password)
        package_name = settings.get('BOT_NAME', '')
        es_client = None
        if api_key_auth:
            es_client = cls(es_index_name, [es_url], index_mapping_file, package_name, api_key=api_key_auth)
        elif http_auth:
            es_client = cls(es_index_name, [es_url], index_mapping_file, package_name, http_auth=http_auth)
        else:
            es_client = cls(es_index_name, [es_url], index_mapping_file, package_name)
        return es_client

    def get(self, id, doc_type=None, params=None, headers=None, **kwargs):
        return super().get(self.es_index_name, id=id, doc_type=doc_type, params=params, headers=headers, **kwargs)

    def index(self, body, doc_type=None, id=None, params=None, headers=None, **kwargs):
        return super().index(index=self.es_index_name, body=body, doc_type=doc_type, id=id, params=params, headers=headers, **kwargs)

    def read_index_mapping_content(self):
        if self.package_name:
            data = pkgutil.get_data(self.package_name, self.index_mapping_file)
            if not data:
                logger.error('read index mapping file %s from package %s failed', self.index_mapping_file, self.package_name)
            return data

        if not self.index_mapping_file or not os.path.exists(self.index_mapping_file):
                logger.error('es index mapping file %s does not exist', self.index_mapping_file)
                return None
        json_str = ''
        with open(self.index_mapping_file, encoding='utf-8') as f:
            json_str = f.read()
        if not json_str:
            logger.error('read es index mapping file(%s) failed', self.index_mapping_file)
        return json_str

    def create_index(self):
        if self.indices.exists(index=self.es_index_name):
            logger.info('es index(%s) already exists', self.es_index_name)
            return
        json_str = self.read_index_mapping_content()
        if json_str:
            self.indices.create(index=self.es_index_name, body=json_str)
