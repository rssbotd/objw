# This file is placed in the Public Domain.
# pylint: disable=C,I,R


"disk"


import os
import pathlib
import _thread


from objx         import update
from objx.decoder import load
from objx.encoder import dump
from objw.workdir import store
from objw.utils   import ident


lock = _thread.allocate_lock()
disklock = _thread.allocate_lock()


"utilities"

def cdir(pth):
    "create directory."
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


"methods"


def fetch(obj, pth):
    "read object from disk."
    with disklock:
        pth2 = store(pth)
        read(obj, pth2)
        return os.sep.join(pth.split(os.sep)[-3:])


def read(obj, pth):
    "read an object from file path."
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            update(obj, load(ofile))


def sync(obj, pth=None):
    "sync object to disk."
    with disklock:
        if pth is None:
            pth = ident(obj)
        pth2 = store(pth)
        write(obj, pth2)
        return pth


def write(obj, pth):
    "write an object to disk."
    with lock:
        cdir(pth)
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile, indent=4)


def __dir__():
    return (
        'fetch',
        'read',
        'sync',
        'write'
    )
