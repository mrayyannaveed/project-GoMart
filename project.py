# import kaggle
# import pandas as pd
# import streamlit as st
# import pymysql
# from sqlalchemy import create_engine 

# st.set_page_config(
#     page_title="Go Mart",
#     page_icon="🧊",
#     layout="wide"
# )
# engine_mysql = create_engine('mysql+pymysql://root:phe9B%40rBit0ne@localhost:3306/walmart_db')

# # Initialize session state for the DataFrame if it doesn't exist
# if 'df' not in st.session_state:
#     st.session_state.df = pd.read_csv("Walmart.csv", encoding_errors='ignore')

# option = st.sidebar.radio("Select a page", ["Home", "About", "Contact", "Generate Data"])

# def home():
#     st.title("🏪Go Mart Online Store")
#     st.write("Welcome to Go Mart, your one-stop shop for all your grocery needs.")
    
#     st.markdown("### 🛒Our Products")
#     if st.checkbox(" Show Products"):
#         mydf = st.session_state.df.head(8)
#         st.dataframe(mydf, hide_index=True)
    
#     if st.checkbox("Show Rows and Columns"):
#         st.write("Number of Rows:", st.session_state.df.shape[0])
#         st.write("Number of Columns:", st.session_state.df.shape[1])
    
#     if st.checkbox("Show Stats"):
#         st.write(st.session_state.df.describe())
    
#     if st.checkbox("Show Duplicates"):
#         st.write("Number of Duplicates:", st.session_state.df.duplicated().sum())
    
#     if st.button("Remove Duplicates"):
#         if st.session_state.df.duplicated().sum() == 0:
#             st.warning("No duplicates found!")
#         else:
#             st.session_state.df = st.session_state.df.drop_duplicates()
#             st.success("Successfully removed duplicates!")
    
#     if st.button("Drop rows with missing records"):
#         # Store original row count
#         original_rows = st.session_state.df.shape[0]
        
#         # Drop null values
#         st.session_state.df = st.session_state.df.dropna()
        
#         # Calculate how many rows were dropped
#         dropped_rows = original_rows - st.session_state.df.shape[0]
        
#         st.success(f"Successfully dropped {dropped_rows} rows with missing values!")
#         # No need for rerun - Streamlit will automatically refresh
        
#     if st.button("Show Null Values"):
#         st.write("Number of Null Values:", st.session_state.df.isnull().sum())

#     if st.button("Replace Dollar"):
#         st.session_state.df['unit_price'] = st.session_state.df['unit_price'].str.replace('$', '').astype(float)
#         st.success("Successfully replaced dollar signs!")

#     if st.button("Add Total Column"):
#         st.session_state.df['total'] = st.session_state.df['unit_price'] * st.session_state.df['quantity']
#         st.success("Successfully added total column!")
    
#     if st.button("Create csv file"):
#         st.session_state.df.to_csv("Walmart_clean_data.csv", index=False)
#         st.success("Successfully created csv file!")
    
#     if st.button("Connect Database and Create Table"):
#         try:
#             engine_mysql

#             st.session_state.df.to_sql('walmart', con=engine_mysql, if_exists='replace', index=False)
#             st.success("Database connected successfully!")
            
#         except Exception as e:
#             st.error(f"Operation failed: {e}")
    
#     if st.button("Get Lower"):
#         st.session_state.df.columns = st.session_state.df.columns.str.lower()
#         st.success("Successfully converted to lowercase!")

#     if st.button("Get Group By"):
#         try:
#             query = """
#             SELECT 
#                 payment_method, 
#                 COUNT(*) AS no_payments, 
#                 SUM(quantity) AS no_qnty_sold 
#             FROM walmart 
#             GROUP BY payment_method;
#             """

#             df_grouped = pd.read_sql_query(query, engine_mysql)

#             # Show result on UI
#             st.subheader("💳 Payments Summary")
#             st.dataframe(df_grouped)

#         except Exception as e:
#             st.error(f"Error retrieving grouped data: {e}")

    
#     if st.button("Show Top Rated Category per Branch"):
#         try:
#             query = """
#             SELECT *
#             FROM (
#                 SELECT 
#                     branch, 
#                     category, 
#                     AVG(rating) AS avg_rating,
#                     RANK() OVER (PARTITION BY branch ORDER BY AVG(rating) DESC) AS rnk
#                 FROM walmart
#                 GROUP BY branch, category
#             ) ranked
#             WHERE rnk = 1;
#             """

#             # Read data using pandas
#             df_top = pd.read_sql_query(query, engine_mysql)

