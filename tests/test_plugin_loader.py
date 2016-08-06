import pytest
import wikischolar

def test_missing_plugin_fails_expectedly():
    with pytest.raises(wikischolar.plugins.PluginError):
        wikischolar.parser.load_plugins(['not_a_plugin'])

def test_successfully_load_a_plugin():
    plugin = wikischolar.parser.load_plugins(['edits'])[0]
    assert plugin == wikischolar.plugins.edits.edits
