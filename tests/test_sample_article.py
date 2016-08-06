"""Test wikischolar commands for a sample article.

Warning! These tests are run live against the Wikipedia servers.
TODO: Swap out real requests with betamaxx
"""
import wikischolar


def test_getting_revisions():
    revisions = wikischolar.revisions.get_revisions('Splendid fairywren')
    assert 'title' in revisions
