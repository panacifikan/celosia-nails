#!/usr/bin/env python3
"""Builds templates/product.json by extending the live PDP block tree with:
star rating, find-my-size link, in-the-box note, 6-row accordion, sticky add
to cart, an on-real-hands section, a reviews band, related products retitle,
and a closing sizing band."""
import json

with open("/tmp/live_product_template.json") as f:
    data = json.load(f)

main = data["sections"]["main"]
main["settings"]["enable_sticky_add_to_cart"] = True

details = main["blocks"]["product-details"]
blocks = details["blocks"]
order = details["block_order"]

# --- Star rating text block, appended inside the header group (after price) ---
header_group = blocks["group_icgrde"]
header_group["blocks"]["text_rating"] = {
    "type": "text",
    "name": "Rating (placeholder)",
    "settings": {
        "text": "<p>&#9733;&#9733;&#9733;&#9733;&#9733; 4.9 average rating</p>",
        "width": "100%",
        "max_width": "normal",
        "alignment": "left",
        "type_preset": "paragraph",
        "font": "var(--font-body--family)",
        "font_size": "0.8125rem",
        "line_height": "normal",
        "letter_spacing": "normal",
        "case": "none",
        "wrap": "pretty",
        "color": "#8E1F2B",
        "background": False,
        "background_color": "#00000026",
        "corner_radius": 0,
        "padding-block-start": 4,
        "padding-block-end": 0,
        "padding-inline-start": 0,
        "padding-inline-end": 0,
    },
    "blocks": {},
}
header_group["block_order"].append("text_rating")

# --- Find my size link, inserted right after the variant picker ---
blocks["text_find_my_size"] = {
    "type": "text",
    "name": "Find my size link",
    "settings": {
        "text": "<p><a href=\"#sizing-guide-accordion\">Find my size</a></p>",
        "width": "100%",
        "max_width": "normal",
        "alignment": "right",
        "type_preset": "paragraph",
        "font": "var(--font-body--family)",
        "font_size": "0.8125rem",
        "line_height": "normal",
        "letter_spacing": "normal",
        "case": "none",
        "wrap": "pretty",
        "color": "#8E1F2B",
        "background": False,
        "background_color": "#00000026",
        "corner_radius": 0,
        "padding-block-start": 0,
        "padding-block-end": 4,
        "padding-inline-start": 0,
        "padding-inline-end": 0,
    },
    "blocks": {},
}

# --- In-the-box note, a Blush Wash group with a text child ---
blocks["group_in_the_box"] = {
    "type": "group",
    "name": "In the box",
    "settings": {
        "content_direction": "column",
        "vertical_on_mobile": True,
        "horizontal_alignment": "flex-start",
        "vertical_alignment": "center",
        "align_baseline": False,
        "horizontal_alignment_flex_direction_column": "flex-start",
        "vertical_alignment_flex_direction_column": "center",
        "gap": 4,
        "width": "fill",
        "custom_width": 100,
        "width_mobile": "fill",
        "custom_width_mobile": 100,
        "height": "fit",
        "custom_height": 100,
        "inherit_color_scheme": False,
        "color_scheme": "scheme-2",
        "background_media": "none",
        "video_position": "cover",
        "background_image_position": "cover",
        "border": "none",
        "border_width": 1,
        "border_opacity": 100,
        "border_radius": 16,
        "toggle_overlay": False,
        "overlay_color": "#00000026",
        "overlay_style": "solid",
        "gradient_direction": "to top",
        "padding-block-start": 16,
        "padding-block-end": 16,
        "padding-inline-start": 16,
        "padding-inline-end": 16,
    },
    "blocks": {
        "text_box_note": {
            "type": "text",
            "settings": {
                "text": "<p><strong>In the box:</strong> one full set in your size, plus nail glue, adhesive tabs, a mini buffer, wooden cuticle stick and prep wipe. Dispatched within 1&ndash;2 business days.</p>",
                "width": "100%",
                "max_width": "normal",
                "alignment": "left",
                "type_preset": "paragraph",
                "font": "var(--font-body--family)",
                "font_size": "0.875rem",
                "line_height": "normal",
                "letter_spacing": "normal",
                "case": "none",
                "wrap": "pretty",
                "color": "",
                "background": False,
                "background_color": "#00000026",
                "corner_radius": 0,
                "padding-block-start": 0,
                "padding-block-end": 0,
                "padding-inline-start": 0,
                "padding-inline-end": 0,
            },
            "blocks": {},
        }
    },
    "block_order": ["text_box_note"],
}

