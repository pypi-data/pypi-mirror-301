#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

def read_file(file_name):
    content = ''
    if not os.path.exists(file_name):
        raise IOError(f'{file_name} not exist')
    if not os.path.isfile(file_name):
        raise IOError(f'{file_name} not file')
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

DEFAULT_SECRETS_BASE_DIR = '/run/secrets'

def get_secrets_base_dir(secrets_base_dir : str = None):
    if secrets_base_dir is None or len(secrets_base_dir) == 0:
        secrets_base_dir = os.environ.get('SECRETS_BASE_DIR', '').strip()
        if len(secrets_base_dir) == 0:
            secrets_base_dir = DEFAULT_SECRETS_BASE_DIR
    return secrets_base_dir
        
def read_secret(secret_file_name_or_env : str, secrets_base_dir = None):
    secrets_base_dir = get_secrets_base_dir(secrets_base_dir)
    if secret_file_name_or_env is None or len(secret_file_name_or_env) == 0:
        raise Exception('secret文件名不能为空')
    secret_file_name_or_env = secret_file_name_or_env.strip()
    secret_file_name = ''
    if secret_file_name_or_env.endswith('_FILE'):
        secret_file_name = os.environ.get(secret_file_name_or_env, '')
    elif secret_file_name_or_env.endswith('.txt') or secret_file_name_or_env.endswith('.json'):
        secret_file_name = secret_file_name_or_env
    else:
        secret = os.environ.get(secret_file_name_or_env, '')
        if not (secret is None or len(secret) == 0):
            return secret
        secret_file_name = secret_file_name_or_env
    secret_full_file_name = os.path.join(secrets_base_dir, secret_file_name)
    return read_file(secret_full_file_name)