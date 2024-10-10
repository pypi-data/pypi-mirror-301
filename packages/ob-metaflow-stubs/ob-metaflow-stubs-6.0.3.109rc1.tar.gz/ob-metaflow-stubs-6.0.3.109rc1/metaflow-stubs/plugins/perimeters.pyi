##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.25.1+obcheckpoint(0.0.13);ob(v1)                              #
# Generated on 2024-10-10T01:39:58.508541                                        #
##################################################################################

from __future__ import annotations

import typing

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

CURRENT_PERIMETER_KEY: str

CURRENT_PERIMETER_URL: str

CURRENT_PERIMETER_URL_LEGACY_KEY: str

def get_perimeter_config_url_if_set_in_ob_config() -> typing.Optional[str]:
    ...

