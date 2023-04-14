import streamlit as st
import pickle

# !pip install streamlit-extras
from streamlit_extras.switch_page_button import switch_page


def main():
    st.title("Home Page")

st.title('Welcome to my Airbnb assistance page')
st.text("")
st.subheader("Your one stop shop for Airbnb listing analysis\n" \
             "What can I help you with?")

price = st.button("I have a listing, but need help pricing it")
if price:
    switch_page("Price Recommender")

reviews = st.button("I want to see analysis of my reviews")
if reviews:
    switch_page("Review Analysis")

sentiment = st.button("How does the tone of my descriptions compare to other listings?")
if sentiment:
    switch_page("Sentiment Analysis")

how = st.button("Wait... how does this all work")
if how:
    switch_page("How it works")


