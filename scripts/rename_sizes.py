#!/usr/bin/env python3
"""Renames the Size option values from XS/S/M/L to full words on every product."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from shopify_api import get_token, graphql

RENAME = {"XS": "Extra small", "S": "Small", "M": "Medium", "L": "Large"}

LIST_QUERY = """
{ products(first: 20) {
    nodes {
      id
      handle
      options { id name optionValues { id name } }
    }
  }
}
"""

UPDATE_MUTATION = """
mutation productOptionUpdate($productId: ID!, $option: OptionUpdateInput!, $optionValuesToUpdate: [OptionValueUpdateInput!]) {
  productOptionUpdate(productId: $productId, option: $option, optionValuesToUpdate: $optionValuesToUpdate) {
    userErrors { field message }
  }
}
"""

token = get_token()
result = graphql(token, LIST_QUERY)
products = result["data"]["products"]["nodes"]

for p in products:
    for opt in p["options"]:
        if opt["name"] != "Size":
            continue
        updates = []
        for v in opt["optionValues"]:
            if v["name"] in RENAME:
                updates.append({"id": v["id"], "name": RENAME[v["name"]]})
        if not updates:
            print(f"skip {p['handle']}: already renamed or no match")
            continue
        variables = {
            "productId": p["id"],
            "option": {"id": opt["id"]},
            "optionValuesToUpdate": updates,
        }
        res = graphql(token, UPDATE_MUTATION, variables)
        errors = res.get("data", {}).get("productOptionUpdate", {}).get("userErrors", [])
        if errors:
            print(f"FAILED {p['handle']}: {errors}")
        else:
            print(f"OK {p['handle']}")
