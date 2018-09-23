import pytest
from client import Client
import CloudFlare
import json

def _get_zones_mock():
    return [{
        "account": {
            "id": "00000000000000000000000000000",
            "name": "admin@example.ch"
        },
        "created_on": "2016-12-12T14:12:39.347791Z",
        "development_mode": -13220610,
        "id": "d2f875556efffa09dfff47823aaae680",
        "name": "example.ch"
    }]

def _get_zone_record_list_mock():
    return [ {
        "content": "pl000.pluto.webhoster.de",
        "created_on": "2018-09-03T10:12:00.000000Z",
        "id": "8000fdd023dddebd71ffffd9ccb9bff1",
        "modified_on": "2016-09-03T10:12:00.000000Z",
        "name": "beat.server.example.ch",
        "proxiable": True,
        "proxied": False,
        "ttl": 1,
        "type": "CNAME",
        "zone_id": "d2f875556efffa09dfff47823aaae680",
        "zone_name": "example.ch"
    },
    {
        "content": "beta.server.example.ch",
        "created_on": "2018-09-03T10:12:00.000000Z",
        "id": "8067fdd023dddebd71ffffd9cdb9b001",
        "modified_on": "2016-09-03T10:12:00.000000Z",
        "name": "wiki.example.ch",
        "proxiable": True,
        "proxied": True,
        "ttl": 1,
        "type": "CNAME",
        "zone_id": "d2f875556efffa09dfff47823aaae680",
        "zone_name": "example.ch"
    },
    {
        "content": "mail.example.ch",
        "created_on": "2018-09-03T10:12:00.000000Z",
        "id": "ff67fdd023dddebd71ffffd9cdb9b001",
        "modified_on": "2016-09-03T10:12:00.000000Z",
        "name": "example.ch",
        "priority": 10,
        "proxiable": False,
        "proxied": False,
        "ttl": 1,
        "type": "CNAME",
        "zone_id": "d2f875556efffa09dfff47823aaae680",
        "zone_name": "example.ch"
    }]

def test_list_failed_zone_id_not_found(mocker):
    cf = CloudFlare.CloudFlare()
    m = mocker.patch.object(cf.zones, "get", autospec=True)
    m.return_value = []

    client = Client(cf, "server.fail.ch")

    with pytest.raises(ValueError):
        client.get_available_servers()

def test_list_available_servers(mocker):
    cf = CloudFlare.CloudFlare()
    mocker.patch.object(cf.zones, "get", autospec=True).return_value = _get_zones_mock()
    mocker.patch.object(cf.zones.dns_records, "get", autospec=True).return_value = _get_zone_record_list_mock()

    client = Client(cf, "server.example.ch")

    assert [{
        "backend": "pl000.pluto.webhoster.de",
        "name": "beat"
    }] == client.get_available_servers()