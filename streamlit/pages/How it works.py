import streamlit as st
import numpy as np
import pandas as pd

from PIL import Image

# !pip install streamlit-extras
from streamlit_extras.switch_page_button import switch_page


st.title('How does this all work?')
st.subheader("A look behind the curtain")

url = "http://insideairbnb.com/"
word = "Inside Airbnb"


st.write(f"[{word}]({url}) offers free access to Airbnb data from pretty much every major market in the world")
st.write("From here I was able to download 2 main datasets.  One considing of over 5000 rentals with over 60 columns. Another of order a quarter million reviews.")


st.write("We have found the feature importance of price can be determined by the following categories ")
image = Image.open('../images/bagged_GD_final.png')
st.image(image, caption='Top 10 features that determine price')

