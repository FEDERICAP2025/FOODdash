import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
def load_data():
    url = 'https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/main/V.DEF_train.csv'
    df = pd.read_csv(url)

    df['Time_taken(min)'] = df['Time_taken(min)'].str.extract('(\d+)').astype(float)
    df['Delivery_person_Age'] = pd.to_numeric(df['Delivery_person_Age'], errors='coerce')
    df['Delivery_person_Ratings'] = pd.to_numeric(df['Delivery_person_Ratings'], errors='coerce')
    df['multiple_deliveries'] = pd.to_numeric(df['multiple_deliveries'], errors='coerce')

    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    df['Time_Orderd'] = pd.to_datetime(df['Order_Date'].astype(str) + ' ' + df['Time_Orderd'], errors='coerce')
    df['Time_Order_picked'] = pd.to_datetime(df['Order_Date'].astype(str) + ' ' + df['Time_Order_picked'], errors='coerce')

    df.dropna(subset=['Time_taken(min)', 'Delivery_person_Age', 'Delivery_person_Ratings'], inplace=True)
    return df

# Sidebar filters
def sidebar_filters(df):
    st.sidebar.header("Filters")
    city = st.sidebar.multiselect("Select City", options=df['City'].unique(), default=df['City'].unique())
    order_type = st.sidebar.multiselect("Select Order Type", options=df['Type_of_order'].unique(), default=df['Type_of_order'].unique())
    weather = st.sidebar.multiselect("Weather", options=df['Weatherconditions'].unique(), default=df['Weatherconditions'].unique())
    traffic = st.sidebar.multiselect("Traffic Density", options=df['Road_traffic_density'].unique(), default=df['Road_traffic_density'].unique())
    return df[(df['City'].isin(city)) & (df['Type_of_order'].isin(order_type)) & (df['Weatherconditions'].isin(weather)) & (df['Road_traffic_density'].isin(traffic))]

# Main dashboard
st.set_page_config(layout="wide", page_title="Delivery Dashboard")
st.title("📦 Food Delivery Insights Dashboard")

# Load and filter data
df = load_data()
df_filtered = sidebar_filters(df)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Delivery Time", "Rider Performance", "Traffic & Weather", "Order & Geography"])

with tab1:
    st.subheader("📈 Delivery Time Analysis")
    st.write("This section explores delivery durations in various scenarios.")
    st.plotly_chart(px.histogram(df_filtered, x='Time_taken(min)', nbins=40, title='Delivery Time Distribution'))
    st.plotly_chart(px.box(df_filtered, x='City', y='Time_taken(min)', title='Delivery Time by City'))
    st.plotly_chart(px.bar(df_filtered.groupby('Type_of_order')['Time_taken(min)'].mean().reset_index(), x='Type_of_order', y='Time_taken(min)', title='Avg Delivery Time by Order Type'))
    st.plotly_chart(px.line(df_filtered.groupby('Order_Date')['Time_taken(min)'].mean().reset_index(), x='Order_Date', y='Time_taken(min)', title='Daily Avg Delivery Time'))

with tab2:
    st.subheader("🚴 Rider Performance")
    st.write("Understand how rider attributes affect delivery time.")
    st.plotly_chart(px.scatter(df_filtered, x='Delivery_person_Age', y='Time_taken(min)', color='City', title='Age vs Delivery Time'))
    st.plotly_chart(px.scatter(df_filtered, x='Delivery_person_Ratings', y='Time_taken(min)', color='Type_of_vehicle', title='Ratings vs Delivery Time'))
    st.plotly_chart(px.bar(df_filtered.groupby('Vehicle_condition')['Delivery_person_Ratings'].mean().reset_index(), x='Vehicle_condition', y='Delivery_person_Ratings', title='Avg Ratings by Vehicle Condition'))
    leaderboard = df_filtered.groupby('Delivery_person_ID')[['Time_taken(min)', 'Delivery_person_Ratings']].mean().reset_index().sort_values('Time_taken(min)')
    st.dataframe(leaderboard.head(10), use_container_width=True)

with tab3:
    st.subheader("🌦️ Traffic & Weather Impact")
    st.write("Analysis of environmental conditions on delivery times.")
    st.plotly_chart(px.box(df_filtered, x='Weatherconditions', y='Time_taken(min)', title='Delivery Time by Weather'))
    st.plotly_chart(px.box(df_filtered, x='Road_traffic_density', y='Time_taken(min)', title='Delivery Time by Traffic Density'))
    st.plotly_chart(px.bar(df_filtered.groupby(['Road_traffic_density', 'City'])['Time_taken(min)'].mean().reset_index(), 
                           x='Road_traffic_density', y='Time_taken(min)', color='City', barmode='group', title='Traffic vs Delivery Time by City'))

with tab4:
    st.subheader("🗺️ Orders & Geography")
    st.write("Explore spatial and order-related trends.")
    st.plotly_chart(px.pie(df_filtered, names='Festival', title='Festival vs Non-Festival Deliveries'))
    st.plotly_chart(px.violin(df_filtered, y='Delivery_person_Age', x='City', box=True, title='Rider Age Distribution by City'))
    st.plotly_chart(px.scatter_geo(df_filtered.head(500), 
                                   lat='Restaurant_latitude', lon='Restaurant_longitude', 
                                   hover_name='City', title='Sample Restaurant Locations'))
