#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:
# Description:
from configparser import ConfigParser
import subprocess
from typing import Optional
from pydantic import (
    BaseModel,
    Field,
)


PIP_CONF_CMD_PREFIXS = ['python', '-m', 'pip', 'config']
GLOBAL_TRUSTED_HOST = 'global.trusted-host'
GLOBAL_INDEX_URL = 'global.index-url'


class SubConfig(BaseModel):
    index_url: Optional[str] = Field(None, alias='index-url')
    trusted_host: Optional[str] = Field(None, alias='trusted-host')


class PipConfig(BaseModel):
    global_: Optional[SubConfig] = Field(None, alias='global')


class ConfigPath(BaseModel):
    path: Optional[str] = Field(None)
    exists: bool = Field(False)


class PipPath(BaseModel):
    global_: Optional[ConfigPath] = Field(None, alias='global')
    site: Optional[ConfigPath] = Field(None)
    user: Optional[ConfigPath] = Field(None)


def cmd_output(cmds: list) -> str:
    return subprocess.check_output(cmds).decode()


def pip_config_set(name: str, value: str) -> bool:
    cmds = [
        'pip',
        'config',
        'set',
        name,
        value
    ]
    res = cmd_output(cmds)
    if 'Writing to' in res:
        return True
    return False


def pip_config_get(name: str):
    cmds = list(PIP_CONF_CMD_PREFIXS)
    cmds.extend([
        'get',
        name
    ])
    return cmd_output(cmds)


def pip_config_list():
    out_byte = subprocess.check_output(['pip', 'config', 'list'])
    out_text = out_byte.decode()
    print(f"-{out_text}-", type(out_text))


def pip_config_debug():
    cmds = list(PIP_CONF_CMD_PREFIXS)
    cmds.extend([
        'debug'
    ])
    return cmd_output(cmds)


def line_to_path(line: str) -> ConfigPath:
    path, exists = line.split(",")
    cp = ConfigPath()
    cp.path = path.strip()
    cp.exists = True if 'True' in exists else False
    return cp


def get_pip_config_path(debug_text: Optional[str] = None) -> PipPath:
    '''获取 pip config 地址'''
    if not debug_text:
        debug_text = pip_config_debug()
    lines = debug_text.split("\n")
    p = PipPath()
    for i, line in enumerate(lines):
        if line == 'global:':
            p.global_ = line_to_path(lines[i+1])
        if line == 'site:':
            p.site = line_to_path(lines[i+1])
        if line == 'user:':
            p.user = line_to_path(lines[i+1])
            if not p.user.exists:
                p.user = line_to_path(lines[i+2])
    return p


def get_user_config() -> Optional[PipConfig]:
    conf = get_pip_config_path().user
    if not conf.exists:
        return None

    parser = ConfigParser()
    parser.read(conf.path)

    item = PipConfig()
    if 'global' in parser:
        item.global_ = SubConfig(**parser['global'])
    return item


def pip_config_set_registry(
    index_url: str,
    trusted_host: str,
):
    return (
        pip_config_set(GLOBAL_INDEX_URL, index_url) and
        pip_config_set(GLOBAL_TRUSTED_HOST, trusted_host)
    )


if __name__ == "__main__":
    pip_config_list()
    #  print(pip_config)

    config = ConfigParser()
    config.read('/Users/wxnacy/.config/pip/pip.conf')
    print(dict(config))
    c = config['global']
    print(c)
    print(dict(c))

    p = get_pip_config_path()
    print(p)

    print(get_user_config())
