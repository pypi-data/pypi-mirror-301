#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com

from .registry import (
    get_registry,
    get_registrys,
    set_registry,
    get_use_registry,
)
from .http_tools import (
    test_latency
)


__all__ = [
    'get_registry',
    'get_registrys',
    'set_registry',
    'get_use_registry',
    'test_latency',
]
