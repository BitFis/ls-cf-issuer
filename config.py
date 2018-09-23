import os
import sys

class Env:

    _errors = []

    @staticmethod
    def get_errors():
        return Env._errors

    @staticmethod
    def _get_default(env, default, required):
        if required:
            Env._errors.append("'$" + env + "' is not defined in the environment variables!")
        else:
            return default

    @staticmethod
    def get_env(env, default="", required=False):
        try:
            return os.environ[env]
        except KeyError:
            return Env._get_default(env, default, required)

cloudflare = {
    "username": Env.get_env("CLOUDFLARE_USERNAME", required=True),
    "token": Env.get_env("CLOUDFLARE_TOKEN", required=True)
}

settings = {
    "server_prefix": Env.get_env("LSCF_SUFFIX")
}

if len(Env.get_errors()) > 0:
    sys.stderr.write('\n'.join(str(x) for x in Env.get_errors()) )
    sys.exit(1)
