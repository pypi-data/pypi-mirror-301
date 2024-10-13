# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

"""Trustworthy AI Vision SDK package."""

from trustworthyai_vision.common.constants import ModelTask
from trustworthyai_vision.tai_vision_insights import RAIVisionInsights

from .version import name, version

__name__ = name
__version__ = version

__all__ = ['ModelTask', 'RAIVisionInsights']
