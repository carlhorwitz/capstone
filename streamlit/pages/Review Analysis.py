import streamlit as st
import pandas as pd
import pickle
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import time
import matplotlib.pyplot as plt
import altair as alt
import numpy as np
from PIL import Image

# !pip install streamlit-extras
from streamlit_extras.switch_page_button import switch_page

df = pd.read_csv('../data/1500_review_sentiment.csv')

st.title("Review Analysis")
st.subheader("Let's explore the reviews you have received on your property and how they compare to the average review.")
st.write("Enter your listing ID below. If you don't know it, go to your listing page and copy the number at the end of the url")
            
user_input = st.number_input("Enter a number", value=177)

user_input = int(user_input)

if user_input not in df['id'].unique():
    st.write("Sorry, according to our records, there are no reviews of this listing yet")

else:
    num_reviews = df.loc[df['id'] == user_input, 'number_of_reviews'].iloc[0]

    if st.button("How are my reviews?"):
        with st.spinner('Predicting...'):
            time.sleep(20)

            rating = df.loc[df['id'] == user_input, 'review_scores_rating'].iloc[0]
            cleanliness = df.loc[df['id'] == user_input, 'review_scores_cleanliness'].iloc[0]
            communication = df.loc[df['id'] == user_input, 'review_scores_communication'].iloc[0]
            location = df.loc[df['id'] == user_input, 'review_scores_location'].iloc[0]
            

            ave_rating = round(df['review_scores_rating'].mean(),2)
            ave_cleanliness = round(df['review_scores_cleanliness'].mean(),2)
            ave_communication = round(df['review_scores_communication'].mean(),2)
            ave_location = round(df['review_scores_location'].mean(),2)
            

            st.write(f"You have received {num_reviews} reviews so far") 
            st.write(f"On average guests have rated their stay a {rating}, compared to an Airbnb average of {ave_rating}") 
            st.write(f"On average guests have rated the cleanliness of your place a {cleanliness}, compared to an Airbnb average of {ave_cleanliness}") 
            st.write(f"On average guests have rated your communication a {communication}, compared to an Airbnb average of {ave_communication}")
            st.write(f"On average guests have rated your communication a {location}, compared to an Airbnb average of {ave_location}")

            all_users = [ave_rating, ave_cleanliness, ave_communication, ave_location] 
            one_user = [rating, cleanliness, communication, location]                            
            labels = ['Overall Rating', 'Cleanliness', 'Communication' , 'Location']
            
            x = np.arange(len(labels))  
            width = 0.35  
            
            fig, ax = plt.subplots()
            all_users_plot = ax.bar(x - width/2, all_users, width, label='Airbnb Average')
            one_user_plot = ax.bar(x + width/2, one_user, width, label='Your results', color='red')
            
            
            ax.set_ylabel('Scores')
            ax.set_title('Comparison of your reviews')
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
            ax.legend(loc='lower right')


            # Display the chart using Streamlit
            st.pyplot(fig)

            #sentiment analysis of reviews 

            psentiment= round(df.loc[df['id'] == user_input, 'review_sent_pos'].iloc[0],2)
            nsentiment= round(df.loc[df['id'] == user_input, 'review_sent_neg'].iloc[0],2)
            csentiment= round(df.loc[df['id'] == user_input, 'review_sent_compound'].iloc[0],2)

            ave_psentiment= round(df['review_sent_pos'].mean(),2)
            ave_nsentiment= round(df['review_sent_neg'].mean(),2)
            ave_csentiment= round(df['review_sent_compound'].mean(),2)

            st.write("Sentiment analysis is one way to interpret the tone of the written word.\n" \
                    "An analysis calculates a positive, negative, neutral and compound sentiment scores\n" \
                    "Positive and negative scores are on a 0-1 scale. Where 1 is strongly correlated to that sentiment and 0 is not correlated at all.\n" \
                    "The compound score is a combination of the three other scores and reflects a wholistic score:\n" \
                    "-1 being collectively negative and +1 being collectively positive")

            st.write(f"On average your reviews had a positive sentiment score of {psentiment}, compared to an Airbnb average of {ave_psentiment}")
            st.write(f"On average your reviews had a negative sentiment score of {nsentiment}, compared to an Airbnb average of {ave_nsentiment}")
            st.write(f"On average your reviews had a compound sentiment score of {csentiment}, compared to an Airbnb average of {ave_csentiment}")


            all_users = [ave_psentiment, ave_nsentiment, ave_csentiment] 
            one_user = [psentiment, nsentiment, csentiment]                            
            labels = ['Positive Sentiment', 'Negative Sentiment', 'Compound Sentiment']
            
            x = np.arange(len(labels))  
            width = 0.35  
            
            fig, ax = plt.subplots()
            all_users_plot = ax.bar(x - width/2, all_users, width, label='Airbnb Average')
            one_user_plot = ax.bar(x + width/2, one_user, width, label='Your results', color='red')
            
            
            ax.set_ylabel('Scores')
            ax.set_title('Comparison of your review sentiment')
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
            ax.legend(loc='lower right')

            # Display the chart using Streamlit
            st.pyplot(fig)
