#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from openpyxl import Workbook

# Load data from uploaded_data.xlsx
@st.cache_data
def load_uploaded_data():
    try:
        return pd.read_excel("uploaded_data.xlsx")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Paper DOI", "Particle_Used", "Particle_Size", "Aspect_Ratio", "Diffusivity", 
                                     "Permeability", "Polymer Network Mesh Size", "Specificity"])

# Save new data to uploaded_data.xlsx
def save_to_excel(data, file_name="uploaded_data.xlsx"):
    df = pd.DataFrame(data)
    try:
        existing_data = pd.read_excel(file_name)
        df = pd.concat([existing_data, df], ignore_index=True)
    except FileNotFoundError:
        pass  # If the file doesn't exist, create a new one
    df.to_excel(file_name, index=False, float_format="%.5f")

# Page title
st.markdown("<h1 style='text-align: center; font-size: 36px;'>The Dynamic Database of Molecular Transport Properties in Soft Materials</h1>", unsafe_allow_html=True)

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Explore the Database"

# Sidebar navigation
st.sidebar.markdown("## Navigation")
if st.sidebar.button("Explore the Database"):
    st.session_state["current_page"] = "Explore the Database"
if st.sidebar.button("Upload Data"):
    st.session_state["current_page"] = "Upload Data"

# Page: Explore the Database
if st.session_state["current_page"] == "Explore the Database":
    st.write("This page allows users to explore molecular transport properties in soft materials.")
    data = load_uploaded_data()

    if data.empty:
        st.warning("No data available! Please upload data in the 'Upload Data' page first.")
    else:
        # Sidebar input
        st.sidebar.header("Explore the Database:")
        x_axis = st.sidebar.selectbox("Select X-axis:", options=data.columns[2:])
        y_axis = st.sidebar.selectbox("Select Y-axis:", options=data.columns[2:])
        size = st.sidebar.selectbox("Select Data for Size:", options=[None] + list(data.columns[2:]))
        color = st.sidebar.selectbox("Select Data for Color:", options=[None] + list(data.columns[2:]))
        particle_filter = st.sidebar.multiselect("Filter by Particle Used:", options=data["Particle_Used"].dropna().unique())

        # Custom particle inputs
        st.sidebar.header("Evaluate your new particle:")
        custom_particle_size = st.sidebar.number_input("Enter Particle Size (nm)", min_value=0.0, step=0.00001, format="%.5f")
        custom_diffusivity = st.sidebar.number_input("Enter Diffusivity (m²/s)", min_value=0.0, step=0.00001, format="%.5f")
        custom_permeability = st.sidebar.number_input("Enter Permeability (m²)", min_value=0.0, step=0.00001, format="%.5f")

        # Filter data
        filtered_data = data[data["Particle_Used"].isin(particle_filter)] if particle_filter else data

        # Visualization
        st.markdown("<h2 style='text-align: center; font-size: 30px;'>Interactive Visualization</h2>", unsafe_allow_html=True)
        if x_axis and y_axis:
            fig = px.scatter(filtered_data, x=x_axis, y=y_axis, size=size, color=color, hover_name="Particle_Used", title=f"{y_axis} vs {x_axis}", template="plotly_white")
            fig.add_trace(go.Scatter(x=[custom_particle_size], y=[custom_permeability], mode='markers', marker=dict(size=15, color='red', symbol='star'), name='User Input'))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Please select both X-axis and Y-axis to view the chart.")
        st.subheader("Filtered Data Table")
        st.dataframe(filtered_data)

# Page: Upload Data
elif st.session_state["current_page"] == "Upload Data":
    st.write("This page allows users to upload new data.")
    with st.form("data_entry_form"):
        particle_used = st.text_input("Particle Used")
        particle_size = st.number_input("Particle Size (nm)", min_value=0.0, step=0.00001, format="%.5f")
        aspect_ratio = st.number_input("Aspect Ratio", min_value=0.0, step=0.00001, format="%.5f")
        diffusivity = st.number_input("Diffusivity (m²/s)", min_value=0.0, step=0.00001, format="%.5f")
        permeability = st.number_input("Permeability (m²)", min_value=0.0, step=0.00001, format="%.5f")
        polymer_network_mesh_size = st.number_input("Polymer Network Mesh Size (nm)", min_value=0.0, step=0.00001, format="%.5f")
        specificity = st.text_input("Specificity")
        paper_doi = st.text_input("Paper DOI", placeholder="e.g. 10.1016/j.jmps.2024.105732")
        submitted = st.form_submit_button("Submit Data")

    if submitted:
        new_data = {
            "Particle_Used": [particle_used.strip() if particle_used.strip() else None],
            "Particle_Size": [particle_size if particle_size else None],
            "Aspect_Ratio": [aspect_ratio if aspect_ratio else None],
            "Diffusivity": [diffusivity if diffusivity else None],
            "Permeability": [permeability if permeability else None],
            "Polymer Network Mesh Size": [polymer_network_mesh_size if polymer_network_mesh_size else None],
            "Specificity": [specificity.strip() if specificity else None],
            "Paper DOI": [paper_doi.strip() if paper_doi else None]
        }
        new_data = {k: v for k, v in new_data.items() if v}
        if new_data:
            save_to_excel(new_data)
            st.success("Data saved successfully to 'uploaded_data.xlsx'!")
            st.write(pd.DataFrame(new_data))
        else:
            st.error("Please fill at least one field to submit data!")

