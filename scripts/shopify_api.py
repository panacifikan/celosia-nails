#!/usr/bin/env python3
"""Helper for talking to the Shopify Admin API against the dev theme.

Usage:
  python3 scripts/shopify_api.py get-asset <key> [out_path]
  python3 scripts/shopify_api.py put-asset <key> <in_path>
  python3 scripts/shopify_api.py delete-asset <key>
  python3 scripts/shopify_api.py list-assets
  python3 scripts/shopify_api.py graphql <query_file> [variables_json]
"""
import os
import sys
import json
import base64
import urllib.request
import urllib.parse

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")


def load_env():
    env = {}
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k] = v
    return env


ENV = load_env()
SHOP = ENV["SHOPIFY_SHOP"]
API_VERSION = ENV["SHOPIFY_API_VERSION"]
DEV_THEME_ID = ENV["SHOPIFY_DEV_THEME_ID"]


def request(method, url, data=None, headers=None):
    headers = headers or {}
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {url} -> {e.code}: {e.read().decode()[:500]}")


def get_token():
    url = f"https://{SHOP}/admin/oauth/access_token"
    payload = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": ENV["SHOPIFY_CLIENT_ID"],
        "client_secret": ENV["SHOPIFY_CLIENT_SECRET"],
    }).encode()
    req = urllib.request.Request(url, data=payload, method="POST",
                                  headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["access_token"]


def auth_headers(token, json_content=True):
    h = {"X-Shopify-Access-Token": token}
    if json_content:
        h["Content-Type"] = "application/json"
    return h


def graphql(token, query, variables=None):
    url = f"https://{SHOP}/admin/api/{API_VERSION}/graphql.json"
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    return request("POST", url, payload, auth_headers(token))


def get_asset(token, theme_id, key):
    url = f"https://{SHOP}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json?" + \
          urllib.parse.urlencode({"asset[key]": key})
    return request("GET", url, headers=auth_headers(token, json_content=False))


def put_asset(token, theme_id, key, value=None, attachment=None):
    url = f"https://{SHOP}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
    asset = {"key": key}
    if attachment is not None:
        asset["attachment"] = attachment
    else:
        asset["value"] = value
    return request("PUT", url, {"asset": asset}, auth_headers(token))


def delete_asset(token, theme_id, key):
    url = f"https://{SHOP}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json?" + \
          urllib.parse.urlencode({"asset[key]": key})
    req = urllib.request.Request(url, method="DELETE", headers=auth_headers(token, json_content=False))
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def list_assets(token, theme_id):
    url = f"https://{SHOP}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
    return request("GET", url, headers=auth_headers(token, json_content=False))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    token = get_token()

    if cmd == "get-asset":
        key = sys.argv[2]
        result = get_asset(token, DEV_THEME_ID, key)
        value = result.get("asset", {}).get("value")
        if value is None:
            attachment = result.get("asset", {}).get("attachment")
            if attachment:
                value_bytes = base64.b64decode(attachment)
                out_path = sys.argv[3] if len(sys.argv) > 3 else None
                if out_path:
                    with open(out_path, "wb") as f:
                        f.write(value_bytes)
                    print(f"Wrote {len(value_bytes)} bytes to {out_path}")
                else:
                    sys.stdout.buffer.write(value_bytes)
                return
            print(json.dumps(result), file=sys.stderr)
            sys.exit(1)
        out_path = sys.argv[3] if len(sys.argv) > 3 else None
        if out_path:
            with open(out_path, "w") as f:
                f.write(value)
            print(f"Wrote {len(value)} chars to {out_path}")
        else:
            print(value)

    elif cmd == "put-asset":
        key = sys.argv[2]
        in_path = sys.argv[3]
        is_binary = key.split(".")[-1].lower() in (
            "png", "jpg", "jpeg", "gif", "webp", "woff", "woff2", "ttf", "otf", "ico"
        )
        if is_binary:
            with open(in_path, "rb") as f:
                attachment = base64.b64encode(f.read()).decode()
            result = put_asset(token, DEV_THEME_ID, key, attachment=attachment)
        else:
            with open(in_path, "r") as f:
                value = f.read()
            result = put_asset(token, DEV_THEME_ID, key, value=value)
        if "errors" in result or ("asset" not in result):
            print(json.dumps(result), file=sys.stderr)
            sys.exit(1)
        print(f"OK: {key}")

    elif cmd == "delete-asset":
        key = sys.argv[2]
        result = delete_asset(token, DEV_THEME_ID, key)
        print(json.dumps(result))

    elif cmd == "list-assets":
        result = list_assets(token, DEV_THEME_ID)
        for a in sorted(result.get("assets", []), key=lambda a: a["key"]):
            print(a["key"])

    elif cmd == "graphql":
        query_file = sys.argv[2]
        variables = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
        with open(query_file) as f:
            query = f.read()
        result = graphql(token, query, variables)
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
