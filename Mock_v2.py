#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Load the Excel data
@st.cache_data
def load_data():
    return pd.read_excel("soft_material_properties_sample.xlsx")

data = load_data()

# Sidebar for user input
st.sidebar.header("Explore the Database:")
x_axis = st.sidebar.selectbox(
    "Select X-axis:",
    options=["Particle_Size", "Aspect_Ratio", "Diffusivity", "Permeability", "Specificity", "Selectivity"]
)
y_axis = st.sidebar.selectbox(
    "Select Y-axis:",
    options=["Particle_Size", "Aspect_Ratio", "Diffusivity", "Permeability", "Specificity", "Selectivity"]
)
size = st.sidebar.selectbox(
    "Select Data for Size:",
    options=[None, "Particle_Size", "Aspect_Ratio"]
)
color = st.sidebar.selectbox(
    "Select Data for Color:",
    options=[None, "Specificity", "Selectivity"]
)
particle_filter = st.sidebar.multiselect(
    "Filter by Particle Used:",
    options=data["Particle_Used"].unique(),
    default=data["Particle_Used"].unique()
)

# Additional input for custom particle size and permeability
st.sidebar.header("Custom Data Point:")
custom_particle_size = st.sidebar.number_input("Enter Particle Size", min_value=0.0, value=1.0)
custom_permeability = st.sidebar.number_input("Enter Permeability", min_value=0.0, value=1.0)

# Filter the data based on user input
filtered_data = data[data["Particle_Used"].isin(particle_filter)]

# Main visualization
st.header("Interactive Visualization")

if x_axis and y_axis:
    # Base scatter plot with existing data
    fig = px.scatter(
        filtered_data,
        x=x_axis,
        y=y_axis,
        size=size,
        color=color,
        hover_name="Particle_Used",
        title=f"{y_axis} vs {x_axis}",
        template="plotly_white"
    )
    
    # Add the custom data point as a new trace
    fig.add_trace(
        go.Scatter(
            x=[custom_particle_size],
            y=[custom_permeability],
            mode='markers',
            marker=dict(
                size=15,
                color='red',  # Distinct color for the custom data point
                symbol='star'  # Distinct marker shape
            ),
            name='User Input'
        )
    )
    
    # Show the plot
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Please select both X-axis and Y-axis to view the chart.")

# Additional feature: Show the filtered data
st.subheader("Filtered Data Table")
st.dataframe(filtered_data)

# Optional: Download filtered data
# @st.cache
# def convert_df(df):
#     return df.to_csv(index=False).encode('utf-8')

# csv_data = convert_df(filtered_data)
# st.download_button(
#     label="Download Filtered Data as CSV",
#     data=csv_data,
#     file_name="filtered_data.csv",
#     mime="text/csv"
# )

