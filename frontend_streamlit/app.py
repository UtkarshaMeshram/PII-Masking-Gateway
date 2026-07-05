import streamlit as st
import re
import random
import string
from datetime import datetime
import httpx

st.set_page_config(page_title="DRKT", layout="wide", page_icon="🛍️")

# ─────────────────────────────────────────────
# GLOBAL CSS — Dark theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

:root {
    --accent:   #e8ff47;
    --bg:       #0d0d0d;
    --surface:  #161616;
    --surface2: #1e1e1e;
    --border:   #2a2a2a;
    --text:     #f0f0f0;
    --muted:    #666666;
    --green:    #3ddc84;
    --red:      #ff4e6a;
}

html, body, [class*="css"], .stApp {
    font-family: 'Space Grotesk', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container {
    padding-top: 0 !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    max-width: 1280px !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }
section[data-testid="stSidebar"] .stRadio label {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    color: var(--muted) !important;
}
section[data-testid="stSidebar"] hr { border-color: var(--border) !important; }

/* ── Buttons — base style ── */
div.stButton > button {
    background: transparent !important;
    color: var(--accent) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    border: 1.5px solid var(--accent) !important;
    border-radius: 8px !important;
    padding: 0.45rem 0.8rem !important;
    width: 100% !important;
    transition: background 0.18s, color 0.18s !important;
    white-space: nowrap !important;
}
div.stButton > button:hover {
    background: var(--accent) !important;
    color: #000 !important;
}

/* Ghost buttons: sidebar nav, back buttons */
div.stButton > button.ghost-btn {
    border-color: var(--border) !important;
    color: var(--text) !important;
}

/* Danger / remove buttons */
.remove-btn div.stButton > button {
    border-color: #444 !important;
    color: var(--muted) !important;
    font-size: 0.7rem !important;
}
.remove-btn div.stButton > button:hover {
    background: rgba(255,78,106,0.15) !important;
    color: var(--red) !important;
    border-color: var(--red) !important;
}

/* Wishlist heart button — small, icon-like */
.wl-btn div.stButton > button {
    border-color: #333 !important;
    color: var(--muted) !important;
    font-size: 1rem !important;
    padding: 0.3rem 0.5rem !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
}
.wl-btn div.stButton > button:hover {
    background: rgba(255,78,106,0.15) !important;
    color: var(--red) !important;
    border-color: var(--red) !important;
}
.wl-btn-active div.stButton > button {
    border-color: var(--red) !important;
    color: var(--red) !important;
    font-size: 1rem !important;
    padding: 0.3rem 0.5rem !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
}
.wl-btn-active div.stButton > button:hover {
    background: rgba(255,78,106,0.2) !important;
}

/* Checkout primary button */
.primary-btn div.stButton > button {
    background: var(--accent) !important;
    color: #000 !important;
    border-color: var(--accent) !important;
}
.primary-btn div.stButton > button:hover {
    background: #d4e93f !important;
}

/* ── Inputs ── */
input, textarea, select {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.88rem !important;
}
input:focus, textarea:focus { border-color: var(--accent) !important; }
input::placeholder, textarea::placeholder { color: var(--muted) !important; }
label[data-testid="stWidgetLabel"] p {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
}

/* Number input */
div[data-testid="stNumberInput"] input { text-align: center !important; }
div[data-testid="stNumberInput"] button {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    width: auto !important;
}

/* Divider */
hr { border-color: var(--border) !important; margin: 0.6rem 0 !important; }

/* Toast */
[data-testid="stToast"] {
    background: var(--surface2) !important;
    border: 1px solid var(--green) !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
}

/* Error / Alert */
[data-testid="stAlert"] {
    background: rgba(255,78,106,0.08) !important;
    border: 1px solid rgba(255,78,106,0.4) !important;
    border-radius: 8px !important;
}
[data-testid="stAlert"] p { color: var(--text) !important; }

/* Images */
[data-testid="stImage"] img { border-radius: 8px !important; }

/* Fade in */
.stApp { animation: fadeIn 0.2s ease; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
defaults = {
    "gender": "Men",
    "category": None,
    "page": "shop",
    "cart": [],
    "wishlist": [],
    "order_id": None,
    "_ratings": {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
# CATALOG
# ─────────────────────────────────────────────
PRODUCTS = {
    "Men": {
        "Footwear": [
            {"name": "Derby Oxford",       "price": 4299, "brand": "Clarks",          "img": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&q=80",  "new": True},
            {"name": "Canvas Low-Top",     "price": 1999, "brand": "Vans",            "img": "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=500&q=80", "new": False},
            {"name": "Leather Loafer",     "price": 3499, "brand": "Hush Puppies",   "img": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=500&q=80", "new": True},
        ],
        "T-Shirts": [
            {"name": "Relaxed White Tee",  "price": 899,  "brand": "H&M",            "img": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&q=80", "new": False},
            {"name": "Textured Knit Polo", "price": 1599, "brand": "US Polo",        "img": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=500&q=80", "new": True},
            {"name": "Washed Oversized",   "price": 1299, "brand": "Roadster",       "img": "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=500&q=80", "new": False},
        ],
        "Western": [
            {"name": "Slim Tapered Chino", "price": 2199, "brand": "Mango Man",      "img": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=500&q=80", "new": False},
            {"name": "Denim Jacket",       "price": 3999, "brand": "Jack & Jones",   "img": "https://images.unsplash.com/photo-1601333144130-8cbb312386b6?w=500&q=80", "new": True},
            {"name": "Linen Shirt",        "price": 1899, "brand": "Marks & Spencer","img": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500&q=80", "new": False},
        ],
        "Traditional": [
            {"name": "Cotton Kurta",       "price": 1399, "brand": "Manyavar",       "img": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=500&q=80", "new": False},
            {"name": "Embroidered Kurta",  "price": 2799, "brand": "Fabindia",       "img": "https://images.unsplash.com/photo-1617196034183-421b4040ed20?w=500&q=80", "new": True},
            {"name": "Bandhgala Set",      "price": 6499, "brand": "Manyavar",       "img": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500&q=80", "new": False},
        ],
    },
    "Women": {
        "Footwear": [
            {"name": "Block Heel Mule",    "price": 2499, "brand": "Steve Madden",   "img": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500&q=80",  "new": True},
            {"name": "Strappy Flat",       "price": 1599, "brand": "Aldo",           "img": "https://images.unsplash.com/photo-1535043934128-cf0b28d52f95?w=500&q=80", "new": False},
            {"name": "Chelsea Boot",       "price": 4299, "brand": "Clarks",         "img": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=500&q=80",  "new": True},
        ],
        "Tops": [
            {"name": "Linen Wrap Blouse",  "price": 1199, "brand": "Zudio",          "img": "https://images.unsplash.com/photo-1598554747436-c9293d6a588f?w=500&q=80", "new": False},
            {"name": "Crop Knit Top",      "price": 1499, "brand": "Bershka",        "img": "https://images.unsplash.com/photo-1594938298603-c8148c4b4afe?w=500&q=80", "new": True},
            {"name": "Pintuck Tunic",      "price": 1799, "brand": "W",              "img": "https://images.unsplash.com/photo-1485462537746-965f33f7f6a7?w=500&q=80", "new": False},
        ],
        "Western": [
            {"name": "Pleated Midi Skirt", "price": 2199, "brand": "Mango",          "img": "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=500&q=80", "new": False},
            {"name": "High-Rise Mom Jean", "price": 2799, "brand": "Levi's",         "img": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500&q=80", "new": True},
            {"name": "Blazer Dress",       "price": 3699, "brand": "Forever 21",     "img": "https://images.unsplash.com/photo-1585386959984-a4155224a1ad?w=500&q=80", "new": False},
        ],
        "Traditional": [
            {"name": "Bandhani Kurti",     "price": 1499, "brand": "Biba",           "img": "https://images.unsplash.com/photo-1624222247344-550fb60583dc?w=500&q=80", "new": False},
            {"name": "Anarkali Suit",      "price": 4299, "brand": "Libas",          "img": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500&q=80", "new": True},
            {"name": "Palazzo Co-ord",     "price": 2899, "brand": "Aurelia",        "img": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=500&q=80", "new": False},
        ],
        "Saree": [
            {"name": "Banarasi Silk",      "price": 7499, "brand": "Saree Mall",     "img": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500&q=80", "new": False},
            {"name": "Chiffon Drape",      "price": 3199, "brand": "Mitera",         "img": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=500&q=80", "new": True},
            {"name": "Organza Edit",       "price": 4799, "brand": "Pothys",         "img": "https://images.unsplash.com/photo-1624222247344-550fb60583dc?w=500&q=80", "new": False},
        ],
    },
}

ALL_PRODUCTS = [p for gender in PRODUCTS.values() for cat in gender.values() for p in cat]

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def get_meta(name, price):
    if name not in st.session_state._ratings:
        orig = int(price * random.uniform(1.3, 1.7) / 100) * 100
        st.session_state._ratings[name] = {
            "orig":    orig,
            "rating":  round(random.uniform(3.8, 4.8), 1),
            "reviews": random.randint(120, 4800),
        }
    return st.session_state._ratings[name]

def add_to_cart(prod):
    for item in st.session_state.cart:
        if item["name"] == prod["name"]:
            item["qty"] += 1
            return
    st.session_state.cart.append({**prod, "qty": 1})

def remove_from_cart(name):
    st.session_state.cart = [i for i in st.session_state.cart if i["name"] != name]

def set_cart_qty(name, qty):
    if qty <= 0:
        remove_from_cart(name)
    else:
        for item in st.session_state.cart:
            if item["name"] == name:
                item["qty"] = qty
                break

def cart_count():
    return sum(i["qty"] for i in st.session_state.cart)

def cart_subtotal():
    return sum(i["price"] * i["qty"] for i in st.session_state.cart)

def cart_tax():
    return int(cart_subtotal() * 0.05)

def cart_grand():
    return cart_subtotal() + cart_tax()

def is_in_wishlist(name):
    return name in st.session_state.wishlist

def add_to_wishlist(name):
    if name not in st.session_state.wishlist:
        st.session_state.wishlist.append(name)

def remove_from_wishlist(name):
    if name in st.session_state.wishlist:
        st.session_state.wishlist.remove(name)

def toggle_wishlist(name):
    if is_in_wishlist(name):
        remove_from_wishlist(name)
    else:
        add_to_wishlist(name)

def cart_savings():
    return sum(
        (get_meta(i["name"], i["price"])["orig"] - i["price"]) * i["qty"]
        for i in st.session_state.cart
    )

def generate_order_id():
    return "DRK" + "".join(random.choices(string.digits + string.ascii_uppercase, k=9))

def valid_email(e):
    return bool(re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", e.strip()))

def valid_card(c):
    return bool(re.fullmatch(r"\d{16}", c.replace(" ", "")))

def valid_cvv(c):
    return bool(re.fullmatch(r"\d{3,4}", c.strip()))

def valid_expiry(e):
    try:
        m, y = e.replace(" ", "").split("/")
        return datetime(2000 + int(y), int(m), 1) > datetime.now()
    except Exception:
        return False

def valid_phone(p):
    return bool(re.fullmatch(r"\d{10}", p.replace(" ", "").replace("-", "")))


# ─────────────────────────────────────────────
# COMPONENTS
# ─────────────────────────────────────────────

def _step_node(n, label, state):
    """
    state: 'done' | 'active' | 'todo'
    Returns (circle_html, label_color, line_color)
    """
    if state == "done":
        circle = (
            '<div style="width:26px;height:26px;border-radius:50%;background:#3ddc84;'
            'border:2px solid #3ddc84;display:flex;align-items:center;justify-content:center;'
            'font-size:12px;font-weight:700;color:#000;flex-shrink:0">&#10003;</div>'
        )
        lc, line = "#3ddc84", "#3ddc84"
    elif state == "active":
        circle = (
            '<div style="width:26px;height:26px;border-radius:50%;background:#e8ff47;'
            'border:2px solid #e8ff47;display:flex;align-items:center;justify-content:center;'
            'font-size:12px;font-weight:700;color:#000;flex-shrink:0">' + str(n) + '</div>'
        )
        lc, line = "#e8ff47", "#2a2a2a"
    else:
        circle = (
            '<div style="width:26px;height:26px;border-radius:50%;background:#1e1e1e;'
            'border:2px solid #2a2a2a;display:flex;align-items:center;justify-content:center;'
            'font-size:12px;font-weight:700;color:#666;flex-shrink:0">' + str(n) + '</div>'
        )
        lc, line = "#555", "#2a2a2a"
    return circle, lc, line


def render_steps(current):
    steps = ["Bag", "Address & Payment", "Confirmed"]
    nodes_html = []

    for i, label in enumerate(steps):
        n = i + 1
        if n < current:
            state = "done"
        elif n == current:
            state = "active"
        else:
            state = "todo"

        circle, lc, line_color = _step_node(n, label, state)

        is_last = (i == len(steps) - 1)
        flex_val = "1" if is_last else "0 0 auto"
        connector = (
            ""
            if is_last
            else '<div style="flex:1;height:1px;background:' + line_color + ';margin:0 10px"></div>'
        )

        node = (
            '<div style="display:flex;align-items:center;flex:' + flex_val + '">'
            '<div style="display:flex;align-items:center;gap:7px">'
            + circle
            + '<span style="font-size:13px;font-weight:600;color:' + lc + ';white-space:nowrap">'
            + label
            + '</span>'
            '</div>'
            + connector
            + '</div>'
        )
        nodes_html.append(node)

    html = (
        '<div style="display:flex;align-items:center;background:#161616;border:1px solid #2a2a2a;'
        'border-radius:10px;padding:14px 20px;margin-bottom:24px">'
        + "".join(nodes_html)
        + '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_header():
    wl_count = len(st.session_state.wishlist)
    bag_count = cart_count()
    wl_icon = "♥" if wl_count else "♡"
    wl_color = "#ff4e6a" if wl_count else "#666"
    bag_color = "#e8ff47" if bag_count else "#666"
    wl_label = "Wishlist (" + str(wl_count) + ")" if wl_count else "Wishlist"
    bag_label = "Bag (" + str(bag_count) + ")" if bag_count else "Bag"

    html = (
        '<div style="background:rgba(13,13,13,0.97);border-bottom:1px solid #2a2a2a;margin-bottom:0">'
        '<div style="display:flex;align-items:center;justify-content:space-between;padding:14px 0 12px">'
        '<span style="font-family:\'Syne\',sans-serif;font-size:1.6rem;font-weight:800;'
        'color:#e8ff47;letter-spacing:-0.5px">DRKT</span>'
        '<div style="display:flex;gap:24px;align-items:center">'
        '<div style="text-align:center;font-size:0.7rem;font-weight:600;color:' + wl_color + '">'
        '<div style="font-size:1.1rem">' + wl_icon + '</div>' + wl_label +
        '</div>'
        '<div style="text-align:center;font-size:0.7rem;font-weight:600;color:' + bag_color + '">'
        '<div style="font-size:1.1rem">&#128717;</div>' + bag_label +
        '</div>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_price_summary(show_items=False):
    subtotal = cart_subtotal()
    tax = cart_tax()
    grand = cart_grand()
    savings = cart_savings()

    items_html = ""
    if show_items:
        for item in st.session_state.cart:
            line_total = item["price"] * item["qty"]
            items_html += (
                '<div style="display:flex;justify-content:space-between;padding:6px 0;'
                'font-size:13px;border-bottom:1px dashed #2a2a2a">'
                '<span style="color:#888;max-width:170px;overflow:hidden;text-overflow:ellipsis;'
                'white-space:nowrap">' + item["name"] + " \u00d7" + str(item["qty"]) + '</span>'
                '<span>&#8377;' + f"{line_total:,}" + '</span>'
                '</div>'
            )

    html = (
        '<div style="background:#161616;border:1px solid #2a2a2a;border-radius:12px;padding:18px">'
        '<div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.2px;'
        'color:#555;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid #2a2a2a">'
        'Price Details'
        '</div>'
        + items_html +
        '<div style="display:flex;justify-content:space-between;padding:7px 0;font-size:14px;'
        'border-bottom:1px dashed #2a2a2a">'
        '<span style="color:#888">Subtotal (' + str(cart_count()) + ' items)</span>'
        '<span>&#8377;' + f"{subtotal:,}" + '</span>'
        '</div>'
        '<div style="display:flex;justify-content:space-between;padding:7px 0;font-size:14px;'
        'border-bottom:1px dashed #2a2a2a;color:#3ddc84">'
        '<span>Discount</span>'
        '<span>-&#8377;' + f"{savings:,}" + '</span>'
        '</div>'
        '<div style="display:flex;justify-content:space-between;padding:7px 0;font-size:14px;'
        'border-bottom:1px dashed #2a2a2a">'
        '<span style="color:#888">Delivery</span>'
        '<span style="color:#3ddc84;font-weight:600">Free</span>'
        '</div>'
        '<div style="display:flex;justify-content:space-between;padding:7px 0;font-size:14px;'
        'border-bottom:1px dashed #2a2a2a">'
        '<span style="color:#888">GST (5%)</span>'
        '<span>&#8377;' + f"{tax:,}" + '</span>'
        '</div>'
        '<div style="display:flex;justify-content:space-between;padding:14px 0 10px;'
        'font-size:17px;font-weight:700">'
        '<span>Total</span>'
        '<span style="color:#e8ff47">&#8377;' + f"{grand:,}" + '</span>'
        '</div>'
        '<div style="background:rgba(61,220,132,0.08);border:1px solid rgba(61,220,132,0.25);'
        'border-radius:8px;padding:8px 12px;font-size:12px;font-weight:600;color:#3ddc84">'
        '&#127881; You save &#8377;' + f"{savings:,}" + ' on this order!'
        '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
    return tax, grand


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("GENDER")
    new_gender = st.radio("", ["Men", "Women"],
                          index=0 if st.session_state.gender == "Men" else 1)
    if new_gender != st.session_state.gender:
        st.session_state.gender = new_gender
        st.session_state.category = None
        st.session_state.page = "shop"
        st.rerun()

    st.divider()
    st.markdown("NAVIGATE")
    if st.button("🏠  Home / Shop", key="sb_home"):
        st.session_state.page = "shop"
        st.rerun()
    if st.button(f"🛍️  My Bag  ({cart_count()})", key="sb_bag"):
        st.session_state.page = "cart"
        st.rerun()
    if st.button(f"♡  Wishlist  ({len(st.session_state.wishlist)})", key="sb_wl"):
        st.session_state.page = "wishlist"
        st.rerun()

    if st.session_state.cart:
        st.divider()
        st.markdown("YOUR BAG")
        for item in st.session_state.cart:
            item_total = item["price"] * item["qty"]
            st.markdown(
                '<div style="display:flex;justify-content:space-between;align-items:center;'
                'padding:7px 0;border-bottom:1px solid #2a2a2a;font-size:12px">'
                '<span style="color:#ccc;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:120px">'
                + item["name"] + " \u00d7" + str(item["qty"]) +
                '</span>'
                '<span style="font-weight:700;color:#e8ff47;white-space:nowrap;margin-left:6px">'
                '&#8377;' + f"{item_total:,}" +
                '</span>'
                '</div>',
                unsafe_allow_html=True
            )
        st.markdown(
            '<div style="display:flex;justify-content:space-between;padding:10px 0 2px;'
            'font-size:14px;font-weight:700">'
            '<span>Total</span>'
            '<span style="color:#e8ff47">&#8377;' + f"{cart_subtotal():,}" + '</span>'
            '</div>',
            unsafe_allow_html=True
        )

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
render_header()
st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# PAGE: SHOP
# ═══════════════════════════════════════════════
if st.session_state.page == "shop":

    st.markdown(
        '<div style="background:#161616;border:1px solid #2a2a2a;border-radius:14px;'
        'padding:28px 32px;margin-bottom:24px;'
        'display:flex;align-items:center;justify-content:space-between">'
        '<div>'
        '<div style="font-family:\'Syne\',sans-serif;font-size:2rem;font-weight:800;line-height:1.15;margin-bottom:8px">'
        'New Season<br><span style="color:#e8ff47">Arrivals.</span>'
        '</div>'
        '<div style="color:#666;font-size:14px">Fresh styles for ' + st.session_state.gender + '. Updated daily.</div>'
        '</div>'
        '<div style="background:#e8ff47;color:#000;font-weight:800;font-size:13px;'
        'padding:10px 24px;border-radius:32px;letter-spacing:0.5px;white-space:nowrap">'
        'UP TO 50% OFF'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    cats = list(PRODUCTS[st.session_state.gender].keys())
    pill_labels = ["All"] + cats
    pill_cols = st.columns(len(pill_labels))
    for i, cat in enumerate(pill_labels):
        with pill_cols[i]:
            target = None if cat == "All" else cat
            is_active = st.session_state.category == target
            label = "✓ " + cat if is_active else cat
            if st.button(label, key="pill_" + cat):
                st.session_state.category = target
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    display_cats = [st.session_state.category] if st.session_state.category else cats

    for cat in display_cats:
        prods = PRODUCTS[st.session_state.gender][cat]
        st.markdown(
            '<div style="display:flex;align-items:baseline;gap:10px;margin-bottom:14px">'
            '<span style="font-family:\'Syne\',sans-serif;font-size:1.2rem;font-weight:800">' + cat + '</span>'
            '<span style="color:#555;font-size:12px">' + str(len(prods)) + ' items</span>'
            '</div>',
            unsafe_allow_html=True
        )

        pcols = st.columns(3)
        for j, prod in enumerate(prods):
            meta = get_meta(prod["name"], prod["price"])
            orig = meta["orig"]
            disc = int((orig - prod["price"]) / orig * 100)
            in_wl = is_in_wishlist(prod["name"])

            with pcols[j % 3]:
                new_badge = (
                    '<div style="display:inline-block;background:#e8ff47;color:#000;'
                    'font-size:10px;font-weight:800;padding:2px 10px;border-radius:4px;'
                    'margin-bottom:8px;letter-spacing:0.5px">NEW IN</div>'
                    if prod.get("new") else
                    '<div style="height:20px"></div>'
                )

                st.markdown(
                    '<div style="background:#161616;border:1px solid #2a2a2a;border-radius:12px;'
                    'overflow:hidden;margin-bottom:6px">'
                    '<img src="' + prod["img"] + '" style="width:100%;height:210px;object-fit:cover;display:block"/>'
                    '<div style="padding:11px 13px 10px">'
                    + new_badge +
                    '<div style="font-size:11px;font-weight:700;color:#555;margin-bottom:2px">'
                    + prod.get("brand", "DRKT") +
                    '</div>'
                    '<div style="font-size:14px;font-weight:500;margin-bottom:8px;'
                    'white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'
                    + prod["name"] +
                    '</div>'
                    '<div style="display:flex;align-items:center;gap:8px;margin-bottom:7px">'
                    '<span style="font-weight:700;font-size:15px">&#8377;' + f"{prod['price']:,}" + '</span>'
                    '<span style="font-size:12px;color:#555;text-decoration:line-through">&#8377;' + f"{orig:,}" + '</span>'
                    '<span style="font-size:11px;color:#3ddc84;font-weight:700">(' + str(disc) + '% off)</span>'
                    '</div>'
                    '<div style="display:flex;align-items:center;gap:6px">'
                    '<span style="background:#3ddc84;color:#000;font-size:10px;'
                    'font-weight:700;padding:2px 6px;border-radius:4px">'
                    '&#11088; ' + str(meta["rating"]) +
                    '</span>'
                    '<span style="font-size:11px;color:#555">(' + f"{meta['reviews']:,}" + ')</span>'
                    '</div>'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

                ba, bb, bwl = st.columns([5, 5, 2])
                with ba:
                    if st.button("ADD", key="add_" + cat + "_" + str(j)):
                        add_to_cart(prod)
                        st.toast("✓ " + prod["name"] + " added to bag!", icon="🛍️")
                        st.rerun()
                with bb:
                    if st.button("BUY NOW", key="buy_" + cat + "_" + str(j)):
                        add_to_cart(prod)
                        st.session_state.page = "cart"
                        st.rerun()
                with bwl:
                    wl_class = "wl-btn-active" if in_wl else "wl-btn"
                    wl_icon = "♥" if in_wl else "♡"
                    st.markdown('<div class="' + wl_class + '">', unsafe_allow_html=True)
                    if st.button(wl_icon, key="wl_" + cat + "_" + str(j)):
                        was_in = is_in_wishlist(prod["name"])
                        toggle_wishlist(prod["name"])
                        st.toast("Removed from wishlist" if was_in else "❤ Added to wishlist!")
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# PAGE: WISHLIST
# ═══════════════════════════════════════════════
elif st.session_state.page == "wishlist":

    hc1, hc2 = st.columns([1, 9])
    with hc1:
        if st.button("← Back", key="wl_back"):
            st.session_state.page = "shop"
            st.rerun()
    with hc2:
        st.markdown(
            '<div style="font-family:\'Syne\',sans-serif;font-size:1.4rem;font-weight:800;padding-top:2px">'
            'Wishlist <span style="color:#555;font-size:1rem;font-weight:400">('
            + str(len(st.session_state.wishlist)) + ' saved)</span>'
            '</div>',
            unsafe_allow_html=True
        )

    if not st.session_state.wishlist:
        st.markdown(
            '<div style="text-align:center;padding:80px 0;color:#555">'
            '<div style="font-size:48px;margin-bottom:12px">&#9825;</div>'
            '<div style="font-size:16px;font-weight:600;color:#f0f0f0;margin-bottom:6px">Your wishlist is empty</div>'
            '<div style="font-size:13px">Tap &#9825; on any product to save it here</div>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        wl_prods = [p for p in ALL_PRODUCTS if is_in_wishlist(p["name"])]
        wl_cols = st.columns(3)

        for i, prod in enumerate(wl_prods):
            with wl_cols[i % 3]:
                meta = get_meta(prod["name"], prod["price"])
                orig = meta["orig"]
                disc = int((orig - prod["price"]) / orig * 100)

                st.markdown(
                    '<div style="background:#161616;border:1px solid #2a2a2a;border-radius:12px;'
                    'overflow:hidden;margin-bottom:6px">'
                    '<img src="' + prod["img"] + '" style="width:100%;height:200px;object-fit:cover;display:block"/>'
                    '<div style="padding:11px 13px 10px">'
                    '<div style="font-size:11px;color:#555;margin-bottom:2px">' + prod.get("brand", "") + '</div>'
                    '<div style="font-size:14px;font-weight:500;margin-bottom:6px;'
                    'white-space:nowrap;overflow:hidden;text-overflow:ellipsis">' + prod["name"] + '</div>'
                    '<div style="display:flex;align-items:center;gap:8px">'
                    '<span style="font-weight:700;font-size:15px;color:#e8ff47">&#8377;' + f"{prod['price']:,}" + '</span>'
                    '<span style="font-size:12px;color:#555;text-decoration:line-through">&#8377;' + f"{orig:,}" + '</span>'
                    '<span style="font-size:11px;color:#3ddc84;font-weight:700">(' + str(disc) + '% off)</span>'
                    '</div>'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

                if st.button("ADD TO BAG", key="wl_add_" + str(i)):
                    add_to_cart(prod)
                    st.toast("✓ " + prod["name"] + " added to bag!", icon="🛍️")
                    st.rerun()

                st.markdown('<div class="remove-btn">', unsafe_allow_html=True)
                if st.button("✕  Remove from wishlist", key="wl_rm_" + str(i)):
                    remove_from_wishlist(prod["name"])
                    st.toast(prod["name"] + " removed from wishlist")
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# PAGE: CART
# ═══════════════════════════════════════════════
elif st.session_state.page == "cart":

    render_steps(1)
    st.markdown(
        '<div style="font-family:\'Syne\',sans-serif;font-size:1.4rem;font-weight:800;margin-bottom:20px">'
        'My Bag <span style="color:#555;font-size:1rem;font-weight:400">(' + str(cart_count()) + ' items)</span>'
        '</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.cart:
        st.markdown(
            '<div style="text-align:center;padding:60px 0;background:#161616;'
            'border:1px solid #2a2a2a;border-radius:12px">'
            '<div style="font-size:40px;margin-bottom:12px">&#128717;</div>'
            '<div style="font-size:16px;font-weight:600;margin-bottom:6px">Your bag is empty</div>'
            '<div style="font-size:13px;color:#666">Add items from the shop</div>'
            '</div>',
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Continue Shopping", key="cart_empty_back"):
            st.session_state.page = "shop"
            st.rerun()
    else:
        left, right = st.columns([3, 1])

        with left:
            for idx, item in enumerate(list(st.session_state.cart)):
                st.markdown(
                    '<div style="background:#161616;border:1px solid #2a2a2a;border-radius:12px;'
                    'padding:14px 16px;margin-bottom:2px">',
                    unsafe_allow_html=True
                )

                img_col, info_col, qty_col = st.columns([1, 4, 2])

                with img_col:
                    st.image(item["img"], width=76)

                with info_col:
                    st.markdown(
                        '<div style="padding-top:4px">'
                        '<div style="font-size:11px;color:#555;margin-bottom:2px">' + item.get("brand", "") + '</div>'
                        '<div style="font-size:15px;font-weight:600;margin-bottom:4px">' + item["name"] + '</div>'
                        '<div style="font-size:13px;color:#555">&#8377;' + f"{item['price']:,}" + ' per piece</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )

                with qty_col:
                    st.markdown(
                        '<div style="font-size:11px;color:#555;margin-bottom:4px;font-weight:600">QTY</div>',
                        unsafe_allow_html=True
                    )
                    qty_options = list(range(1, 11))
                    current_idx = qty_options.index(item["qty"]) if item["qty"] in qty_options else 0
                    new_qty = st.selectbox(
                        "qty_select", qty_options,
                        index=current_idx,
                        key="qty_sel_" + str(idx),
                        label_visibility="collapsed"
                    )
                    if new_qty != item["qty"]:
                        set_cart_qty(item["name"], new_qty)
                        st.rerun()

                    line_total = item["price"] * item["qty"]
                    st.markdown(
                        '<div style="font-size:16px;font-weight:700;color:#e8ff47;margin-top:6px">'
                        '&#8377;' + f"{line_total:,}" + '</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown('<div class="remove-btn">', unsafe_allow_html=True)
                    if st.button("✕ Remove", key="del_" + str(idx) + "_" + item["name"]):
                        remove_from_cart(item["name"])
                        st.toast(item["name"] + " removed")
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("</div><br>", unsafe_allow_html=True)

        with right:
            render_price_summary()
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
            if st.button("CHECKOUT →", key="to_checkout"):
                st.session_state.page = "checkout"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Continue Shopping", key="cart_back"):
            st.session_state.page = "shop"
            st.rerun()

# ═══════════════════════════════════════════════
# PAGE: CHECKOUT
# ═══════════════════════════════════════════════
elif st.session_state.page == "checkout":

    render_steps(2)
    st.markdown(
        '<div style="font-family:\'Syne\',sans-serif;font-size:1.4rem;font-weight:800;margin-bottom:20px">'
        'Secure <span style="color:#e8ff47">Checkout</span>'
        '</div>',
        unsafe_allow_html=True
    )

    grand = cart_grand()
    left, right = st.columns([3, 2])

    with right:
        render_price_summary(show_items=True)

    with left:
        st.markdown(
            '<div style="background:#161616;border:1px solid #2a2a2a;border-radius:12px;'
            'padding:18px 20px;margin-bottom:14px">'
            '<div style="font-size:10px;font-weight:700;text-transform:uppercase;'
            'letter-spacing:1.2px;color:#555;margin-bottom:14px">'
            '&#128230; Delivery Details'
            '</div>',
            unsafe_allow_html=True
        )
        name    = st.text_input("Full Name",        placeholder="Your full name",         key="co_name")
        email   = st.text_input("Email Address",    placeholder="you@email.com",          key="co_email")
        phone   = st.text_input("Phone Number",     placeholder="10-digit mobile number", key="co_phone", max_chars=10)
        address = st.text_area( "Delivery Address", placeholder="Street, City, State, PIN",key="co_addr", height=80)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div style="background:#161616;border:1px solid #2a2a2a;border-radius:12px;'
            'padding:18px 20px">'
            '<div style="font-size:10px;font-weight:700;text-transform:uppercase;'
            'letter-spacing:1.2px;color:#555;margin-bottom:14px">'
            '&#128179; Card Details'
            '</div>',
            unsafe_allow_html=True
        )
        card_name = st.text_input("Name on Card", placeholder="As printed on card",   key="co_cname")
        card_num  = st.text_input("Card Number",  placeholder="16-digit card number", key="co_cnum",  max_chars=16)
        ec1, ec2  = st.columns(2)
        with ec1:
            expiry = st.text_input("Expiry Date", placeholder="MM/YY", key="co_exp", max_chars=5)
        with ec2:
            cvv = st.text_input("CVV", placeholder="3 or 4 digits", key="co_cvv", max_chars=4, type="password")
        st.markdown(
            '<div style="display:flex;gap:16px;margin-top:10px;color:#555;font-size:12px">'
            '<span>&#128274; 256-bit SSL</span>'
            '<span>&#9989; PCI DSS</span>'
            '<span>&#128737; 100% Secure</span>'
            '</div>',
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        nav1, nav2 = st.columns(2)
        with nav1:
            if st.button("← Back to Bag", key="checkout_back"):
                st.session_state.page = "cart"
                st.rerun()
        with nav2:
            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
            if st.button("PAY  ₹" + f"{grand:,}" + " →", key="pay_btn"):
                errors = []
                if not name.strip():
                    errors.append("Full name is required.")
                if not valid_email(email):
                    errors.append("Enter a valid email address.")
                if not valid_phone(phone):
                    errors.append("Phone must be exactly 10 digits.")
                if not address.strip():
                    errors.append("Delivery address is required.")
                if not card_name.strip():
                    errors.append("Name on card is required.")
                if not valid_card(card_num):
                    errors.append("Card number must be exactly 16 digits.")
                if not valid_expiry(expiry):
                    errors.append("Expiry date is invalid or has passed (use MM/YY).")
                if not valid_cvv(cvv):
                    errors.append("CVV must be 3 or 4 digits.")

                if errors:
                    for err in errors:
                        st.error(err)
                else:
                    
                    try:
                        response = httpx.post(
                             "http://127.0.0.1:8000/scan",
                              json={
                                    "text": f"""
                                     Name: {name}
                                     Email: {email}
                                     Phone: {phone}
                                     Address: {address}
                                     Card: {card_num}
                                     CVV: {cvv}
                                     Expiry: {expiry}
                                     """
                              }
                        )
                        
                        result = response.json()
                         

                    # 👇 silent logging only (optional debug)
                        print("PII Scan Result:", result)

                    except Exception as e:
                       print("Backend error:", e)
                    
                    st.session_state.order_id = generate_order_id()
                    st.session_state.page = "confirmation"
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# PAGE: CONFIRMATION
# ═══════════════════════════════════════════════
elif st.session_state.page == "confirmation":

    render_steps(3)

    grand   = cart_grand()
    tax     = cart_tax()
    savings = cart_savings()

    items_html = "".join(
        '<div style="display:flex;justify-content:space-between;padding:8px 0;'
        'border-bottom:1px solid #2a2a2a;font-size:14px">'
        '<span style="color:#666">' + i["name"] + " \u00d7" + str(i["qty"]) + '</span>'
        '<span style="font-weight:600">&#8377;' + f"{i['price'] * i['qty']:,}" + '</span>'
        '</div>'
        for i in st.session_state.cart
    )

    st.markdown(
        '<div style="max-width:540px;margin:0 auto;text-align:center;background:#161616;'
        'border:1px solid #2a2a2a;border-radius:16px;padding:44px 40px">'
        '<div style="width:64px;height:64px;border-radius:50%;'
        'background:rgba(61,220,132,0.1);border:2px solid #3ddc84;'
        'display:flex;align-items:center;justify-content:center;'
        'font-size:26px;margin:0 auto 20px">&#10003;</div>'
        '<div style="font-size:11px;letter-spacing:2px;color:#555;margin-bottom:8px;text-transform:uppercase">'
        'Order ID: ' + str(st.session_state.order_id) +
        '</div>'
        '<div style="font-family:\'Syne\',sans-serif;font-size:2rem;font-weight:800;margin-bottom:10px">'
        'Order Confirmed!'
        '</div>'
        '<div style="color:#666;font-size:13px;line-height:2.1;margin-bottom:28px">'
        'Your order will be dispatched within 24 hours.<br>'
        'Estimated delivery: <strong style="color:#f0f0f0">3&#8211;5 business days</strong>'
        '</div>'
        '<div style="text-align:left;border-top:1px solid #2a2a2a;padding-top:16px">'
        + items_html +
        '<div style="display:flex;justify-content:space-between;padding:8px 0;'
        'border-bottom:1px solid #2a2a2a;font-size:14px">'
        '<span style="color:#666">GST (5%)</span>'
        '<span>&#8377;' + f"{tax:,}" + '</span>'
        '</div>'
        '<div style="display:flex;justify-content:space-between;padding:14px 0 0;'
        'font-size:17px;font-weight:700">'
        '<span>Grand Total</span>'
        '<span style="color:#e8ff47">&#8377;' + f"{grand:,}" + '</span>'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    _, cc, _ = st.columns([1, 2, 1])
    with cc:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("CONTINUE SHOPPING 🛍️", key="conf_continue"):
            st.session_state.cart     = []
            st.session_state.category = None
            st.session_state.page     = "shop"
            st.session_state.order_id = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)