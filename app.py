import streamlit as st
import pandas as pd
import plotly.express as px

# Load and clean the data
def load_data():
    df = pd.read_csv("V.DEF_train.csv")

    # Clean 'Time_taken(min)'
    df['Time_taken(min)'] = df['Time_taken(min)'].str.extract('(\\d+)').astype(float)

    # Convert data types
    df['Delivery_person_Age'] = pd.to_numeric(df['Delivery_person_Age'], errors='coerce')
    df['Delivery_person_Ratings'] = pd.to_numeric(df['Delivery_person_Ratings'], errors='coerce')
    df['multiple_deliveries'] = pd.to_numeric(df['multiple_deliveries'], errors='coerce')

    # Convert dates and times
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    df['Time_Orderd'] = pd.to_datetime(df['Order_Date'].astype(str) + ' ' + df['Time_Orderd'], errors='coerce')
    df['Time_Order_picked'] = pd.to_datetime(df['Order_Date'].astype(str) + ' ' + df['Time_Order_picked'], errors='coerce')

    # Drop rows with nulls in key columns
    df.dropna(subset=['Time_taken(min)', 'Delivery_person_Age', 'Delivery_person_Ratings'], inplace=True)

    return df

# Streamlit config
st.set_page_config(page_title="Delivery Dashboard", layout="wide")
st.title("📦 Food Delivery Insights Dashboard")

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")
selected_city = st.sidebar.multiselect("Select City", df['City'].unique(), default=df['City'].unique())
selected_type = st.sidebar.multiselect("Select Order Type", df['Type_of_order'].unique(), default=df['Type_of_order'].unique())

# Apply filters
filtered_df = df[(df['City'].isin(selected_city)) & (df['Type_of_order'].isin(selected_type))]

# Tabs
tab1, tab2 = st.tabs(["Delivery Time", "Rider Performance"])

with tab1:
    st.subheader("📊 Delivery Time Distribution")
    st.plotly_chart(px.histogram(filtered_df, x="Time_taken(min)", nbins=30, title="Delivery Time (Minutes)"))

    st.subheader("📍 Delivery Time by City")
    st.plotly_chart(px.box(filtered_df, x="City", y="Time_taken(min)", color="City"))

    st.subheader("🛍️ Avg Delivery Time by Order Type")
    st.plotly_chart(px.bar(filtered_df.groupby("Type_of_order")["Time_taken(min)"].mean().reset_index(),
                           x="Type_of_order", y="Time_taken(min)", title="Avg Time by Order Type"))

with tab2:
    st.subheader("👤 Rider Age vs Delivery Time")
    st.plotly_chart(px.scatter(filtered_df, x="Delivery_person_Age", y="Time_taken(min)", color="City"))

    st.subheader("⭐ Ratings vs Delivery Time")
    st.plotly_chart(px.scatter(filtered_df, x="Delivery_person_Ratings", y="Time_taken(min)", color="Type_of_vehicle"))