# --- Accordion with six rows ---
STATIC_APPLY_STEPS = {
    "step_1": "Wash and dry your hands. Push back cuticles and lightly buff the surface of your natural nails.",
    "step_2": "Wipe each nail with the included prep wipe so the glue grips.",
    "step_3": "Add a small dot of glue to your nail and a thin layer to the back of the press-on.",
    "step_4": "Press the nail down from cuticle to tip and hold for 15–30 seconds.",
    "step_5": "Wait at least an hour before any water exposure so the glue can cure.",
}

def text_block(html, preset="paragraph", size="0.875rem"):
    return {
        "type": "text",
        "settings": {
            "text": html,
            "width": "100%",
            "max_width": "normal",
            "alignment": "left",
            "type_preset": preset,
            "font": "var(--font-body--family)",
            "font_size": size,
            "line_height": "normal",
            "letter_spacing": "normal",
            "case": "none",
            "wrap": "pretty",
            "color": "",
            "background": False,
            "background_color": "#00000026",
            "corner_radius": 0,
            "padding-block-start": 0,
            "padding-block-end": 0,
            "padding-inline-start": 0,
            "padding-inline-end": 0,
        },
        "blocks": {},
    }

accordion_rows = {
    "row_design": {
        "type": "_accordion-row",
        "settings": {"heading": "Design & materials", "open_by_default": True, "icon": "none"},
        "blocks": {
            "product_intro": {"type": "celosia-product-intro", "settings": {}, "blocks": {}}
        },
        "block_order": ["product_intro"],
    },
    "row_box": {
        "type": "_accordion-row",
        "settings": {"heading": "What's in the box", "open_by_default": False, "icon": "none"},
        "blocks": {
            "text_box": text_block(
                "<p>One full set of press-on nails in your chosen size, nail glue, adhesive tabs, a mini buffer, a wooden cuticle stick and a prep wipe.</p>"
            )
        },
        "block_order": ["text_box"],
    },
    "row_sizing": {
        "type": "_accordion-row",
        "settings": {"heading": "Sizing guide", "open_by_default": False, "icon": "none"},
        "blocks": {
            "sizing_table": {
                "type": "celosia-sizing-table",
                "settings": {"xs_range": "", "s_range": "", "m_range": "", "l_range": ""},
                "blocks": {},
            }
        },
        "block_order": ["sizing_table"],
    },
    "row_apply": {
        "type": "_accordion-row",
        "settings": {"heading": "How to apply", "open_by_default": False, "icon": "none"},
        "blocks": {
            "text_apply_intro": text_block(
                "<p>Each set comes with both nail glue and adhesive tabs. This is the long-wear glue method, up to two weeks.</p>"
            ),
            "apply_steps": {
                "type": "celosia-apply-steps",
                "settings": STATIC_APPLY_STEPS,
                "blocks": {},
            },
        },
        "block_order": ["text_apply_intro", "apply_steps"],
    },
    "row_wear": {
        "type": "_accordion-row",
        "settings": {"heading": "Wear, removal & re-wear", "open_by_default": False, "icon": "none"},
        "blocks": {
            "text_wear": text_block(
                "<p>Wear gloves for cleaning, dishes and gardening, and pat your hands dry rather than rubbing. Avoid long hot showers in the first 24 hours. If a nail lifts, re-glue it from underneath rather than pressing it back down.</p>"
                "<p><strong>Removal:</strong> soak your hands in warm, soapy water for 10&ndash;15 minutes, then gently lift each nail from the cuticle edge with the included cuticle stick. Each set can be re-worn once removed cleanly.</p>"
            )
        },
        "block_order": ["text_wear"],
    },
    "row_shipping": {
        "type": "_accordion-row",
        "settings": {"heading": "Shipping & returns", "open_by_default": False, "icon": "none"},
        "blocks": {
            "text_shipping": text_block(
                "<p>Dispatched within 1&ndash;2 business days. Free express shipping on orders over $120, Australia wide.</p>"
                "<p>Returns are accepted within 14 days on unopened sets.</p>"
            )
        },
        "block_order": ["text_shipping"],
    },
}

