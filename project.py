import kaggle
import pandas as pd
import streamlit as st
import pymysql
from sqlalchemy import create_engine 
from config import get_mysql_engine
import os

# os.environ['KAGGLE_USERNAME'] = os.getenv('KAGGLE_USERNAME')
# os.environ['KAGGLE_KEY'] = os.getenv('KAGGLE_KEY')

# Page config
st.set_page_config(
    page_title="Walmart",
    page_icon="🛒",
    layout="wide"
)

# Database engine
engine_mysql = get_mysql_engine()

# Session data
if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv("Walmart.csv", encoding_errors='ignore')

# Sidebar navigation
option = st.sidebar.radio("📂 Navigation", ["🏠 Home", "ℹ️ About", "📞 Contact", "📊 Generate Data"])

# ----------------------------- UI SECTIONS -----------------------------
def home():
    st.title("🏪 Walart Online Store")
    st.markdown("Welcome to **Walmart**, your one-stop solution for all your shopping needs.")

    with st.container():
        st.subheader("🛍 Product Overview")

        col1, col2 = st.columns(2)
        with col1:
            show_products = st.toggle("Show Products")
            if show_products:
                st.dataframe(st.session_state.df.head(8), hide_index=True, use_container_width=True)

        with col2:
            show_shape = st.toggle("Show Dataset Info")
            if show_shape:
                st.write("🧾 Rows:", st.session_state.df.shape[0])
                st.write("🧾 Columns:", st.session_state.df.shape[1])

    with st.expander("🔍 Data Cleaning & Insights"):
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔁 Remove Duplicates"):
                if st.session_state.df.duplicated().sum() == 0:
                    st.info("No duplicates found.")
                else:
                    st.session_state.df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed!")

            if st.button("📉 Drop Null Records"):
                before = len(st.session_state.df)
                st.session_state.df.dropna(inplace=True)
                dropped = before - len(st.session_state.df)
                st.success(f"Dropped {dropped} records with null values.")

        with col2:
            if st.button("📊 Show Null Values"):
                st.dataframe(st.session_state.df.isnull().sum().reset_index(), hide_index=True)

            if st.button("💲 Clean Currency"):
                st.session_state.df['unit_price'] = st.session_state.df['unit_price'].str.replace('$', '', regex=False).astype(float)
                st.success("Removed dollar signs.")

        with col3:
            if st.button("➕ Add Total Column"):
                st.session_state.df['total'] = st.session_state.df['unit_price'] * st.session_state.df['quantity']
                st.success("Total column added.")

            if st.button("💾 Save as CSV"):
                st.session_state.df.to_csv("Walmart_clean_data.csv", index=False)
                st.success("CSV file created.")

    with st.expander("🗃 Database Actions"):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔗 Upload to MySQL"):
                try:
                    st.session_state.df.to_sql('walmart', con=engine_mysql, if_exists='replace', index=False)
                    st.success("Data uploaded to MySQL successfully.")
                except Exception as e:
                    st.error(f"Upload failed: {e}")

        with col2:
            if st.button("🔤 Normalize Column Names"):
                st.session_state.df.columns = st.session_state.df.columns.str.lower()
                st.success("Column names converted to lowercase.")

    with st.expander("📈 Analytical Reports"):
        analysis_options = [
            "Group By Payment Method",
            "Top Rated Category per Branch",
            "Top Rated Day per Branch",
            "Quantity Sold per Payment Method",
            "Min/Max/Avg Rating per City and Category",
            "Total Revenue and Profit per Category",
            "Top Payment Method per Branch",
            "Total Transactions per Branch & Time",
            "Revenue: 2022 vs 2023"
        ]
        selected_analysis = st.selectbox("📊 Choose an analysis to run", analysis_options)

        queries = {
            "Group By Payment Method": """
                SELECT payment_method, COUNT(*) AS no_payments, SUM(quantity) AS no_qnty_sold 
                FROM walmart GROUP BY payment_method;
            """,
            "Top Rated Category per Branch": """
                SELECT * FROM (
                    SELECT branch, category, AVG(rating) AS avg_rating,
                    RANK() OVER (PARTITION BY branch ORDER BY AVG(rating) DESC) AS rnk
                    FROM walmart GROUP BY branch, category
                ) AS ranked WHERE rnk = 1;
            """,
            "Top Rated Day per Branch": """
                SELECT * FROM (
                    SELECT branch, DAYNAME(date) AS day_name, COUNT(*) AS total_sales,
                    RANK() OVER (PARTITION BY branch ORDER BY COUNT(*) DESC) AS rnk
                    FROM walmart GROUP BY branch, day_name
                ) AS ranked WHERE rnk = 1;
            """,
            "Quantity Sold per Payment Method": """
                SELECT payment_method, SUM(quantity) as no_of_quantity_sold 
                FROM walmart GROUP BY payment_method;
            """,
            "Min/Max/Avg Rating per City and Category": """
                SELECT city, category, MIN(rating) as min_rating, MAX(rating) as max_rating, AVG(rating) as avg_rating 
                FROM walmart GROUP BY city, category;
            """,
            "Total Revenue and Profit per Category": """
                SELECT category, SUM(total) as total_revenue, SUM(total * profit_margin) as profit 
                FROM walmart GROUP BY category ORDER BY profit DESC;
            """,
            "Top Payment Method per Branch": """
                WITH cte AS (
                    SELECT branch, payment_method, COUNT(*) AS total_trans, 
                    RANK() OVER(PARTITION BY branch ORDER BY COUNT(*) DESC) AS rnk 
                    FROM walmart GROUP BY branch, payment_method
                ) SELECT * FROM cte WHERE rnk = 1;
            """,
            "Total Transactions per Branch & Time": """
                SELECT branch,
                CASE
                    WHEN HOUR(TIME(time)) < 12 THEN 'Morning'
                    WHEN HOUR(TIME(time)) BETWEEN 12 AND 17 THEN 'Afternoon'
                    ELSE 'Evening'
                END AS day_time,
                COUNT(*) AS total_transactions
                FROM walmart
                GROUP BY branch, day_time
                ORDER BY branch, total_transactions DESC;
            """,
            "Revenue: 2022 vs 2023": """
                WITH revenue_2022 AS (
                    SELECT branch, SUM(total) AS revenue 
                    FROM walmart WHERE YEAR(STR_TO_DATE(date, '%%d/%%m/%%y')) = 2022 GROUP BY branch
                ),
                revenue_2023 AS (
                    SELECT branch, SUM(total) AS revenue 
                    FROM walmart WHERE YEAR(STR_TO_DATE(date, '%%d/%%m/%%y')) = 2023 GROUP BY branch
                )
                SELECT ls.branch, ls.revenue AS last_year_revenue, cs.revenue AS cr_year_revenue,
                ROUND((ls.revenue - cs.revenue) / ls.revenue * 100, 2) AS rev_dec_ratio
                FROM revenue_2022 AS ls
                JOIN revenue_2023 AS cs ON ls.branch = cs.branch
                WHERE ls.revenue > cs.revenue
                ORDER BY rev_dec_ratio DESC;
            """
        }

        if st.button("📥 Run Analysis"):
            try:
                df_result = pd.read_sql_query(queries[selected_analysis], engine_mysql)
                st.dataframe(df_result, use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"Query failed: {e}")

