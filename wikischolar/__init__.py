import logging

from .plugins import plugin
from .plugins import edits, generations, qualities, words
from . import db, parser, revisions, tasks, util

root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(logging.StreamHandler())
