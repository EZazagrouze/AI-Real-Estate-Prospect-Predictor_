import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Configuration page
# -----------------------------

st.set_page_config(
    page_title="AI Real Estate Predictor",
    page_icon="🏠",
    layout="wide"
)

# -----------------------------
# Charger modèle
# -----------------------------

model = joblib.load("model.pkl")
model_columns = joblib.load("columns.pkl")

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("🏠 AI Real Estate")

st.sidebar.info(
"""
Real Estate Prospect Prediction System

This AI predicts if a prospect is likely to buy a property.
"""
)

# -----------------------------
# Titre
# -----------------------------

st.title("AI Real Estate Prospect Predictor")

# -----------------------------
# Formulaire
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 18, 100)
    income = st.number_input("Income")

    children = st.number_input(
        "Children",
        0,
        10
    )

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

predict = st.button("🔮 Predict Prospect")

# -----------------------------
# Prediction
# -----------------------------

if predict:

    data_input = {
        "age":[age],
        "income":[income],
        "marital_status":[marital_status],
        "children":[children],
        "budget":[budget],
        "city":[city],
        "property_type":[property_type]
    }

    df = pd.DataFrame(data_input)

    df_ml = pd.get_dummies(df)
    df_ml = df_ml.reindex(columns=model_columns, fill_value=0)

    prediction = model.predict(df_ml)

    probability = model.predict_proba(df_ml)[0][1]

    if prediction[0] == 1:
        st.success("✅ Client likely to BUY")
    else:
        st.error("❌ Client unlikely to buy")

    st.write(
        "Probability of buying:",
        round(probability*100,2),
        "%"
    )

    # -----------------------------
    # Sauvegarde dataset
    # -----------------------------

    dataset = pd.read_csv(
        "real_estate_prospects.csv",
        sep=";",
        encoding="utf-8-sig"
    )

    dataset.columns = dataset.columns.str.strip()

    new_id = dataset["id"].max() + 1

    df["id"] = new_id
    df["bought"] = prediction[0]

    df = df[
        [
            "id",
            "age",
            "income",
            "marital_status",
            "children",
            "budget",
            "city",
            "property_type",
            "bought"
        ]
    ]

    dataset = pd.concat(
        [dataset, df],
        ignore_index=True
    )

    dataset.to_csv(
        "real_estate_prospects.csv",
        sep=";",
        index=False
    )

    dataset.to_excel(
        "real_estate_prospects.xlsx",
        index=False
    )

    st.success("Prospect ajouté au dataset")

# -----------------------------
# Charger dataset
# -----------------------------

data = pd.read_csv(
    "real_estate_prospects.csv",
    sep=";",
    encoding="utf-8-sig"
)

data.columns = data.columns.str.strip()

# -----------------------------
# Dataset
# -----------------------------

st.markdown("## 📋 Prospects Dataset")

st.dataframe(data)

# -----------------------------
# Statistiques
# -----------------------------

st.markdown("## 📊 Key Statistics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Prospects",
    len(data)
)

col2.metric(
    "Buy Rate (%)",
    round(data["bought"].mean()*100,2)
)

col3.metric(
    "Average Budget",
    round(data["budget"].mean(),0)
)

# -----------------------------
# Graphiques
# -----------------------------

st.markdown("## 📈 Dataset Statistics")

col1, col2 = st.columns(2)

with col1:
    st.write("Prospects by City")
    st.bar_chart(
        data["city"].value_counts()
    )

with col2:
    st.write("Property Types")
    st.bar_chart(
        data["property_type"].value_counts()
    )

st.write("Buy Rate")
st.bar_chart(
    data["bought"].value_counts()
)