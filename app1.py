import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ================================
# Load & Clean Data FIRST
# ================================
df = pd.read_csv(r"E:\internship modules\NassauCandyDistributor.csv")

df.columns = df.columns.str.strip()
df = df.dropna()

df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')

df['Lead_Time'] = (df['Ship Date'] - df['Order Date']).dt.days

# ================================
# Title
# ================================
st.title("Nassau Candy Factory Optimization Dashboard")

# ================================
# Filters
# ================================
selected_region = st.selectbox("Select Region", df['Region'].unique())
selected_division = st.multiselect("Select Division(s)", df['Division'].unique(), default=df['Division'].unique())
selected_ship_mode = st.selectbox("Select Ship Mode", df['Ship Mode'].unique())

# ================================
# Apply Filters
# ================================
filtered_df = df[
    (df['Region'] == selected_region) &
    (df['Division'].isin(selected_division)) &
    (df['Ship Mode'] == selected_ship_mode)
]

st.write("Filtered Data Preview:", filtered_df.head())

# ================================
# KPI (USE FILTERED DATA)
# ================================
st.header("📊 KPI Dashboard")

avg_lead = filtered_df['Lead_Time'].mean()
median_lead = filtered_df['Lead_Time'].median()
profit_std = filtered_df['Gross Profit'].std()
coverage = filtered_df['Product Name'].nunique() / len(filtered_df)

st.metric("Average Lead Time", round(avg_lead, 2))
st.metric("Median Lead Time", round(median_lead, 2))
st.metric("Profit Stability", round(profit_std, 2))
st.metric("Coverage", f"{coverage:.2%}")

# ================================
# Example Chart (FIXED)
# ================================
st.subheader("Sales by Region")

sales_region = filtered_df.groupby('Region')['Sales'].sum()

plt.figure(figsize=(8,5))
sales_region.plot(kind='bar')
st.pyplot(plt)

# ================================
# Product Analysis (FIXED)
# ================================
st.subheader("Top Products by Sales")

product_sales = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False)

plt.figure(figsize=(10,5))
product_sales.head(10).plot(kind='bar')
plt.xticks(rotation=45)
st.pyplot(plt)

# Profit by division
profit_division = df.groupby('Division')['Gross Profit'].sum()
plt.figure(figsize=(6,6))
profit_division.plot(kind='pie', autopct='%1.1f%%', startangle=90, cmap="Set3")
plt.title("Profit Share by Division")
plt.ylabel("")
plt.show()
st.pyplot(plt)

# Lead time distribution
plt.figure(figsize=(8,5))
sns.histplot(df['Lead_Time'], bins=30, kde=True, color="skyblue")
plt.title("Distribution of Shipping Lead Times")
plt.xlabel("Lead Time (days)")
plt.ylabel("Frequency")
plt.show()
st.pyplot(plt)

# Average Lead Time per Region
avg_lead_region = filtered_df.groupby('Region')['Lead_Time'].mean().sort_values(ascending=False)
st.subheader("Average Lead Time per Region")
st.write(avg_lead_region)

# Top 10 slowest shipping products
slow_products =filtered_df.groupby('Product Name')['Lead_Time'].mean().sort_values(ascending=False).head(10)
st.subheader("Top 10 Slowest Shipping Products")
st.write(slow_products)

# Profitability by division
factory_profit =filtered_df.groupby('Division')['Gross Profit'].sum()
st.subheader("Profitability by Division")
st.write(factory_profit)

# --- Profit by Product ---
product_profit = filtered_df.groupby('Product Name')['Gross Profit'].sum().sort_values(ascending=False)

st.subheader("Top 10 Products by Profit")
plt.figure(figsize=(11,6))
product_profit.head(10).plot(kind='bar', color="green")
plt.title("Top 10 Products by Profit")
plt.ylabel("Gross Profit")
plt.xticks(rotation=45)
st.pyplot(plt)

# --- Lead Time by Product ---
product_lead =filtered_df.groupby('Product Name')['Lead_Time'].mean().sort_values(ascending=False)

st.subheader("Products with Longest Average Lead Time")
plt.figure(figsize=(11,6))
product_lead.head(10).plot(kind='bar', color="red")
plt.title("Products with Longest Average Lead Time")
plt.ylabel("Average Lead Time (days)")
plt.xticks(rotation=45)
st.pyplot(plt)

# --- Profit Margin by Product ---
df['Profit_Margin'] = df['Gross Profit'] / df['Sales']
product_margin = df.groupby('Product Name')['Profit_Margin'].mean().sort_values(ascending=False)

st.subheader("Products with Highest Profit Margin")
plt.figure(figsize=(11,6))
product_margin.head(10).plot(kind='bar', color="purple")
plt.title("Products with Highest Profit Margin")
plt.ylabel("Profit Margin")
plt.xticks(rotation=45)
st.pyplot(plt)

# 9. Factory Efficiency Comparison
# ================================

# Average lead time per factory
factory_lead = df.groupby('Division')['Lead_Time'].mean()

# Total profit per factory
factory_profit = df.groupby('Division')['Gross Profit'].sum()

# Combine into one table
factory_kpi = pd.DataFrame({
    "Average Lead Time (days)": factory_lead.round(2),
    "Total Profit Contribution": factory_profit.round(2)
})

# Display table in Streamlit
st.header("🏭 Factory Efficiency Comparison")
st.table(factory_kpi)

# Visualize as bar charts
st.subheader("Average Lead Time by Factory")
plt.figure(figsize=(8,5))
factory_lead.plot(kind='bar', color="skyblue")
plt.title("Average Lead Time by Factory")
plt.ylabel("Days")
plt.xticks(rotation=45)
st.pyplot(plt)

# Profit comparison
st.subheader("Total Profit Contribution by Factory")
plt.figure(figsize=(8,5))
factory_profit.plot(kind='bar', color="green")
plt.title("Total Profit Contribution by Factory")
plt.ylabel("Gross Profit")
plt.xticks(rotation=45)
st.pyplot(plt)

