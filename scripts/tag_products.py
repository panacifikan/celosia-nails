#!/usr/bin/env python3
"""Applies vibe + label tags to the 12 Celosia products, per the design handoff
product data table."""
import subprocess
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from shopify_api import get_token, graphql

PRODUCTS = {
    "blushing-royalty": {"id": "gid://shopify/Product/10438977749173", "vibe": "vibe-blush-pink", "labels": ["label-bestseller", "featured-hero"]},
    "soft-girl": {"id": "gid://shopify/Product/10438981484725", "vibe": "vibe-soft-nude", "labels": ["label-everyday"]},
    "icy-princess": {"id": "gid://shopify/Product/10438979551413", "vibe": "vibe-icy-chrome", "labels": ["label-trending"]},
    "red-theory": {"id": "gid://shopify/Product/10438981386421", "vibe": "vibe-bold-red", "labels": ["label-bestseller"]},
    "whimsicle": {"id": "gid://shopify/Product/10438982795445", "vibe": "vibe-lilac-pearl", "labels": ["label-new"]},
    "statement": {"id": "gid://shopify/Product/10438981517493", "vibe": "vibe-statement", "labels": ["label-editors-pick"]},
    "rose-garden": {"id": "gid://shopify/Product/10438981419189", "vibe": "vibe-bold-red", "labels": ["label-restocked"]},
    "hawaii": {"id": "gid://shopify/Product/10438979289269", "vibe": "vibe-icy-chrome", "labels": ["label-summer"]},
    "icy-queen": {"id": "gid://shopify/Product/10438979616949", "vibe": "vibe-icy-chrome", "labels": ["label-low-stock"]},
    "girly": {"id": "gid://shopify/Product/10438979027125", "vibe": "vibe-blush-pink", "labels": ["label-everyday"]},
    "date-night": {"id": "gid://shopify/Product/10438977781941", "vibe": "vibe-statement", "labels": ["label-trending"]},
    "out-of-this-world": {"id": "gid://shopify/Product/10438980272309", "vibe": "vibe-statement", "labels": ["label-new"]},
}

MUTATION = """
mutation tagsAdd($id: ID!, $tags: [String!]!) {
  tagsAdd(id: $id, tags: $tags) {
    node { ... on Product { id tags } }
    userErrors { field message }
  }
}
"""

token = get_token()
for handle, info in PRODUCTS.items():
    tags = [info["vibe"]] + info["labels"]
    result = graphql(token, MUTATION, {"id": info["id"], "tags": tags})
    errors = result.get("data", {}).get("tagsAdd", {}).get("userErrors", [])
    if errors:
        print(f"FAILED {handle}: {errors}")
    else:
        node = result["data"]["tagsAdd"]["node"]
        print(f"OK {handle}: {node['tags']}")
