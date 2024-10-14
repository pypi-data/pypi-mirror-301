#!/opt/homebrew/anaconda3/envs/quantfin/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 下午4:51
# @Author  : @Zhenxi Zhang
# @File    : __init__.py.py
# @Software: PyCharm

import logging
import typing
from logging.handlers import RotatingFileHandler
import configparser


def setup_logger(
    log_file: str = "", name: typing.Optional[str] = __name__, level: int = logging.DEBUG
) -> logging.Logger:
    """设置日志记录器，并根据需要添加一个RotatingFileHandler来处理日志文件的滚动。

    Args:
        log_file (str, optional): 日志文件的路径。如果提供，则会添加一个RotatingFileHandler。
            Defaults to "".
        name (str, optional): 日志记录器的名字。如果为None，则默认使用根记录器。
            Defaults to None.
        level (int, optional): 日志记录级别。Defaults to logging.INFO.

    Returns:
        logging.Logger: 配置好的日志记录器对象。
    """
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if log_file:
        handler = RotatingFileHandler(
            log_file, maxBytes=1024 * 1024, backupCount=5, encoding="utf-8"
        )
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def read_config(config_file: str, encoding: str = "utf-8") -> configparser.ConfigParser:
    """读取配置文件，并处理可能发生的异常。

    Args:
        config_file (str): 配置文件的路径。
        encoding (str, optional): 配置文件的编码方式。Defaults to "utf-8".

    Returns:
        configparser.ConfigParser: 读取的配置文件内容。

    Raises:
        Exception: 如果读取配置文件失败，则抛出此异常。
    """
    config = configparser.ConfigParser()
    try:
        config.read(config_file, encoding=encoding)
    except Exception as e:
        raise Exception(f"读取配置文件 {config_file} 失败：{e}")
    return config
