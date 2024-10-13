# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

"""Implementation of Model Analysis API."""

# ModelTask is only imported for backwards compatibility.
from affectlog_utils.models import ModelTask
from trustworthyai.tai_insights.tai_insights import RAIInsights

__all__ = ['ModelTask', 'RAIInsights']
