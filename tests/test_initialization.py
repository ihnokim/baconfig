from baconfig.config import Config


def test_getting_default_name():
    assert Config.get_name() == 'BACONFIG'
