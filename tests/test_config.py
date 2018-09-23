import pytest
import os
from importlib import reload

def test_load_config_from_env(mocker):
    mocker.patch('os.environ', {
        "CLOUDFLARE_USERNAME": "test@example.ch",
        "CLOUDFLARE_TOKEN": "xxxx",
    })
    import config
    reload(config)
    assert config.cloudflare["username"] == "test@example.ch"
    assert config.cloudflare["token"] == "xxxx"

def test_missing_env_variable(mocker):
    mocker.patch.dict('os.environ', { })

    with pytest.raises(SystemExit):
        import config
        reload(config)
        print(config)

def test_default_server_suffix(mocker):
    mocker.patch.dict('os.environ', {
        "CLOUDFLARE_USERNAME": "test@example.ch",
        "CLOUDFLARE_TOKEN": "xxxx",
    })

    import config
    reload(config)

    assert config.settings["server_prefix"] == ""

def test_server_suffix(mocker):
    mocker.patch.dict('os.environ', {
        "CLOUDFLARE_USERNAME": "test@example.ch",
        "CLOUDFLARE_TOKEN": "xxxx",
        "LSCF_SUFFIX": "server.example.ch"
    })

    import config
    reload(config)
    
    assert config.settings["server_prefix"] == "server.example.ch"


