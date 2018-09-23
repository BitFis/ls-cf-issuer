# Letsencrypt Cloudflare Issuer

> lscf.sh uses needs docker to run

Script enables combining certificates issueing and cname management.
For the certificate issuing letsencript [acme.sh]
script is used and for the cname management and for the dns issuing cloudflare is used.

## Issue certificate

```bash
export CLOUDFLARE_USERNAME=xxxx@xxxx.xx
export CLOUDFLARE_TOKEN=xxxxxx

lscf.sh -d app1.example.ch -s beta.server.example.ch
```

This will 
1. create an cname record like `app1.example.ch.        CNAME  beta.server.example.ch.` in the cloudflare records.
2. extend the base certificate `example.ch.` with an wildcard entry `*.example.ch.` by calling [acme.sh] as following:
  - ```bash
    acme.sh --issue \
      -d example.ch -d *.example.ch \
      --dns dns_cf
    ```

## Customize acme.sh

All other paramters are passed to the acme.sh script, the only
parameters changed are `-d` and `--dns`, and `--issue` is always used.

```bash
lscf.sh -d app1.example.ch -s beta.server.example.ch \
  --cert-file /acme.sh/nginx/example.ch.crt
```

This will 
1. create an cname record like `app1.example.ch.        CNAME  beta.server.example.ch.` in the cloudflare records.
2. extend the base certificate `example.ch.` with an wildcard entry `*.example.ch.` by calling [acme.sh] as following:
  - ```bash
    acme.sh --issue \
      -d example.ch -d *.example.ch \
      --dns dns_cf
    ```

## Use suffix

If you follow a specific naming convention, suffix are helpful to
list available servers for cname entries.

```bash
export LSCF_SUFFIX="server.example.ch"

# list available servers, this will check dns records of cf for entries *.server.example.ch
lscf.sh -l

# same as example before
lscf.sh -d app1.example.ch -s beta
```

[acme.sh]: https://github.com/Neilpang/acme.sh