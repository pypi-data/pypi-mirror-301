##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.25.1+obcheckpoint(0.0.12);ob(v1)                              #
# Generated on 2024-10-10T01:08:08.975330                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.event_logger

class DebugEventLogger(metaflow.event_logger.NullEventLogger, metaclass=type):
    @classmethod
    def get_worker(cls):
        ...
    ...

class DebugEventLoggerSidecar(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    ...

