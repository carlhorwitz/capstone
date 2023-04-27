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

# df = pd.read_csv('/Users/carl/GA/projects/airbnb/data/1500_sentiment_api.csv')
df = pd.read_csv('../data/1500_sentiment_api.csv') 


st.title("Sentiment Analysis")
st.subheader('The tone of a listing has an impact on whether people elect to stay in a location and how much they will pay')

st.write("Sentiment analysis is a computational process for determining whether a piece of writing has a positive, negative, or neutral tone. \n" \
       "The analysis returns numeric values on a 0-1 scale, with the number indicating the probability that a given input fits into that category.\n" \
       "Additionally, sentiment analysis combines individual scores to create a compound score, which provides a more 'holistic' assessment of sentiment.\n" \
       "A compound score of -1 suggests a strong probability of negativity, while a score of +1 suggests a strong probability of positivity.")

st.write("Input a block of text from your listing and we'll compare the tone of your post existing posts.")

description = st.selectbox("What description would you like to have analyzed?", ('Host Description', 'Property Description','Neighborhood Overview'))

st.write("")
words=st.text_area("Paste your description here:")

if st.button('Make prediction'):
    with st.spinner('Predicting...'):
        time.sleep(20)
        sia = SentimentIntensityAnalyzer()
        sentiments = sia.polarity_scores(words)
        compound= sentiments['compound']
        positive= sentiments['pos']
        negative = sentiments['neg']
        neutral = sentiments['neu']

        
        st.write(f"Your {description} description has a") 
        st.write(f"Positive sentiment score of {positive}") 
        st.write(f"Negative sentiment score of {negative}") 
        st.write(f"When looked at collectively, Your {description} has a compound sentiment score of {compound}")


        st.write(f'The graph below shows how your "{description}" compares with the average of all other listings.')

    if description =='Host Description':
        all_users = [df['host_sent_pos'].mean(), df['host_sent_neg'].mean(), df['host_sent_compound'].mean()] 
        one_user = [positive, negative, compound]
        labels = ['Positive', 'Negative', 'Compound']
        
        x = np.arange(len(labels))  
        width = 0.35  
        
        fig, ax = plt.subplots()
        all_users_plot = ax.bar(x - width/2, all_users, width, label='Airbnb Average')
        one_user_plot = ax.bar(x + width/2, one_user, width, label='Your results')
        
        
        ax.set_ylabel('Scores')
        ax.set_title('Comparison of average sentiment scores with your input')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        st.pyplot(fig)




    if description =='Neighborhood Overview':
        all_users = [df['neighborhood_sent_pos'].mean(), df['neighborhood_sent_neg'].mean(), df['neighborhood_sent_compound'].mean()] 
        one_user = [positive, negative, compound]
        labels = ['Positive', 'Negative', 'Compound']
        
        x = np.arange(len(labels))  
        width = 0.35  
        
        fig, ax = plt.subplots()
        all_users_plot = ax.bar(x - width/2, all_users, width, label='Airbnb Average')
        one_user_plot = ax.bar(x + width/2, one_user, width, label='Your results')
        
        ax.set_ylabel('Scores')
        ax.set_title('Comparison of average sentiment scores with your input')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        st.pyplot(fig)


    if description =='Property Description':                  
        all_users = [df['description_sent_pos'].mean(), df['description_sent_neg'].mean(), df['description_sent_compound'].mean()] 
        one_user = [positive, negative, compound]
        labels = ['Positive', 'Negative', 'Compound']
        
        x = np.arange(len(labels))  
        width = 0.35  
        
        fig, ax = plt.subplots()
        all_users_plot = ax.bar(x - width/2, all_users, width, label='Airbnb Average')
        one_user_plot = ax.bar(x + width/2, one_user, width, label='Your results')
        
        
        ax.set_ylabel('Scores')
        ax.set_title('Comparison of average sentiment scores with your input')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        st.pyplot(fig)
