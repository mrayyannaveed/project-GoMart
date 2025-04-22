import kaggle
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Go Mart",
    page_icon="🧊",
    layout="wide"
)


option = st.sidebar.radio("Select a page", ["Home", "About", "Contact", "Generate Data"])
def home():
    st.title("🏪Go Mart Online Store")
    st.write("Welcome to Go Mart, your one-stop shop for all your grocery needs. We offer a wide range of products, from fresh produce to pantry essentials, all at competitive prices.")
    st.markdown("### 🛒Our Products")
    df = pd.read_csv("Walmart.csv")
    if st.checkbox(" Show Products"):
        mydf = df.head(8)
        st.dataframe(mydf, hide_index=True)
    if st.checkbox("Show Rows and Columns"):
        st.write("Number of Rows:", df.shape[0])
        st.write("Number of Columns:", df.shape[1])
    if st.checkbox("Show Stats"):
        st.write(df.describe())
    if st.checkbox("Show Duplicates"):
        st.write("Number of Duplicates:",df.duplicated().sum())
def about():
    st.title("About US")
    st.write("We aim to build a better world — helping people live better and renew the planet while building thriving, resilient communities. For us, this means working to create opportunity, build a more sustainable future, advance belonging and bring communities closer together.")
    st.header("Go Mart Owner's 💰")
    st.write("### Muhammad Rayyan Naveed") 
    st.write("### Muhammad Saim Rao") 
    st.write("### Muhammad Sajjid Jhedu") 
    st.write("### Syed Zohaib Shah")
    st.write("### Shayan Meo Rajput")

def contact():
    st.title("Contact Go Mart")
    st.write("#### 📧mygomart@gmail.com")
    st.write("#### 📞111-555-898")

def get_api_data(api):
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(api, path='.', unzip=True)
    
def main():

    if option == "Home":
        home()
    elif option == "About":
        about()
    elif option == "Contact":
        contact()
    elif option == "Generate Data":
        st.title("Generate Data Through API")
        st.write("#### Enter the API to convert it into csv data format.")
        api = st.text_input("Enter API")
        if api:
            get_api_data(api)
        else:
            st.success("Please enter an API")
    

if __name__ == "__main__":
    main()