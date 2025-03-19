# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10ZEZwlFUYXezlRnnh1Q3SenePT6K3ndY

- **Name: Aashi Talwar**
- **Data Science Major Project**
- **Title: Recommendation System**





---

### Online Retail Recommendation System Project

- **1. Project Goal and Dataset**


Goal: I have developed a recommendation system to suggest products to online shoppers, similar to features on popular e-commerce websites. This system aims to improve user experience and potentially drive sales.
Dataset: I have utilized the "Online Retail" dataset from Kaggle for this project. This dataset provides valuable transactional information about an online retail store.
Columns: I have worked with columns such as invoice number, product descriptions, quantities, customer IDs, and countries, each of which played a crucial role in building the recommendation system.

- **2. Data Preprocessing and Exploration**

Data Cleaning: I have cleaned the data by handling missing values in the 'CustomerID' column, removing duplicates, and converting the 'InvoiceDate' to a suitable format for analysis.
Exploratory Data Analysis (EDA): I have explored the dataset to gain insights into product popularity. I have identified globally popular items, country-wise popular items, and month-wise popular items. To visualize these trends, I have used Seaborn and Matplotlib libraries to create bar plots and heatmaps.

- **3. Recommendation System Development**

Data Sampling: I have sampled 20% of the original dataset to ensure faster processing during the model development and testing phase.
Feature Engineering: To build the recommendation system, I have focused on product descriptions.
TF-IDF Vectorization: I have used TF-IDF to convert product descriptions into numerical vectors, which enable comparisons based on word importance.
Dimensionality Reduction: I have applied Truncated SVD to reduce the complexity of the data and improve efficiency.
Similarity Calculation (KNN):
I have implemented the K-Nearest Neighbors algorithm with cosine similarity to identify products similar to a given product. This approach leverages the reduced TF-IDF vectors to find neighbors in the product space.

- **4. User Input and Recommendations**

Streamlit Integration: I have developed an interactive web application using Streamlit to showcase the recommendation system.
User Input: The application allows users to input a product name.
Product Matching: I have implemented fuzzy string matching to ensure accurate product identification, even with minor spelling errors in the user's input.
Recommendation Generation: Once a product is matched, the KNN model retrieves the most similar products based on the pre-calculated similarity matrix.
Displaying Recommendations: The application then displays these recommended products to the user.

- **5. Conclusion and Future Enhancements**

I have successfully built and deployed an online retail recommendation system using Python and Streamlit.
For future enhancements, I plan to explore other algorithms, incorporate user preferences, and improve the application's user interface.**

