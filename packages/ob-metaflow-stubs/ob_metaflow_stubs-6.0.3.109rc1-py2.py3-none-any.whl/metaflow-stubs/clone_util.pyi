##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.25.1+obcheckpoint(0.0.13);ob(v1)                              #
# Generated on 2024-10-10T01:39:58.536260                                        #
##################################################################################

from __future__ import annotations


class MetaDatum(tuple, metaclass=type):
    """
    MetaDatum(field, value, type, tags)
    """
    @staticmethod
    def __new__(_cls, field, value, type, tags):
        """
        Create new instance of MetaDatum(field, value, type, tags)
        """
        ...
    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...
    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...
    ...

def clone_task_helper(flow_name, clone_run_id, run_id, step_name, clone_task_id, task_id, flow_datastore, metadata_service, origin_ds_set = None, attempt_id = 0):
    ...

