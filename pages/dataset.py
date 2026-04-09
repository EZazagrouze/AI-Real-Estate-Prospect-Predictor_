import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dataset", layout="wide")

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
    <h1 style='text-align: center; color: #00C9A7;'>
     Dataset Analysis
    </h1>
    <p style='text-align: center;'>
    Explore and analyze real estate prospects
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

search = st.sidebar.text_input(" Search by city")

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

x_axis = st.sidebar.selectbox(
    "X-Axis",
    ["age", "income", "children", "budget"]
)

y_axis = st.sidebar.selectbox(
    "Y-Axis",
    ["income", "budget", "age", "children"]
)

# -----------------------------
# FILTER DATA
# -----------------------------
filtered_data = data[
    (data["city"].isin(city_filter)) &
    (data["property_type"].isin(property_filter))
]

if search:
    filtered_data = filtered_data[
        filtered_data["city"].str.contains(search, case=False)
    ]

# -----------------------------
# CHARTS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader(" Relationship (Scatter)")
    st.scatter_chart(filtered_data[[x_axis, y_axis]])

with col2:
    st.subheader(" Avg Budget by City")
    st.bar_chart(filtered_data.groupby("city")["budget"].mean())

# -----------------------------
# TABLE
# -----------------------------
st.markdown("###  Filtered Dataset")
st.dataframe(filtered_data)

# -----------------------------
# DOWNLOAD
# -----------------------------
st.download_button(
    label="⬇ Download Dataset",
    data=filtered_data.to_csv(index=False),
    file_name="dataset.csv",
    mime="text/csv"
)