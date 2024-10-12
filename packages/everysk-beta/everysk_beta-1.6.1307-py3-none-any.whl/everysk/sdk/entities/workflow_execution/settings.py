###############################################################################
#
# (C) Copyright 2024 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

###############################################################################
#   Imports
###############################################################################
from everysk.core.fields import StrField, ListField, IntField, RegexField

###############################################################################
#   Settings Implementation
###############################################################################
WORKFLOW_EXECUTION_ID_PREFIX = StrField(default='wfex_', readonly=True)
WORKFLOW_EXECUTION_ID_LENGTH = IntField(default=25, readonly=True)
WORKFLOW_EXECUTION_ID_REGEX = RegexField(default=r'^wfex_[a-zA-Z0-9]{25}', readonly=True)

WORKFLOW_ID_PREFIX = StrField(default='wrkf_', readonly=True)
WORKFLOW_ID_LENGTH = IntField(default=25, readonly=True)
WORKFLOW_ID_REGEX = RegexField(default=r'^wrkf_[a-zA-Z0-9]{25}', readonly=True)

WORKFLOW_EXECUTION_STATUS_OK = StrField(default='OK', readonly=True)
WORKFLOW_EXECUTION_STATUS_COMPLETED = StrField(default='COMPLETED', readonly=True)
WORKFLOW_EXECUTION_STATUS_FAILED = StrField(default='FAILED', readonly=True)
WORKFLOW_EXECUTION_STATUS_RUNNING = StrField(default='RUNNING', readonly=True)
WORKFLOW_EXECUTION_STATUS = ListField(default=['OK', 'COMPLETED', 'FAILED', 'RUNNING'], readonly=True)
WORKFLOW_EXECUTION_STATUS_FINISHED = ListField(default=['COMPLETED', 'FAILED'], readonly=True)
