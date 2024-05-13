import random
import string

from datetime import datetime
from zoneinfo import ZoneInfo
from random_username.generate import generate_username


def random_domain() -> str:
    return random.choices(
        ["google", "outlook", "gmail", "yahoo", "hotmail", "live", "twitter"], k=32
    )[0]


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_nickname() -> str:
    return generate_username(1)[0]


def random_email() -> str:
    return f"{random_nickname()}@{random_domain()}.com"


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")