blocks["accordion_main"] = {
    "type": "accordion",
    "name": "Product details accordion",
    "settings": {
        "icon": "plus",
        "dividers": "all",
        "type_preset": "paragraph",
        "inherit_color_scheme": True,
        "color_scheme": "",
        "border": "none",
        "border_width": 1,
        "border_opacity": 100,
        "border_radius": 0,
        "padding-block-start": 0,
        "padding-block-end": 0,
        "padding-inline-start": 0,
        "padding-inline-end": 0,
    },
    "blocks": accordion_rows,
    "block_order": list(accordion_rows.keys()),
}

# --- Assemble the new block order: keep title/price/rating group, divider,
# variant picker, find-my-size link, buy buttons, in-the-box note, accordion.
# Drop the old flat description block (text_aEtTtq) since its content now
# lives inside the "Design & materials" accordion row. ---
new_order = []
for key in order:
    new_order.append(key)
    if key == "variant_picker_R3rGDr":
        new_order.append("text_find_my_size")
    if key == "buy_buttons_eYQEYi":
        new_order.append("group_in_the_box")
        new_order.append("accordion_main")

new_order = [k for k in new_order if k != "text_aEtTtq"]
del blocks["text_aEtTtq"]

details["block_order"] = new_order

# --- Retitle related products heading ---
rec_section = data["sections"]["product_recommendations_qggXJq"]
rec_section["blocks"]["text_cbcgyb"]["settings"]["text"] = "<h3>Wears well with</h3>"

# --- New top-level sections: on-real-hands, reviews band, sizing band ---
data["sections"]["celosia_on_real_hands"] = {
    "type": "celosia-on-real-hands",
    "settings": {"label": "On real hands", "color_scheme": "scheme-1"},
}

data["sections"]["celosia_reviews_band"] = {
    "type": "celosia-social-proof",
    "settings": {"average_rating": "4.9", "show_bars": True, "show_ugc": False, "color_scheme": "scheme-2"},
    "blocks": {
        "bar_5": {"type": "rating_bar", "settings": {"label": "5 stars", "percent": 92}},
        "bar_4": {"type": "rating_bar", "settings": {"label": "4 stars", "percent": 6}},
        "bar_3": {"type": "rating_bar", "settings": {"label": "3 stars", "percent": 2}},
        "review_1": {"type": "review", "settings": {"quote": "Held up through a full week of dishes and the gym, no lifting.", "name": "Jess T.", "meta": "Worn 9 days", "fallback_avatar": "celosia-ugc1.png"}},
        "review_2": {"type": "review", "settings": {"quote": "Ten minutes and they looked salon-done.", "name": "Priya N.", "meta": "Worn 12 days", "fallback_avatar": "celosia-ugc4.png"}},
    },
    "block_order": ["bar_5", "bar_4", "bar_3", "review_1", "review_2"],
}

data["sections"]["celosia_sizing_band"] = {
    "type": "celosia-sizing-band",
    "settings": {
        "heading": "Not sure of your size?",
        "body": "Check the sizing guide above before you order — it only takes a minute.",
        "link": "#sizing-guide-accordion",
        "link_label": "Sizing guide",
    },
}

data["order"] = [
    "main",
    "celosia_on_real_hands",
    "celosia_reviews_band",
    "product_recommendations_qggXJq",
    "celosia_sizing_band",
]

with open("/tmp/build_product_template.json", "w") as f:
    json.dump(data, f, indent=2)

print("Wrote /tmp/build_product_template.json")
