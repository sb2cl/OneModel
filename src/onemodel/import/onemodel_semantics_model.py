#!/usr/bin/env python

# CAVEAT UTILITOR
#
# This file was automatically generated by TatSu.
#
#    https://pypi.python.org/pypi/tatsu/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.

from __future__ import annotations

from tatsu.objectmodel import Node
from tatsu.semantics import ModelBuilderSemantics


class ModelBase(Node):
    pass


class OneModelModelBuilderSemantics(ModelBuilderSemantics):
    def __init__(self, context=None, types=None):
        types = [
            t for t in globals().values()
            if type(t) is type and issubclass(t, ModelBase)
        ] + (types or [])
        super(OneModelModelBuilderSemantics, self).__init__(context=context, types=types)


class DefineParameter(ModelBase):
    comment = None
    name = None
    units = None
    value = None
