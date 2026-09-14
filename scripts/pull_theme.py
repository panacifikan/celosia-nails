#!/usr/bin/env python3
"""Pulls every file from the live theme into the repo root, mirroring the
actual Shopify theme structure (assets/, config/, layout/, locales/,
sections/, blocks/, snippets/, templates/)."""
import base64
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from shopify_api import get_token, graphql, SHOP

THEME_GID = "gid://shopify/OnlineStoreTheme/193596719285"
REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")

QUERY = """
query themeFiles($id: ID!, $after: String) {
  theme(id: $id) {
    files(first: 50, after: $after) {
      nodes {
        filename
        contentType
        body {
          ... on OnlineStoreThemeFileBodyText { content }
          ... on OnlineStoreThemeFileBodyBase64 { contentBase64 }
          ... on OnlineStoreThemeFileBodyUrl { url }
        }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}
"""

token = get_token()
after = None
count = 0

while True:
    result = graphql(token, QUERY, {"id": THEME_GID, "after": after})
    if "errors" in result:
        print("GraphQL error:", result["errors"])
        sys.exit(1)
    files_data = result["data"]["theme"]["files"]
    for node in files_data["nodes"]:
        filename = node["filename"]
        out_path = os.path.join(REPO_ROOT, filename)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        body = node["body"]
        if "content" in body:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(body["content"])
        elif "contentBase64" in body:
            with open(out_path, "wb") as f:
                f.write(base64.b64decode(body["contentBase64"]))
        elif "url" in body:
            urllib.request.urlretrieve(body["url"], out_path)
        else:
            print("Unknown body type for", filename, body)
            continue
        count += 1
    page_info = files_data["pageInfo"]
    if not page_info["hasNextPage"]:
        break
    after = page_info["endCursor"]
    print(f"...{count} files so far")

print(f"Done. Pulled {count} files.")
