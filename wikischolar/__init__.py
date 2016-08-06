import logging

from .plugins import plugin
from .plugins import edits, generations, qualities, words
from . import db, parser, revisions, tasks, util

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
