import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 28th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# copy original dataframe before as_index=False
df_original = df.copy()

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

# 1. Add Drop Down for Category 
# Extract unique category values
categories = df_original["Category"].unique()

# Streamlit dropdown widget
selected_category = st.selectbox("Choose a Category", categories)

# Filter data based on selection
filtered_df = df[df["Category"] == selected_category]

# Refine- Choose Sub-Categories
# 2.1 Get sub-categories from filtered category data
subcategories = filtered_df["Sub_Category"].unique()

# Create a multiselect sub-categories
selected_subcategories = st.multiselect(
        "Choose Sub-Categories",
        subcategories,
        default = subcategories # pre-selected all to show full chart by default
)

# 2.2 Filter Data based on Multi-selection
filtered_df_subcat = filtered_df[filtered_df["Sub_Category"].isin(selected_subcategories)]

# 3. Line Chart Visual to show multi-selected sub-categories
# 3.1 Aggregate Sales by selected Sub_Category
subcat_sales = filtered_df_subcat.groupby("Sub_Category", as_index=False)["Sales"].sum()

# Set Sub_Category as index for line_chart to recognize x-axis
subcat_sales.set_index("Sub_Category", inplace=True)

# 3.2 Create Line Chart Visual
st.write(f"### Sales by Sub_Category ({selected_category})")
st.line_chart(subcat_sales)


# 4. Computer Three Metrics
total_sales = filtered_df_subcat["Sales"].sum()
total_profit = filtered_df_subcat["Profit"].sum()

# 4.1 Calculate overall profit margin (%)
profit_margin = (total_profit/ total_sales) * 100 if total_sales > 0 else 0

# 4.2 Display Metrics
st.write("### Key Metrics for Selected Sub-Categories")
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales: ", f"${total_sales:,.2f}")
col2.metric("Total Profit:",f"${total_profit:,.2f}")
col3.metric("Profit Margin (%):", f"${profit_margin:,.2f}")

# 5 Overall Profit Margin
overall_sales = df["Sales"].sum()
overall_profit = df["Profit"].sum()
overall_margin = (overall_profit / overall_sales) * 100 if overall_sales > 0 else 0

# Calculate Delta = difference between selected and overall margin
margin_delta = profit_margin - overall_margin

# Display profit margin with comparison
col3.metric(
      label ="Profit Margin (%)",
    value=f"{profit_margin:.2f}%",
    delta=f"{margin_delta:+.2f}%"
)

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
