import streamlit as st
import pickle
import numpy as np
import pandas as pd
import time


import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from PIL import Image

df = pd.read_csv('../data/1500_review_sentiment.csv')

# !pip install streamlit-extras
from streamlit_extras.switch_page_button import switch_page


st.title('How much should I charge for my Airbnb listing?')
st.subheader("Answer the following questions and given current market trends, we'll recommend a price")


owner = st.text_input("What is your name?","")

#take in all the necessary information
st.write(f"Hi {owner}.") 
st.subheader("Information about the space:")
st.write("The first two questions are pull-down menus, or you can start typing to narrow down the options")
st.write("")


shared_status = st.selectbox("What type of accomodations is being offered?", ('entire home', 'private room', 'shared space', 'hotel Room'))
st.write("")


hoods= ['Virginia Village', 'Highland', 'Berkeley', 'West Highland',
       'Five Points', 'City Park West', 'North Park Hill',
       'Cory - Merrill', 'Union Station', 'City Park', 'Baker',
       'Athmar Park', 'Whittier', 'North Capitol Hill', 'Stapleton',
       'Capitol Hill', 'Congress Park', 'South Park Hill',
       'Washington Virginia Vale', 'Hampden South', 'Windsor', 'CBD',
       'Montclair', 'Lincoln Park', 'Jefferson Park',
       'Washington Park West', 'Gateway - Green Valley Ranch', 'Speer',
       'Clayton', 'Cole', 'Rosedale', 'Harvey Park South', 'Fort Logan',
       'Sunnyside', 'University', 'Regis', 'Skyland', 'University Park',
       'Platt Park', 'Lowry Field', 'Goldsmith', 'Cheesman Park', 'Hale',
       'Cherry Creek', 'Barnum West', 'Hilltop', 'Villa Park',
       'Washington Park', 'Bear Valley', 'West Colfax', 'Wellshire',
       'Sloan Lake', 'Country Club', 'Hampden', 'Barnum',
       'University Hills', 'East Colfax', 'Overland',
       'Northeast Park Hill', 'Indian Creek', 'Globeville', 'Ruby Hill',
       'Civic Center', 'Mar Lee', 'Chaffee Park', 'DIA', 'Montbello',
       'College View - South Platte', 'Belcaro', 'Westwood',
       'Harvey Park', 'Valverde', 'Sun Valley', 'Elyria Swansea',
       'Kennedy', 'Auraria', 'Southmoor Park', 'Marston']
sorted_hoods=sorted(hoods)

neighborhood = st.selectbox("The listing is available which neighborhood?", sorted_hoods)
st.write("")
st.write("Use the slider to answer the following questions about your listing")
st.write("")

col1, col2 = st.columns(2)
with col1:
    accommodates = st.slider("How many people can your listing accomodate?", min_value=1, max_value=16)
with col2:
    beds_adjusted = st.slider("How many beds are available?", min_value=1, max_value=10)

col1, col2 = st.columns(2)
with col1:
    bedrooms = st.slider("In how many bedrooms?", min_value=1, max_value=6)
with col2:
    bathrooms = st.slider("How many bathrooms are available?", min_value=1, max_value=6)


stay_range = st.slider("What is the minimum and maximum length of a stay?", value=[1,90])

minimum_nights=stay_range[0]
maximum_nights=stay_range[1]

st.subheader("Information about the listing:")

#create a map so that the inputs here match the format of the df

yes_no_dict = {'Yes': 1, 'No': 0}

host_identity_verified = st.radio(
    "Have you verified your hosting status with AirBnb?",
    ('No', 'Yes'))
host_identity_verified = yes_no_dict[host_identity_verified]

host_has_profile_pic = st.radio(
    "Do you have a profile picture in your listing?",
    ('No', 'Yes'))
host_has_profile_pic = yes_no_dict[host_has_profile_pic]

host_lives_in_neighborhood = st.radio(
    "Do you live in the same neighborhood as your listing?",
    ('No', 'Yes'))
host_lives_in_neighborhood = yes_no_dict[host_lives_in_neighborhood]

license_listed = st.radio(
    "Is your license number included in your listing?",
    ('No', 'Yes'))
license_listed = yes_no_dict[license_listed]

instant_bookable = st.radio(
    "Is your listing available for instant booking?",
    ('No', 'Yes'))
instant_bookable = yes_no_dict[instant_bookable]

st.subheader("Walk Score")
st.markdown("Please visit the site [WalkScore](https://www.walkscore.com/CO/Denver) and enter your address "+ 
            "to get the Walk, Bike and Transit Scores for your listing. " + 
            "These scores tell us the proximity to nearby amenities.")
st.write("")

walk_scores = st.slider("What is your Walk Score?", min_value=1, max_value=100)

col1, col2 = st.columns(2)
with col1:
    transit_scores = st.slider("What is your Transit Score?", min_value=1, max_value=100)
with col2:
    bike_scores = st.slider("What is your Bike Score?", min_value=1, max_value=100)



