import platform
import uuid

import arrow
from cowsay.__main__ import cli


def os():
    print(platform.system())


def say():
    cli()


def ts():
    timestamp = arrow.now().timestamp()
    print(int(timestamp))


def ms():
    timestamp = arrow.now().timestamp()
    print(int(timestamp * 1000))


def gen_uuid():
    print(uuid.uuid4())
