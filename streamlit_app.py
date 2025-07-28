# Import Python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Connect to Snowflake
cnx = st.connection("snowflake", type="snowflake")
session = cnx.session()

# Set the correct database and schema (important if default context is wrong)
session.use_database("smoothies")
session.use_schema("public")
session.use_warehouse("compute_wh")

# UI: Title and instructions
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input: Name on the smoothie
name_on_order = st.text_input("Name on smoothie")
st.write("The name on your smoothie will be: ", name_on_order)

# Fetch fruit options from Snowflake
try:
    my_dataframe = session.table("fruit_options").select(col("FRUIT_NAME"))
    fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

    # UI: Multi-select fruit ingredients
    ingredient_list = st.multiselect("Choose up to five ingredients:", fruit_list, max_selections=5)

    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
    st.text(smoothiefroot_response)

    if ingredient_list:
        st.write("Selected ingredients:", ingredient_list)
        ingredients_string = ' '.join(ingredient_list)

        # Prepare SQL insert statement
        my_insert_stmt = f"""
            INSERT INTO orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """

        # Button to submit the order
        if st.button("Submit Order"):
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")

except Exception as e:
    st.error("An error occurred while accessing Snowflake data.")
    st.exception(e)
