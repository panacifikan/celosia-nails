#!/usr/bin/env python3
"""Rewrites config/settings_data.json 'current' block with the Celosia Nails
design tokens (colors + fonts + radii) from the design handoff README."""
import json

IN_PATH = "/tmp/dev_settings_data.json"
OUT_PATH = "/tmp/dev_settings_data.new.json"

PLUM_INK = "#241519"
PETAL_WHITE = "#FBF5F2"
PORCELAIN = "#FFFFFF"
BLUSH_WASH = "#F6E3E4"
ROSE_QUARTZ = "#E3A7B1"
CHERRY = "#8E1F2B"
PINK_ICING = "#F2D2D7"
MUTED_INK = "#5F4A4F"

def hexa(hex6, alpha_pct):
    # alpha_pct 0-100 -> two-hex-digit suffix, Shopify color settings accept #RRGGBBAA
    v = round(alpha_pct / 100 * 255)
    return f"{hex6}{v:02x}"

def light_scheme(background):
    return {
        "settings": {
            "background": background,
            "foreground_heading": PLUM_INK,
            "foreground": hexa(MUTED_INK, 100),
            "primary": CHERRY,
            "primary_hover": "#6E1721",
            "border": hexa(PLUM_INK, 12),
            "shadow": PLUM_INK,
            "primary_button_background": CHERRY,
            "primary_button_text": PETAL_WHITE,
            "primary_button_border": CHERRY,
            "primary_button_hover_background": "#6E1721",
            "primary_button_hover_text": PETAL_WHITE,
            "primary_button_hover_border": "#6E1721",
            "secondary_button_background": "rgba(0,0,0,0)",
            "secondary_button_text": PLUM_INK,
            "secondary_button_border": hexa(PLUM_INK, 25),
            "secondary_button_hover_background": hexa(PLUM_INK, 5),
            "secondary_button_hover_text": PLUM_INK,
            "secondary_button_hover_border": PLUM_INK,
            "input_background": PORCELAIN,
            "input_text_color": PLUM_INK,
            "input_border_color": hexa(PLUM_INK, 18),
            "input_hover_background": hexa(PLUM_INK, 4),
            "variant_background_color": PORCELAIN,
            "variant_text_color": PLUM_INK,
            "variant_border_color": hexa(PLUM_INK, 18),
            "variant_hover_background_color": BLUSH_WASH,
            "variant_hover_text_color": PLUM_INK,
            "variant_hover_border_color": CHERRY,
            "selected_variant_background_color": PLUM_INK,
            "selected_variant_text_color": PETAL_WHITE,
            "selected_variant_border_color": PLUM_INK,
            "selected_variant_hover_background_color": "#3A262C",
            "selected_variant_hover_text_color": PETAL_WHITE,
            "selected_variant_hover_border_color": "#3A262C",
        }
    }

def dark_scheme(background):
    return {
        "settings": {
            "background": background,
            "foreground_heading": PETAL_WHITE,
            "foreground": hexa("#BBA4A6", 100),
            "primary": ROSE_QUARTZ,
            "primary_hover": PINK_ICING,
            "border": hexa(PETAL_WHITE, 14),
            "shadow": "#000000",
            "primary_button_background": PINK_ICING,
            "primary_button_text": PLUM_INK,
            "primary_button_border": PINK_ICING,
            "primary_button_hover_background": PETAL_WHITE,
            "primary_button_hover_text": PLUM_INK,
            "primary_button_hover_border": PETAL_WHITE,
            "secondary_button_background": "rgba(0,0,0,0)",
            "secondary_button_text": PETAL_WHITE,
            "secondary_button_border": hexa(PETAL_WHITE, 40),
            "secondary_button_hover_background": hexa(PETAL_WHITE, 10),
            "secondary_button_hover_text": PETAL_WHITE,
            "secondary_button_hover_border": PETAL_WHITE,
            "input_background": background,
            "input_text_color": PETAL_WHITE,
            "input_border_color": hexa(PETAL_WHITE, 30),
            "input_hover_background": hexa(PETAL_WHITE, 8),
            "variant_background_color": PETAL_WHITE,
            "variant_text_color": PLUM_INK,
            "variant_border_color": hexa(PLUM_INK, 18),
            "variant_hover_background_color": BLUSH_WASH,
            "variant_hover_text_color": PLUM_INK,
            "variant_hover_border_color": CHERRY,
            "selected_variant_background_color": CHERRY,
            "selected_variant_text_color": PETAL_WHITE,
            "selected_variant_border_color": CHERRY,
            "selected_variant_hover_background_color": "#6E1721",
            "selected_variant_hover_text_color": PETAL_WHITE,
            "selected_variant_hover_border_color": "#6E1721",
        }
    }

