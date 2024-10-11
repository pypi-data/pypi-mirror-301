"""
Moodle API Client

Powered by `tiny-api-client`
"""

import logging
from .api import MoodleLogin, MoodleSession

__all__ = ['MoodleLogin', 'MoodleSession']

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
