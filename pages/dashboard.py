import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard", layout="wide")

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
    <h1 style='text-align: center; color: #00C9A7;'>
     Advanced Dashboard
    </h1>
    <p style='text-align: center;'>
    Real estate insights & analytics
    </p>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# LOAD DATA
# -----------------------------
data = pd.read_csv(
    "real_estate_prospects.csv",
    sep=";",
    encoding="utf-8-sig"
)

data.columns = data.columns.str.strip()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header(" Filters")

city_filter = st.sidebar.multiselect(
    "City",
    data["city"].unique(),
    default=data["city"].unique()
)

property_filter = st.sidebar.multiselect(
    "Property Type",
    data["property_type"].unique(),
    default=data["property_type"].unique()
)

# -----------------------------
# FILTER DATA
# -----------------------------
df = data[
    (data["city"].isin(city_filter)) &
    (data["property_type"].isin(property_filter))
]

# -----------------------------
# METRICS
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Prospects", len(df))

if len(df) > 0:
    col2.metric("Buy Rate (%)", round(df["bought"].mean()*100,2))
    col3.metric("Average Budget", round(df["budget"].mean(),0))
else:
    col2.metric("Buy Rate (%)", 0)
    col3.metric("Average Budget", 0)

st.markdown("---")

# -----------------------------
# BAR CHARTS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader(" Prospects by City")
    st.bar_chart(df["city"].value_counts())

with col2:
    st.subheader(" Property Types")
    st.bar_chart(df["property_type"].value_counts())

st.markdown("---")

# -----------------------------
# PIE CHARTS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader(" Buy vs Not Buy")
    fig1, ax1 = plt.subplots()
    df["bought"].value_counts().plot.pie(
        autopct='%1.1f%%',
        ax=ax1
    )
    ax1.set_ylabel("")
    st.pyplot(fig1)

with col2:
    st.subheader(" Distribution by City")
    fig2, ax2 = plt.subplots()
    df["city"].value_counts().plot.pie(
        autopct='%1.1f%%',
        ax=ax2
    )
    ax2.set_ylabel("")
    st.pyplot(fig2)