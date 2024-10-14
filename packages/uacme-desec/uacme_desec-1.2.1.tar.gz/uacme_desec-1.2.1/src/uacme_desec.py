"""Hook script for UACME that creates and removes validation records on deSEC"""
# SPDX-FileCopyrightText: 2024 OpenBit
# SPDX-FileContributor: Hugo Rodrigues
#
# SPDX-License-Identifier: MIT

# Based on https://git.sr.ht/~jacksonchen666/uacme-desec-hook/tree/main/item/uacme-desec-hook.sh

import contextlib
import http.client
import json
import logging
import logging.handlers
import pathlib
import os
import sys
import time

# Setp logging
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(logging.StreamHandler())
if os.environ.get("DESEC_SYSLOG", None):
    SYSLOG = logging.handlers.SysLogHandler(address=os.environ["DESEC_SYSLOG"])
    SYSLOG.setFormatter(logging.Formatter("desec: %(message)s"))
    LOGGER.addHandler(SYSLOG)

# Validate token
if os.environ.get("DESEC_TOKEN", None) is None:
    LOGGER.error("DESEC_TOKEN not set")
    sys.exit(1)


# Send a HTTPS REST request
@contextlib.contextmanager
def request(method, host, endpoint, data=None, headers=None):
    """
    Sends a HTTPS request

    args:
        method: HTTP method
        host: Host to connect
        endpoint: API endpoint without the initial /api
        data: Optional body for the request
        headers: Optional headers to send

    returns: context manager with http.client.HTTPResponse
    """
    if headers is None:
        headers = {}
    headers["Content-Type"] = "application/json"

    if isinstance(data, dict):
        data = json.dumps(data).encode("ascii")

    cn = http.client.HTTPSConnection(host)
    try:
        cn.request(method, endpoint, headers=headers, body=data)
        res = cn.getresponse()
        yield res
    except Exception as err:
        LOGGER.error(err)
        raise
    finally:
        cn.close()


# Send a HTTPS request to deSEC
@contextlib.contextmanager
def desec(method, endpoint, data=None):
    """
    Sends a request to deSEC API

    args:
        method: HTTP method
        endpoint: API endpoint without the initial /api
        data: Optional body for the request

    returns: context manager with http.client.HTTPResponse
    """

    with request(method, os.environ.get("DESEC_HOST", "desec.io"), f"/api{endpoint}", headers={"Authorization": f"Token {os.environ['DESEC_TOKEN']}"}, data=data) as res:
        if res.status == 401:
            raise ValueError("Invalid DESEC_TOKEN")
        yield res


def validate_propagation(domain, subname, auth):
    """Use Google DNS to check if the record exists and is valid"""
    google = {}
    while google.get("Status", None) in (None, 3):
        if google.get("Status", None) is None:
            time.sleep(60)
        else:
            time.sleep(10)
        with request("GET", "dns.google.com", f"/resolve?name={subname}.{domain}&type=TXT") as res:
            google = json.loads(res.read().decode())

    if google["Status"] > 0:
        errors = ""
        for error in google.get("extended_dns_errors"):
            errors += f"    {error.get('info_code', 'NA')}: {error.get('extra_text', 'NA')}\n"
        LOGGER.error("Unable to validate DNS records\n    %s\n%s", google.get("Comment", "<No information from Google>"), errors)
        return False
    if not any(auth == ans["data"] for ans in google["Answer"]):
        LOGGER.error("Didn't find any record that matches our validation token")
        return False
    return True


# Create record
def create(domain, subname, auth):
    """Creates the _acme_challenge record"""
    with desec("POST", f"/v1/domains/{domain}/rrsets/", data={"subname": subname,
                                                              "type": "TXT",
                                                              "ttl": "3600",
                                                              "records": [f'"{auth}"']}) as response:
        data = None
        if response.headers["Content-Type"] == "application/json":
            try:
                data = json.loads(response.read().decode())
            except json.decoder.JSONDecodeError:
                data = None
                LOGGER.warning("Unable to parse deSEC response")
        if response.status != 201:
            msg = f"Unable to create record.\nError {response.status}:"
            if data:
                for error, messages in data.items():
                    msg += f"\n    {error}:"
                    if isinstance(messages, list):
                        for message in messages:
                            msg += f"\n        {message}"
                    else:
                        msg += f" {messages}"
            LOGGER.error(msg)
            return 1

    # Wait for DNS propagation
    # DNS propagation at desec.io is slow, taking up to a minute:
    # https://talk.desec.io/t/global-record-propagation-issues/332/2
    #   https://github.com/PowerDNS/pdns/issues/10867
    #       (https://github.com/desec-io/certbot-dns-desec/pull/9)
    if not validate_propagation(domain, subname, auth):
        delete(domain, subname)
        return 1
    LOGGER.info("Created record")
    return 0


# Delete record
def delete(domain, subname):
    """Deletes the record created by create function"""
    with desec("DELETE", f"/v1/domains/{domain}/rrsets/{subname}/TXT/") as response:
        data = None
        if response.headers["Content-Type"] == "application/json":
            try:
                data = json.loads(response.read().decode())
            except json.decoder.JSONDecodeError:
                data = None
                LOGGER.warning("Unable to parse deSEC response")
        if response.status != 204:
            msg = f"Unable to delete record.\nError {response.status}:"
            if data:
                for error, messages in data.items():
                    msg += f"\n    {error}:"
                    if isinstance(messages, list):
                        for message in messages:
                            msg += f"\n        {message}"
                    else:
                        msg += f" {messages}"
            LOGGER.error(msg)
            return 1
        LOGGER.info("Deleted record")
        return 0


def main():
    """main"""

    # Validate input
    if len(sys.argv) < 6:
        LOGGER.error("Usage: %s method type ident auth", pathlib.Path(__file__).name)
        sys.exit(1)

    method = sys.argv[1]
    tpe = sys.argv[2]
    ident = sys.argv[3]
    # token = sys.argv[4]
    auth = sys.argv[5]
    desec_domain = os.environ.get("DESEC_DOMAIN", None)

    if desec_domain is None:
        desec_domain = ".".join(ident.split(".")[-2:])

    if os.environ.get("DESEC_ALIAS", None):
        subname = os.environ['DESEC_ALIAS']
    else:
        subname = f"_acme_challenge.{ident}".replace(f".{desec_domain}", "")

    # Parse and call above functions
    result = 0
    match tpe:
        case "dns-01":
            match method:
                case "begin":
                    result = create(desec_domain, subname, auth)
                case "done":
                    result = delete(desec_domain, subname)
                case "failed":
                    result = delete(desec_domain, subname)
                case _:
                    LOGGER.error("Invalid method %s", method)
        case _:
            LOGGER.error("Invalid type %s", tpe)
            sys.exit(1)
    sys.exit(result)


if __name__ == "__main__":
    main()
