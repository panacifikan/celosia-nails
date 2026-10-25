#!/usr/bin/env bash
# Run Shopify CLI against the store using the app credentials in .env.
#
# Fetches a fresh 24h Admin API token via the client credentials grant and
# passes it to the CLI, so no `shopify auth login` browser flow is needed.
#
# Usage:
#   scripts/shopify-cli.sh theme list
#   scripts/shopify-cli.sh theme pull --theme 193596719285
#   scripts/shopify-cli.sh theme dev --theme 193596719285
#   scripts/shopify-cli.sh theme push --unpublished
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
set -a
# shellcheck disable=SC1091
source "$ROOT/.env"
set +a

TOKEN="$(curl -sf -X POST "https://$SHOPIFY_SHOP/admin/oauth/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=client_credentials" \
  --data-urlencode "client_id=$SHOPIFY_CLIENT_ID" \
  --data-urlencode "client_secret=$SHOPIFY_CLIENT_SECRET" \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')"

export SHOPIFY_FLAG_STORE="$SHOPIFY_SHOP"
export SHOPIFY_CLI_THEME_TOKEN="$TOKEN"
cd "$ROOT"
exec shopify "$@"
