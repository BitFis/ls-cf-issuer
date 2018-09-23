import CloudFlare
import json

class Client:
    """
    cf CloudFlare instance
    """
    def __init__(self, cf, server_prefix):
        self._server_prefix = server_prefix
        self._cf = cf
        self._primary = self._extract_primary()

    def _extract_primary(self):
        return '.'.join(self._server_prefix.split('.')[-2:])

    """
    add domain as cname with the target given by server combined with server_prefix
    """
    def register(self, domain, server):
        zones = self._cf.zones.get(params={"name": self._primary})
        print(zones)
        print(json.dumps(zones, indent=2, sort_keys=True))
#        raise NotImplementedError()

    """
    remove the domain from the cloudflare dns record
    """
    def unregister(self, domain):
        raise NotImplementedError()

    def _get_zone_id(self):
        zones = self._cf.zones.get(params={"name": self._primary})
        if len(zones) > 0:
            return zones[0]["id"]
        else:
            raise ValueError("no zone found for " + self._server_prefix)

    """
    return a list of available servers only if server_prefix is
    set, else the list will be empty
    """
    def get_available_servers(self):
        def extract_name(a):
            return {
                'name': a['name'].replace('.' + self._server_prefix, ''),
                'backend': a['content']
            }
        res = self._cf.zones.dns_records.get(self._get_zone_id())
        print(json.dumps(res, indent=2, sort_keys=True) )
        return [extract_name(r) for r in res if r['name'].endswith(self._server_prefix)]