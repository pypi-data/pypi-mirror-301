##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.25.1+obcheckpoint(0.0.13);ob(v1)                              #
# Generated on 2024-10-10T01:39:58.594057                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

class AirflowException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class NotSupportedException(metaflow.exception.MetaflowException, metaclass=type):
    ...

