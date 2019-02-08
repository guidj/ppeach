"""
Serialization I/O for ppeach classes
"""

import json

from domain import Dependency
from domain import Param
from domain import Target
from domain import Task


def to_json(obj):
    if isinstance(obj, (Task, Target, Param, Dependency)):
        jrepr = vars(obj)
        for k, v in jrepr.iteritems():
            jrepr[k] = to_json(v)
        return jrepr
    elif isinstance(obj, (list, tuple)):
        return [to_json(v) for v in obj]
    elif isinstance(obj, dict):
        for k, v in obj.iteritems():
            obj[k] = to_json(v)
        return obj
    else:
        return obj
