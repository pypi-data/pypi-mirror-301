#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:
# Description:

from typing import List, Optional
from urllib.parse import urlparse
from .exceptions import PipConfigException
from .pip_tools import pip_config_set_registry, get_user_config


class Registry:
    name: str
    index_url: str
    host: str

    def __init__(self, name: str, index_url: str):
        self.name = name
        self.index_url = index_url
        self.host = urlparse(self.index_url).netloc


REGISTRYS = [
    Registry('tencent', 'http://mirrors.cloud.tencent.com/pypi/simple'),
    Registry('tsinghua', 'https://pypi.tuna.tsinghua.edu.cn/simple'),
    Registry('aliyun', 'https://mirrors.aliyun.com/pypi/simple'),
    Registry('edu', 'https://mirrors.ustc.edu.cn/pypi/simple'),
]

REGISTRY_MAP = {o.name: o for o in REGISTRYS}


def get_registrys() -> List[Registry]:
    REGISTRYS.sort(key=lambda o: o.name)
    return REGISTRYS


def get_registry(name: str) -> Optional[Registry]:
    return REGISTRY_MAP.get(name)


def set_registry(name: str):
    r = get_registry(name)
    if not r:
        raise PipConfigException(f"registry: {name} not found")
    if not pip_config_set_registry(r.index_url, r.host):
        raise PipConfigException("set registry failed")


def get_use_registry() -> Optional[Registry]:
    config = get_user_config()
    if not config:
        return None
    if not config.global_:
        return None

    for r in REGISTRYS:
        if r.host == config.global_.trusted_host:
            return r
    return None