**Importing Necessary libraries**
"""

import streamlit as st
import pandas as pd
import numpy as np
import openpyxl 
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors
from thefuzz.process import extractOne




"""**Loading and Sampling the Dataset (20% for faster processing)**"""

# Step 1: Load and Sample the Dataset (20% for faster processing)
@st.cache_data
def load_data(uploaded_file):
    # Read the uploaded file
    df1 = pd.read_excel(uploaded_file)
    # Sample 20% of the data
    df1 = df1.sample(frac=0.2, random_state=42).reset_index(drop=True)
    return df1

# Streamlit app
st.title("Online Retail Data Processing")

# File uploader widget
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Load and process the data
    df1 = load_data(uploaded_file)
    
    # Display the sampled data
    st.write("Sampled Data (20% of the original dataset):")
    st.dataframe(df1)
else:
    st.write("Please upload an Excel file to proceed.")

# Step 2: Data Cleaning & Description
if df1 is not None:
    if "CustomerID" in df1.columns:
        df1.dropna(subset=["CustomerID"], inplace=True)
    else:
        st.warning("Column 'CustomerID' not found in the dataset. Skipping dropna operation.")

    df1.drop_duplicates(inplace=True)
else:
    st.error("Dataframe is empty. Please upload a valid file.")


# Convert Invoice Date to datetime and extract Month
df1["InvoiceDate"] = pd.to_datetime(df1["InvoiceDate"])
df1["Month"] = df1["InvoiceDate"].dt.month

"""**Finding Popular Items (Globally, Country-wise, Month-wise)**"""

# Step 3: Finding Popular Items (Globally, Country-wise, Month-wise)

## Globally Popular Items
popular_items_global1 = df1["Description"].value_counts().head(10)
popular_items_global1

"""**Country-wise Popular Items**"""

## Country-wise Popular Items
popular_items_country1 = df1.groupby("Country")["Description"].value_counts().groupby(level=0).head(3)
popular_items_country1

"""**Month-wise Popular Items**"""

## Month-wise Popular Items
popular_items_month1 = df1.groupby("Month")["Description"].value_counts().groupby(level=0).head(3)
popular_items_month1

# Step 4: Visualizations in Streamlit
st.title("🛍️ Retail Product Analysis & Recommendations")

st.subheader("Top 10 Globally Popular Products")
st.bar_chart(popular_items_global1)

st.subheader("Top Products by Country")
selected_country = st.selectbox("Select a country:", df["Country"].unique())
country_data = df[df["Country"] == selected_country]["Description"].value_counts().head(5)
st.bar_chart(country_data)

# Compute month-wise popular items
popular_items_month1 = df1.groupby("Month")["Description"].value_counts().groupby(level=0).head(3)

# Display in Streamlit
st.title("Month-wise Popular Items")
st.write(popular_items_month1)

# Step 4: Visualizations (Seaborn & Pivot Tables)

# Globally Popular Items
plt.figure(figsize=(10, 5))
sns.barplot(x=popular_items_global1.index, y=popular_items_global1.values, palette="viridis")
plt.xticks(rotation=90)
plt.title("Top 10 Popular Products Globally")
plt.xlabel("Products")
plt.ylabel("Count")
plt.show()

# Country-wise Popular Items (Example: UK)
plt.figure(figsize=(12, 6))
top_countries = df1["Country"].value_counts().head(3).index
for country in top_countries:
    country_data = df1[df1["Country"] == country]["Description"].value_counts().head(5)
    sns.barplot(x=country_data.index, y=country_data.values, label=country)

plt.xticks(rotation=90)
plt.title("Top 5 Products in Each Country")
plt.xlabel("Products")
plt.ylabel("Count")
plt.legend(title="Country")
plt.show()

"""**Recommendation System Optimization**"""

# Step 5: Recommendation System Optimization
vectorizer = TfidfVectorizer(stop_words='english')
item_vectors = vectorizer.fit_transform(df1["Description"].astype(str))
item_vectors

"""**Dimensionality Reduction**"""

# Dimensionality Reduction
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors
from thefuzz.process import extractOne
svd = TruncatedSVD(n_components=50, random_state=42)
item_vectors_reduced = svd.fit_transform(item_vectors)
item_vectors_reduced

"""**KNN Model for Similarity Search**"""

# KNN Model for Similarity Search
knn = NearestNeighbors(n_neighbors=6, metric='cosine')
knn.fit(item_vectors_reduced)

"""**User Input-based Recommendations**"""

# Step 6: User Input-based Recommendations
st.subheader("🔍 Product Recommendation System")
product_name = st.text_input("Enter a product name:", "")

def recommend_products(df):
    """User input-based product recommendation."""
    product_name = input("Enter a product name: ")
    closest_match, score = extractOne(product_name, df["Description"].unique())
    if score < 80:
        return print("Product not found in dataset")

    # Get the index of the matched product within the vectorized data
    descriptions = df["Description"].astype(str).unique()  # Get unique descriptions
    matched_index = np.where(descriptions == closest_match)[0][0]  # Find index of the matched description

    # Recalculate TF-IDF and reduce dimensions using the unique descriptions
    vectorizer = TfidfVectorizer(stop_words='english')
    item_vectors = vectorizer.fit_transform(descriptions)  # Vectorize unique descriptions
    svd = TruncatedSVD(n_components=50, random_state=42)
    item_vectors_reduced = svd.fit_transform(item_vectors)

    # KNN Model for Similarity Search
    knn = NearestNeighbors(n_neighbors=6, metric='cosine')
    knn.fit(item_vectors_reduced)

    distances, indices = knn.kneighbors([item_vectors_reduced[matched_index]])

    # Get recommendations from the unique descriptions and their indices
    top_products = [descriptions[i] for i in indices[0][1:6] if i < len(descriptions)]

    print("Recommended products:")
    for product in top_products:
        print(f"- {product}")

# Title for the Streamlit app
st.title("🔮 Predict & Recommend")

# Step 6: Predict & Recommend
if "df1" in locals() or "df1" in globals():  
    st.subheader("Recommended Products")
    recommendations = recommend_products(df)  # Assuming `recommend_products(df)` returns a DataFrame or list
    st.write(recommendations)
else:
    st.error("DataFrame not found! Please ensure `df1` is loaded before running recommendations.")
