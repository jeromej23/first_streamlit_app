import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title("My Mom's New Healthy Diner")
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega3 and Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔 Hard-Boilded Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Lets put a picklist here so they can pick the fruits they want in the smoothie
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
streamlit.dataframe(fruits_to_show)

# Display Fruityvice
streamlit.header('Fruityvice Fruit Advice!')

def get_fruityvice_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Provide the fruit for which you like more information')
  else:
    fruity_vice_data = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruity_vice_data)
except URLError as e:
  streamlit.error()

streamlit.header("The fruit load list contains:")

def get_fruit_load_list():
  with my_cnx as cursor:
    my_cur = my_cnx.cursor()
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

# Add a button to load fruit list
if streamlit.button("Get Fruit Load List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

# streamlit.stop()

# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)


def insert_row_snowflake(new_fruit):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  with my_cnx as cursor:
    my_cur = my_cnx.cursor()
    my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')");
    return "Thanks for addding " + new_fruit

my_added_fruit = streamlit.text_input('What fruit would you like to add?','')
if streamlit.button("Add fruit to list"):
  insert_row_snowflake(my_added_fruit)
  fruit_added = insert_row_snowflake(my_added_fruit)
  streamlit.write(fruit_added)


