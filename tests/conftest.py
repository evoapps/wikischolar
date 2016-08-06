import pytest
import betamax
import unipath


CASSETTES = unipath.Path('tests/cassettes/')

if not CASSETTES.isdir():
    CASSETTES.mkdir()

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'tests/cassettes/'
    config.default_cassette_options['record_mode'] = 'new_episodes'


@pytest.fixture
def cleanup_pywikibot(request):
    trash = ['apicache/', 'throttle.ctrl']
    def cleanup():
        for item in trash:
            x = unipath.Path(item)
            if x.isdir():
                x.rmtree()
            elif x.exists():
                x.remove()
    request.addfinalizer(cleanup)
