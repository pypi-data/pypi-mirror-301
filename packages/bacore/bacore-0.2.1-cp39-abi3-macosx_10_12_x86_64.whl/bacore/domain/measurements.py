"""Measurements module."""

from datetime import date, datetime, timedelta
from dataclasses import dataclass


@dataclass(frozen=True)
class Time:
    """Class for time related settings."""

    now = datetime.now()
    now_s = now.strftime("%Y-%m-%d %H:%M:%S")
    today = date.today()
    today_s = today.strftime("%Y-%m-%d")
    yesterday = today - timedelta(days=1)
    yesterday_s = yesterday.strftime("%Y-%m-%d")
    ty = today.strftime("%Y")
    tm = today.strftime("%m")
    td = today.strftime("%d")
    yy = yesterday.strftime("%Y")
    ym = yesterday.strftime("%m")
    yd = yesterday.strftime("%d")
