# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

"""Trustworthy AI SDK package."""

# ModelTask is only imported for backwards compatibility
from affectlog_utils.models import ModelTask
from trustworthyai.modelanalysis import ModelAnalysis
from trustworthyai.tai_insights import RAIInsights

from .__version__ import version
from .feature_metadata import FeatureMetadata

__version__ = version

__all__ = ['ModelAnalysis', 'ModelTask', 'RAIInsights', 'FeatureMetadata']
