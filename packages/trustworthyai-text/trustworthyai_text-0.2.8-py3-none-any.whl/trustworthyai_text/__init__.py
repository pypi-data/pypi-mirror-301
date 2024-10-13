# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

"""Trustworthy AI Text SDK package."""

from trustworthyai_text.common.constants import ModelTask
from trustworthyai_text.tai_text_insights import RAITextInsights

from .version import name, version

__name__ = name
__version__ = version

__all__ = ['ModelTask', 'RAITextInsights']