#             # Show result on UI
#             st.subheader("🏆 Top Rated Category per Branch")
#             st.dataframe(df_top, hide_index=True)

#         except Exception as e:
#             st.error(f"Error retrieving data: {e}")
#     if st.button("Show Top Rated Day per Branch"):
#         try:
#             query = """
#             SELECT *
#             FROM (
#                 SELECT
#                     branch,
#                     DAYNAME(date) AS day_name,
#                     COUNT(*) AS total_sales,
#                     RANK() OVER (PARTITION BY branch ORDER BY COUNT(*) DESC) AS rnk
#                 FROM walmart
#                 GROUP BY branch, day_name
#             ) AS ranked
#             WHERE rnk = 1;
#             """

#             # Read data using pandas
#             df_top = pd.read_sql_query(query, engine_mysql)

#             # Show result on UI
#             st.subheader("🏆 Top Rated Day per Branch")
#             st.dataframe(df_top, hide_index=True)

#         except Exception as e:
#             st.error(f"Error retrieving data: {e}")<e



# def about():
#     st.title("About US")
#     st.write("We aim to build a better world — helping people live better and renew the planet while building thriving, resilient communities. For us, this means working to create opportunity, build a more sustainable future, advance belonging and bring communities closer together.")
#     st.header("Go Mart Owner's 💰")
#     st.write("### Muhammad Rayyan Naveed") 
#     st.write("### Muhammad Saim Rao") 
#     st.write("### Muhammad Sajjid Jhedu") 
#     st.write("### Syed Zohaib Shah")
#     st.write("### Shayan Meo Rajput")

# def contact():
#     st.title("Contact Go Mart")
#     st.write("#### 📧mygomart@gmail.com")
#     st.write("#### 📞111-555-898")

# def get_api_data(api):
#         kaggle.api.authenticate()
#         kaggle.api.dataset_download_files(api, path='.', unzip=True)
    
# def main():
#     if option == "Home":
#         home()
#     elif option == "About":
#         about()
#     elif option == "Contact":
#         contact()
#     elif option == "Generate Data":
#         st.title("Generate Data Through API")
#         st.write("#### Enter the API to convert it into csv data format.")
#         api = st.text_input("Enter API")
#         if api:
#             get_api_data(api)
#         else:
#             st.success("Please enter an API")
    

# if __name__ == "__main__":
#     main()

import kaggle
import pandas as pd
import streamlit as st
import pymysql
from sqlalchemy import create_engine 

st.set_page_config(
    page_title="Go Mart",
    page_icon="🛒",
    layout="wide"
)

# Database engine
engine_mysql = create_engine('mysql+pymysql://root:phe9B%40rBit0ne@localhost:3306/walmart_db')

# Load dataset if not in session
if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv("Walmart.csv", encoding_errors='ignore')

# Sidebar navigation
option = st.sidebar.radio("📂 Navigation", ["🏠 Home", "ℹ️ About", "📞 Contact", "📤 Generate Data"])