st.subheader("Sentiment Analysis")
st.write('We have found that tone of a listing has an impact on whether people elect to stay in a location and how much they will pay')
st.write("Cut and paste the following descriptions from your listing below. If you haven't completed that section, that's fine, just leave it blank")

st.write("")
host=st.text_area("About the host:")
description=st.text_area("Property Description:")
hood=st.text_area("Neighborhood Description:")

if len(host)== 0:
    has_host_about=0
    host='neutral'
else: 
    has_host_about=1
    
if len(description)==0:
    description='neutral'

if len(hood)==0:
    hood='neutral'
    has_neighborhood_overview=0
else:
    has_neighborhood_overview=1

sia = SentimentIntensityAnalyzer()

host_sentiments = sia.polarity_scores(host)
host_sent_compound= host_sentiments['compound']

description_sentiments = sia.polarity_scores(description)
description_sent_compound= description_sentiments['compound']

hood_sentiments = sia.polarity_scores(hood)
neighborhood_sent_compound= hood_sentiments['compound']

st.subheader("If you have a new listing, you can skip to the bottom.")
st.write('If you have listed your place and have already had guests, please continue below')

col1, col2 = st.columns(2)
with col1:
    years_hosting = st.slider("How many years have you had your listing?", min_value=0, max_value=20)
with col2:
    superhost = st.radio("Are you a 'Superhost'?",
    ('No', 'Yes'))
host_is_superhost = yes_no_dict[superhost]
       
col1, col2 = st.columns(2)
with col1:
    reviews = st.radio("Do you already have reviews'?",
    ('No', 'Yes'))
    has_reviews = yes_no_dict[reviews]  
with col2:
    number_of_reviews = st.slider("How many reviews do you have?", min_value=0, max_value=50)

#set up the information to be entered into the model
columns=[
    'shared_status', 
    'accommodates',
    'bathrooms', 
    'bedrooms',
    'beds_adjusted',
    'neighborhood', 
    'has_neighborhood_overview', 
    'has_reviews',
    'instant_bookable',
    'host_lives_in_neighborhood',
     'host_is_superhost', 
    'host_has_profile_pic',
    'host_identity_verified', 
    'has_host_about', 
    'years_hosting',
    'license_listed', 
    'minimum_nights',
    'maximum_nights',
     'number_of_reviews',
     'bike_scores',
    'walk_scores',
    'transit_scores',
    'host_sent_compound', 
    'description_sent_compound', 
    'neighborhood_sent_compound']

user_input = np.array([ shared_status, 
    accommodates,
    bathrooms, 
    bedrooms,
    beds_adjusted,
    neighborhood, 
    has_neighborhood_overview, 
    has_reviews,
    instant_bookable,
    host_lives_in_neighborhood,
    host_is_superhost, 
    host_has_profile_pic,
    host_identity_verified, 
    has_host_about, 
    years_hosting,
    license_listed, 
    minimum_nights,
    maximum_nights,
    number_of_reviews,
    bike_scores,
    walk_scores,
    transit_scores,
    host_sent_compound, 
    description_sent_compound, 
    neighborhood_sent_compound])

X = pd.DataFrame(data=user_input.reshape(1, -1), columns=columns)


# Read in model:
with open('../pickle/bagged_GB.pkl', 'rb') as f:
    df_model = pickle.load(f)

st.write("")
if st.button('Make prediction'):
    with st.spinner('Predicting...'):
        time.sleep(20)
        prediction = df_model.predict(X)
        rounded = np.round(prediction)
        st.write(f"Given the info provided, we recommend you list your rental at")
        st.subheader(f"${np.round(prediction)[0]:.0f} per night.") 
    
    st.write("")
    st.write("")

    st.subheader(f"Some information about rentals in {neighborhood}.")

    rentals = df[df['neighborhood']==neighborhood].count()[0]
    ave_price = int(df[df['neighborhood']==neighborhood]['price'].mean())

    st.write(f"There are currently {rentals} rentals listed on AirBnb in {neighborhood}")

    ave_guests=round(df[df['neighborhood']== neighborhood]['accommodates'].mean())
    ave_beds=round(df[df['neighborhood']== neighborhood]['beds_adjusted'].mean(),1)
    ave_price = int(df[df['neighborhood']==neighborhood]['price'].mean())
    common_status = df[df['neighborhood']==neighborhood]['shared_status'].value_counts().idxmax()

    st.write(f"The 'average' rental in {neighborhood} is a {common_status} that accomodates {ave_guests} for ${ave_price}")

    st.write("")
    st.write("We have found the feature importance of price can be determined by the following categories") 
    image = Image.open('../images/bagged_GD_final.png')
    st.image(image, caption='Top factors in Airbnb price')

    st.write("A lot of features of your rental/listing are beyond your control (size, location...) one thing you CAN influence\n" \
             "is the tone of your descriptions, be sure to visit the Sentiment Analysis page to assess how you compare with other listings.")

    if license_listed==0:
        st.write("In this particular model, it's of lesser importance, however in other models having your license listed\n" \
                 "a larger factor in price. It appears you didn't check that box, if you have a license, be sure to include that in your listing.")

