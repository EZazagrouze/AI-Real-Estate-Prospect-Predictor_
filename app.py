import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="AI Real Estate", layout="wide")

# -----------------------------
# STATE NAVIGATION
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# -----------------------------
# NAVBAR PRO
# -----------------------------
col1, col2, col3 = st.columns([2,5,2])

with col1:
    st.markdown("###  AI Real Estate")

with col2:
    c1, c2, c3 = st.columns(3)

    if c1.button(" Home"):
        st.session_state.page = "Home"

    if c2.button(" Dashboard"):
        st.session_state.page = "Dashboard"

    if c3.button(" Dataset"):
        st.session_state.page = "Dataset"



st.markdown("---")

# -----------------------------
# LOAD MODEL
# -----------------------------
model = joblib.load("model.pkl")
model_columns = joblib.load("columns.pkl")

# -----------------------------
# LOAD DATA
# -----------------------------
def load_data():
    try:
        df = pd.read_csv("real_estate_prospects.csv", sep=";", encoding="utf-8-sig")
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=[
            "id","age","income","marital_status",
            "children","budget","city","property_type","bought"
        ])

data = load_data()

# =============================
#  HOME
# =============================
if st.session_state.page == "Home":

    st.markdown("##  AI Real Estate Predictor")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 18, 100)
        income = st.number_input("Income")
        children = st.number_input("Children", 0, 10)

    with col2:
        budget = st.number_input("Budget")

        marital_status = st.selectbox(
            "Marital Status",
            ["single","married","divorced"]
        )

        city = st.selectbox(
            "City",
            ["Rabat","Casablanca","Tangier","Agadir","Marrakech"]
        )

    property_type = st.selectbox(
        "Property Type",
        ["apartment","villa","duplex","studio"]
    )

    st.markdown("---")

    if st.button(" Predict Prospect"):

        df = pd.DataFrame({
            "age":[age],
            "income":[income],
            "marital_status":[marital_status],
            "children":[children],
            "budget":[budget],
            "city":[city],
            "property_type":[property_type]
        })

        df_ml = pd.get_dummies(df)
        df_ml = df_ml.reindex(columns=model_columns, fill_value=0)

        pred = model.predict(df_ml)
        proba = model.predict_proba(df_ml)[0][1]

        if pred[0] == 1:
            st.success("✅ Client likely to BUY")
        else:
            st.error("❌ Client unlikely to buy")

        st.write("Probability:", round(proba*100,2), "%")

        # SAVE
        new_id = 1 if len(data)==0 else data["id"].max()+1

        df["id"] = new_id
        df["bought"] = pred[0]

        df = df[[
            "id","age","income","marital_status",
            "children","budget","city","property_type","bought"
        ]]

        data2 = pd.concat([data, df], ignore_index=True)

        try:
            data2.to_csv("real_estate_prospects.csv", sep=";", index=False)
            data2.to_excel("real_estate_prospects.xlsx", index=False)
            st.success("✔ Saved successfully")
        except:
            st.warning("⚠️ Close Excel file")

# =============================
#  DASHBOARD PRO
# =============================
elif st.session_state.page == "Dashboard":

    st.markdown("##  Advanced Dashboard")

    if len(data) == 0:
        st.warning("No data available")
    else:

        # FILTERS
        st.sidebar.header("Filters")

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

        df = data[
            (data["city"].isin(city_filter)) &
            (data["property_type"].isin(property_filter))
        ]

        # METRICS
        col1, col2, col3 = st.columns(3)

        col1.metric("Total", len(df))

        if len(df) > 0:
            col2.metric("Buy %", round(df["bought"].mean()*100,2))
            col3.metric("Avg Budget", round(df["budget"].mean(),0))
        else:
            col2.metric("Buy %", 0)
            col3.metric("Avg Budget", 0)

        st.markdown("---")

        # BAR CHARTS
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("By City")
            st.bar_chart(df["city"].value_counts())

        with col2:
            st.subheader("Property Types")
            st.bar_chart(df["property_type"].value_counts())

        st.markdown("---")

        # DONUT
        def donut(data_counts):
            fig, ax = plt.subplots()

            ax.pie(
                data_counts,
                labels=data_counts.index,
                autopct='%1.1f%%',
                wedgeprops=dict(width=0.4)
            )

            centre_circle = plt.Circle((0,0),0.70,fc='#0E1117')
            fig.gca().add_artist(centre_circle)

            ax.axis('equal')
            st.pyplot(fig)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Buy vs Not Buy")
            donut(df["bought"].value_counts())

        with col2:
            st.subheader("Cities Distribution")
            donut(df["city"].value_counts())

# =============================
#  DATASET
# =============================
elif st.session_state.page == "Dataset":

    st.markdown("##  Dataset")

    search = st.text_input("Search by city")

    df = data.copy()

    if search:
        df = df[df["city"].str.contains(search, case=False)]

    st.dataframe(df)

    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        "dataset.csv"
    )