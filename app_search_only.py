
import re
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="FnD SKU Search",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
.block-container { padding-top: 1rem; padding-bottom: 2rem; }
html, body { font-size: 18px !important; }

.stTextInput input {
    min-height: 48px;
    font-size: 18px !important;
}

.stButton button {
    min-height: 52px;
    font-size: 18px !important;
    border-radius: 12px;
    width: 100%;
}

.stDataFrame { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

MASTER_CSV = "fnd_sku_master.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(MASTER_CSV, dtype=str).fillna("")
    df.columns = [c.strip() for c in df.columns]
    return df

try:
    df = load_data()
except:
    st.error("Missing fnd_sku_master.csv — keep it in the same folder as this app.")
    st.stop()

col_item = next((c for c in df.columns if "item" in c.lower()), None)
col_desc = next((c for c in df.columns if "desc" in c.lower()), None)
col_stock = next((c for c in df.columns if "stock" in c.lower()), None)
col_spo = next((c for c in df.columns if "special" in c.lower() or "spo" in c.lower()), None)

df["_item_norm"] = df[col_item].str.lower() if col_item else ""
df["_desc_norm"] = df[col_desc].str.lower() if col_desc else ""

st.title("🔎 FnD SKU Search")
st.caption("Fast SKU lookup — phone optimized")

q_item = st.text_input("Search Schluter Item #", placeholder="Example: J125MBW")
q_desc = st.text_input("Search Description", placeholder="Example: matte white jolly")

max_results = st.slider("Max results", 5, 200, 50)

qi = (q_item or "").strip().lower()
qd = (q_desc or "").strip().lower()

filtered = df.copy()

if qi:
    filtered = filtered[filtered["_item_norm"].str.contains(re.escape(qi), na=False)]

if qd:
    tokens = qd.split()
    for t in tokens:
        filtered = filtered[filtered["_desc_norm"].str.contains(re.escape(t), na=False)]

display_cols = [c for c in [col_item, col_desc, col_stock, col_spo] if c]

if qi or qd:
    st.divider()
    st.write(f"**Matches found:** {len(filtered):,}")
    results = filtered[display_cols].head(max_results)
    st.dataframe(results, use_container_width=True, height=520)
else:
    st.info("Type an Item # or Description to start searching.")
