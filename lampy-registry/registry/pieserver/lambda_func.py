import sys
import __builtin__

try:
    lampy = __builtin__.__import__("lampy")
    Server = lampy.core.Server
except:
    print "Load Server from lampy.core failed"

try:
    core = __builtin__.__import__("core")
    Server = core.Server
except:
    print "Load Server from core failed"

assert "Server" in globals() and Server not None

def handler(event):
    server = Server()
    return event

import pytest
def test_load():
