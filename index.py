import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to load dataset
def load_dataset(key):
    file_path = st.file_uploader("Upload CSV file", key=key, type=["csv"])
    if file_path is not None:
        return pd.read_csv(file_path)

# Function to explore data
def explore_data(loaded_dataset):
    st.subheader("Data Exploration")
    st.write(loaded_dataset.head())

# Function to visualize yearly medical cost
def visualize_yearly_medical_cost(loaded_dataset):
    if loaded_dataset is not None:
        yearly_costs = loaded_dataset.groupby('Year')['Medical_Cost'].sum()
        st.subheader("Year-wise Medical Cost")
        fig, ax = plt.subplots()
        bar_chart = ax.bar(yearly_costs.index, yearly_costs.values, color='skyblue')
        for bar, cost in zip(bar_chart, yearly_costs.values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05, f"${cost:.2f}", ha='center', va='bottom')
        ax.tick_params(axis='both', which='major', labelsize=12)
        st.pyplot(fig)

# Function to visualize age-wise medical cost
def visualize_age_wise_medical_cost(loaded_dataset):
    if loaded_dataset is not None:
        age_wise_costs = loaded_dataset.groupby('Age')['Medical_Cost'].sum()
        st.subheader("Age-wise Medical Cost")
        fig, ax = plt.subplots()
        bar_chart = ax.bar(age_wise_costs.index, age_wise_costs.values, color='skyblue')
        for bar, cost in zip(bar_chart, age_wise_costs.values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05, f"${cost:.2f}", ha='center', va='center')
        ax.tick_params(axis='both', which='major', labelsize=12)
        st.pyplot(fig)

# Function to visualize gender-wise medical cost
def visualize_gender_wise_medical_cost(loaded_dataset):
    if loaded_dataset is not None:
        gender_wise_costs = loaded_dataset.groupby('Gender')['Medical_Cost'].sum()
        st.subheader("Gender-wise Medical Cost")
        fig, ax = plt.subplots()
        bar_chart = ax.bar(gender_wise_costs.index, gender_wise_costs.values, color='skyblue')
        for bar, cost in zip(bar_chart, gender_wise_costs.values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05, f"${cost:.2f}", ha='center', va='bottom')
        ax.tick_params(axis='both', which='major', labelsize=12)
        st.pyplot(fig)

# Function to visualize disease-wise medical cost
def visualize_disease_wise_medical_cost(loaded_dataset):
    if loaded_dataset is not None:
        disease_wise_costs = loaded_dataset.groupby('Disease_Name')['Medical_Cost'].sum()
        st.subheader("Disease-wise Medical Cost")
        fig, ax = plt.subplots()
        bar_chart = ax.barh(disease_wise_costs.index, disease_wise_costs.values, color='skyblue')
        for bar, cost in zip(bar_chart, disease_wise_costs.values):
            ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f"${cost:.2f}", va='center', ha='left')
        ax.tick_params(axis='both', which='major', labelsize=12)
        st.pyplot(fig)

# Function to visualize yearly disease distribution
def visualize_yearly_disease_distribution(year, loaded_dataset):
    if loaded_dataset is not None:
        yearly_data = loaded_dataset[loaded_dataset['Year'] == year]
        if yearly_data.empty:
            st.info(f"No records available for year {year}.")
            return
        yearly_grouped = yearly_data.groupby('Disease_Name')['Medical_Cost'].sum().reset_index()
        st.subheader(f'Disease-wise Medical Cost for Year {year}')
        fig, ax = plt.subplots(figsize=(15, 15))
        bar_chart = ax.barh(yearly_grouped['Disease_Name'], yearly_grouped['Medical_Cost'], color='skyblue')
        # Annotate the bar with the highest total cost
        max_cost_index = yearly_grouped['Medical_Cost'].idxmax()
        max_cost_disease = yearly_grouped.loc[max_cost_index, 'Disease_Name']
        max_cost = yearly_grouped.loc[max_cost_index, 'Medical_Cost']
        st.write(f"Highest Total Cost Disease for Year {year}: {max_cost_disease} (${max_cost:.2f})")
        for bar, cost in zip(bar_chart, yearly_grouped['Medical_Cost']):
            ax.text(cost, bar.get_y() + bar.get_height() / 2, f"${cost:.2f}", va='center', ha='left', color='black', fontsize=20)
        ax.set_xlabel('Medical Cost', fontsize=14)
        ax.set_ylabel('Disease', fontsize=14)  # Increase font size here
        ax.tick_params(axis='both', which='major', labelsize=20)
        st.pyplot(fig)

# Function to find the threshold for every year
def find_threshold(loaded_dataset):
    if loaded_dataset is not None:
        st.subheader("Threshold for Every Year")
        yearly_thresholds = loaded_dataset.groupby('Year')['Medical_Cost'].quantile(0.75)
        fig, ax = plt.subplots()
        ax.plot(yearly_thresholds.index, yearly_thresholds.values, marker='o', color='red', linestyle='solid', linewidth=2, markersize=10)
        ax.fill_between(yearly_thresholds.index, yearly_thresholds.values, alpha=0.3)
        ax.set_xlabel('Year')
        ax.set_ylabel('Threshold')
        ax.set_title('Threshold for Every Year')
        ax.grid(True)
        st.pyplot(fig)

# Main function
def main():
    st.title("Medical Data Analysis")
    # Load dataset
    loaded_dataset = load_dataset("file_uploader1")
    if loaded_dataset is not None:
        explore_data(loaded_dataset)
        # Add buttons for each visualization function
        st.subheader("Visualizations:")
        if st.button("Visualize Yearly Medical Cost"):
            visualize_yearly_medical_cost(loaded_dataset)
        if st.button("Visualize Age-wise Medical Cost"):
            visualize_age_wise_medical_cost(loaded_dataset)
        if st.button("Visualize Gender-wise Medical Cost"):
            visualize_gender_wise_medical_cost(loaded_dataset)
        if st.button("Visualize Disease-wise Medical Cost"):
            visualize_disease_wise_medical_cost(loaded_dataset)
        year = st.number_input("Enter the year:", min_value=int(loaded_dataset['Year'].min()), max_value=int(loaded_dataset['Year'].max()))
        if st.button("Visualize Yearly Disease Distribution"):
            visualize_yearly_disease_distribution(year, loaded_dataset)
        if st.button("Find Threshold for Every Year"):
            find_threshold(loaded_dataset)

if __name__ == "__main__":
    main()