def home():
    st.title("🏪 Welcome to Go Mart")
    st.caption("Your one-stop shop for all your grocery needs!")

    st.markdown("---")

    st.subheader("📊 Data Overview")
    with st.expander("🔍 Preview & Structure"):
        st.write("### Sample Products")
        st.dataframe(st.session_state.df.head(8), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rows", st.session_state.df.shape[0])
        with col2:
            st.metric("Columns", st.session_state.df.shape[1])

        if st.checkbox("Show Statistics Summary"):
            st.write(st.session_state.df.describe())

    with st.expander("🧹 Data Cleaning"):
        col1, col2, col3 = st.columns(3)

        if col1.button("Remove Duplicates"):
            count = st.session_state.df.duplicated().sum()
            if count > 0:
                st.session_state.df = st.session_state.df.drop_duplicates()
                st.success(f"✅ Removed {count} duplicate rows.")
            else:
                st.info("No duplicates found.")

        if col2.button("Drop Missing Records"):
            orig = st.session_state.df.shape[0]
            st.session_state.df.dropna(inplace=True)
            new = st.session_state.df.shape[0]
            st.success(f"✅ Dropped {orig - new} rows with missing values.")

        if col3.button("Show Null Values"):
            st.write("Null Values by Column:")
            st.dataframe(st.session_state.df.isnull().sum(), use_container_width=True)

    with st.expander("🔧 Data Transformation"):
        col1, col2 = st.columns(2)

        if col1.button("💲 Remove Dollar Sign in Price"):
            st.session_state.df['unit_price'] = st.session_state.df['unit_price'].str.replace('$', '', regex=False).astype(float)
            st.success("Dollar signs removed.")

        if col2.button("➕ Add Total Column"):
            if 'unit_price' in st.session_state.df.columns and 'quantity' in st.session_state.df.columns:
                st.session_state.df['total'] = st.session_state.df['unit_price'] * st.session_state.df['quantity']
                st.success("Total column added.")

    with st.expander("📥 Save & Export"):
        col1, col2 = st.columns(2)
        if col1.button("💾 Create Clean CSV"):
            st.session_state.df.to_csv("Walmart_clean_data.csv", index=False)
            st.success("Clean CSV saved.")

        if col2.button("🔡 Convert Column Names to Lowercase"):
            st.session_state.df.columns = st.session_state.df.columns.str.lower()
            st.success("Column names converted to lowercase.")

    with st.expander("🛢️ Database Operations"):
        if st.button("📡 Connect and Upload to Database"):
            try:
                st.session_state.df.to_sql('walmart', con=engine_mysql, if_exists='replace', index=False)
                st.success("Uploaded data to MySQL successfully.")
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("📈 Insights & Analysis")

    tabs = st.tabs(["📊 Grouped Summary", "🏆 Top Category by Branch", "🗓️ Top Day by Branch"])

    with tabs[0]:
        if st.button("Show Grouped Payment Data"):
            try:
                query = """
                SELECT 
                    payment_method, 
                    COUNT(*) AS no_payments, 
                    SUM(quantity) AS no_qnty_sold 
                FROM walmart 
                GROUP BY payment_method;
                """
                df_grouped = pd.read_sql_query(query, engine_mysql)
                st.dataframe(df_grouped, use_container_width=True)
            except Exception as e:
                st.error(f"Query error: {e}")

    with tabs[1]:
        if st.button("Show Top Rated Category per Branch"):
            try:
                query = """
                SELECT *
                FROM (
                    SELECT 
                        branch, 
                        category, 
                        AVG(rating) AS avg_rating,
                        RANK() OVER (PARTITION BY branch ORDER BY AVG(rating) DESC) AS rnk
                    FROM walmart
                    GROUP BY branch, category
                ) ranked
                WHERE rnk = 1;
                """
                df_top = pd.read_sql_query(query, engine_mysql)
                st.dataframe(df_top, use_container_width=True)
            except Exception as e:
                st.error(f"Query error: {e}")

    with tabs[2]:
        if st.button("Show Top Rated Day per Branch"):
            try:
                query = """
                SELECT *
                FROM (
                    SELECT
                        branch,
                        DAYNAME(date) AS day_name,
                        COUNT(*) AS total_sales,
                        RANK() OVER (PARTITION BY branch ORDER BY COUNT(*) DESC) AS rnk
                    FROM walmart
                    GROUP BY branch, day_name
                ) ranked
                WHERE rnk = 1;
                """
                df_day = pd.read_sql_query(query, engine_mysql)
                st.dataframe(df_day, use_container_width=True)
            except Exception as e:
                st.error(f"Query error: {e}")

def about():
    st.title("📘 About Go Mart")
    st.write("""
    At Go Mart, we're building a better world — helping people live healthier lives, promoting sustainability, and fostering community.
    """)
    st.subheader("💼 Founders")
    cols = st.columns(2)
    founders = [
        "Muhammad Rayyan Naveed",
        "Muhammad Saim Rao",
        "Muhammad Sajjid Jhedu",
        "Syed Zohaib Shah",
        "Shayan Meo Rajput"
    ]
    for i, name in enumerate(founders):
        cols[i % 2].markdown(f"✅ **{name}**")

def contact():
    st.title("📞 Contact Us")
    st.info("📧 Email: mygomart@gmail.com")
    st.info("📱 Phone: 111-555-898")

def get_api_data(api):
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(api, path='.', unzip=True)

def main():
    if option == "🏠 Home":
        home()
    elif option == "ℹ️ About":
        about()
    elif option == "📞 Contact":
        contact()
    elif option == "📤 Generate Data":
        st.title("📡 Download Data via Kaggle API")
        st.write("Enter the Kaggle API path to download and unzip a dataset.")
        api = st.text_input("🔗 Enter Kaggle API Path")
        if api:
            get_api_data(api)
            st.success("✅ Data downloaded and extracted.")
        else:
            st.warning("⚠️ Please enter a valid API path.")

if __name__ == "__main__":
    main()
