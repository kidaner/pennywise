import streamlit as st
import time
from gro_image import extract_grocery_list
from price_loc import create_grocery_price_matrix
from gro_zip import grocery_city
from struc_items import structured_items
from struc_grocery import structured_grocery
from test_lang import agent_grocery

st.sidebar.title("PENNYWISE")
st.sidebar.title("Save Money on Groceries 🛒")
st.sidebar.subheader("Compare prices across multiple stores and maximize your purchasing power.")

st.sidebar.write("---")
st.sidebar.subheader("Problem:")
st.sidebar.write("Inflation and commodity prices are putting significant financial pressure on households.")
st.sidebar.subheader("Solution:")
st.sidebar.write("Our AI agent streamlines the price comparison process, empowering users to make informed shopping decisions and alleviating financial burdens.")

st.write("Enter your city and upload a photo of your grocery list to find the best prices.")
st.write("Please note that processing times may vary, especially for long grocery lists, due to rate limits.")
st.sidebar.write("---")

city = st.text_input("City")
uploaded_file = st.file_uploader("Upload Grocery List Image", type=["jpg", "jpeg", "png"])

if city and uploaded_file:
    st.write(f"City: {city}")
    st.image(uploaded_file, caption="Uploaded Grocery List", width=300)
    
    with st.spinner("Fetching items..."):
        time.sleep(5)
        grocery_list = extract_grocery_list(uploaded_file)

    if grocery_list:
        items = structured_items(grocery_list)
        with st.spinner("Fetching grocers..."):
            time.sleep(5)
            stores = structured_grocery(grocery_city(city))
        
        with st.spinner("Fetching prices..."):
            time.sleep(5)
        
        with st.spinner("Compiling matrix..."):
            time.sleep(1)
            price_matrix = create_grocery_price_matrix(items, stores, city)

        st.write("Grocery Price Comparison Matrix:")
        st.dataframe(price_matrix)
else:
    st.warning("Please upload an image and input your city.")
