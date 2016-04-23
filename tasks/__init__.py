#!/usr/bin/env python
from invoke import Collection

from .get import get
from .article_quality import article_quality
from .publish import publish

namespace = Collection(get, article_quality, publish)