def overlay_scheme():
    # transparent-bg scheme, used for text/badges laid over photography
    return {
        "settings": {
            "background": "rgba(0,0,0,0)",
            "foreground_heading": PETAL_WHITE,
            "foreground": PETAL_WHITE,
            "primary": PETAL_WHITE,
            "primary_hover": PINK_ICING,
            "border": hexa(PETAL_WHITE, 40),
            "shadow": PLUM_INK,
            "primary_button_background": PETAL_WHITE,
            "primary_button_text": PLUM_INK,
            "primary_button_border": PETAL_WHITE,
            "primary_button_hover_background": PINK_ICING,
            "primary_button_hover_text": PLUM_INK,
            "primary_button_hover_border": PINK_ICING,
            "secondary_button_background": "rgba(0,0,0,0)",
            "secondary_button_text": PETAL_WHITE,
            "secondary_button_border": PETAL_WHITE,
            "secondary_button_hover_background": hexa(PETAL_WHITE, 10),
            "secondary_button_hover_text": PETAL_WHITE,
            "secondary_button_hover_border": PETAL_WHITE,
            "input_background": PETAL_WHITE,
            "input_text_color": PLUM_INK,
            "input_border_color": hexa(PLUM_INK, 18),
            "input_hover_background": BLUSH_WASH,
            "variant_background_color": PETAL_WHITE,
            "variant_text_color": PLUM_INK,
            "variant_border_color": hexa(PLUM_INK, 18),
            "variant_hover_background_color": BLUSH_WASH,
            "variant_hover_text_color": PLUM_INK,
            "variant_hover_border_color": CHERRY,
            "selected_variant_background_color": PLUM_INK,
            "selected_variant_text_color": PETAL_WHITE,
            "selected_variant_border_color": PLUM_INK,
            "selected_variant_hover_background_color": "#3A262C",
            "selected_variant_hover_text_color": PETAL_WHITE,
            "selected_variant_hover_border_color": "#3A262C",
        }
    }

with open(IN_PATH) as f:
    data = json.load(f)

cur = data["current"]

# --- Fonts ---
cur["type_body_font"] = "jost_n4"
cur["type_subheading_font"] = "jost_n5"
cur["type_heading_font"] = "instrument_serif_n4"
cur["type_accent_font"] = "instrument_serif_n4"

# --- Radii (from README spacing/radius table) ---
# Note: these settings are 0-100/0-32/0-16 scales (effectively px, clamped to
# each component's own max), not literal css px matching the README 1:1.
# Button radius at its max (100) already renders as a full pill at normal
# button heights, matching the README's "pills and buttons: 999px" rule.
cur["primary_button_border_width"] = 0
cur["button_border_radius_primary"] = 100
cur["secondary_button_border_width"] = 1
cur["button_border_radius_secondary"] = 100
cur["inputs_border_radius"] = 32
cur["input_border_width"] = 1
cur["popover_border_radius"] = 16
cur["product_corner_radius"] = 20
cur["card_corner_radius"] = 16
cur["variant_button_radius"] = 14
cur["variant_button_border_width"] = 1
cur["badge_corner_radius"] = 100
cur["badge_sale_color_scheme"] = "scheme-5"
cur["badge_sold_out_color_scheme"] = "scheme-2"

# --- Color schemes ---
cur["color_schemes"] = {
    "scheme-1": light_scheme(PETAL_WHITE),
    "scheme-2": light_scheme(BLUSH_WASH),
    "scheme-3": light_scheme(PORCELAIN),
    "scheme-4": light_scheme(BLUSH_WASH),
    "scheme-5": dark_scheme(PLUM_INK),
    "scheme-6": overlay_scheme(),
    "scheme-58084d4c-a86e-4d0a-855e-a0966e5043f7": light_scheme(PORCELAIN),
}

with open(OUT_PATH, "w") as f:
    json.dump(data, f, indent=2)

print("Wrote", OUT_PATH)
