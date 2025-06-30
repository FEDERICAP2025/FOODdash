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
    df['multiple_deliveries'] = pd.to_numeric(df['multiple_deliveries'], errors='coerc_]()]()
