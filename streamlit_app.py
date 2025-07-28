# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom Smoothie!
  """
)

# option = st.selectbox(
#     "What is your favourite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("You selected:", option)

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#st.dataframe(data=my_dataframe, use_container_width=True)
name_on_order = st.text_input("Name on smoothie")
st.write("The name on your smoothie will be: ", name_on_order)
# Convert Snowpark DataFrame to Python list
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

# Multiselect from the list
ingredient_list = st.multiselect("Choose up to five ingredients:", fruit_list, max_selections=5)

#ingredient_list = st.multiselect("Choose up to five ingredients:", my_dataframe, max_selections=5)
if ingredient_list:
    st.write(ingredient_list)
    st.text(ingredient_list)
    ingredients_string = ''
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+name_on_order+ """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