# ------------- About ----------------
def about():
    st.title("📘 About Walmart")
    st.write("""
    At Walmart, we're building a better world — helping people live healthier lives, promoting sustainability, and fostering community.
    """)
    st.subheader("🧑‍💼 Meet The Team")
    cols = st.columns(2)
    founders = [
        "Muhammad Rayyan Naveed",
        "Muhammad Saim Rao",
        "Muhammad Sajjid Jhedu",
        "Syed Zohaib Shah",
        "Shayan Meo Rajput"
    ]
    for i, name in enumerate(founders):
        cols[i % 1].markdown(f"##### ✅ **{name}**")

# -------------- Contact -------------------
def contact():
    st.title("📞 Contact Us")
    st.info("📧 Email: mygomart@gmail.com")
    st.info("📱 Phone: 111-555-898")

# -------------- Kaggle API Call ------------
def get_api_data(api):
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(api, path='.', unzip=True)

# --------------- Main -----------------------
def main():
    if option == "🏠 Home":
        home()
    elif option == "ℹ️ About":
        about()
    elif option == "📞 Contact":
        contact()
    elif option == "📊 Generate Data":
        st.title("📡 Generate Data from Kaggle API")
        st.markdown("Enter the Kaggle dataset API path to download and convert it into CSV format.")
        api = st.text_input("🔗 API Endpoint")
        if st.button("⬇️ Fetch Dataset"):
            if api:
                get_api_data(api)
                st.success("Dataset downloaded and unzipped.")
            else:
                st.warning("Please enter a valid API.")

if __name__ == "__main__":
    main()