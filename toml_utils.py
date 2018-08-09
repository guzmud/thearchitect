#!/usr/bin/env python3

from os import mkdir
from pathlib import Path
from secrets import choice
from string import ascii_letters, digits


def stupid_randint():
    return choice(digits)


def stupid_randval(length):
    return ''.join(choice(ascii_letters+digits) for k in range(length))


def nameval():
    return stupid_randval(7)


def versionval():
    return "0.{}.{}".format(stupid_randint(), stupid_randint())


def authorsval():
    return [stupid_randval(5),]


def publishval(b=False):
    return "{}".format(b).lower()


def package():
    return {"name": nameval(),
            "version": versionval(),
            "authors": authorsval(),
            "publish": publishval(False),
            }


def to_toml(secname, secdict):
    sectoml = "[{}]\n".format(secname)
    for k, v in secdict.items():
        if type(v) is list:
            v = "[{}]".format(', '.join(['"{}"'.format(j) for j in v]))
        else:
            v = '"{}"'.format(v)
        sectoml += "{} = {}\n".format(k, v)
    return sectoml


def gen_toml(path):
    path = Path(path, 'Cargo.toml')
    tomldata = to_toml('package', package())
    with open(path, 'w') as f:
        f.write(tomldata)


def fake_cargo(path):
    srcpath = Path(path, "src")
    mkdir(srcpath)
    gen_toml(path)
