import snscrape.modules.twitter as sntwitter
import streamlit as st
import pandas as pd
import pymongo
from pymongo import MongoClient
from datetime import date
import json

client = pymongo.MongoClient("mongodb://Srivathsa2910:sriv12345@ac-iqku39l-shard-00-00.ujpbo5o.mongodb.net:27017,ac-iqku39l-shard-00-01.ujpbo5o.mongodb.net:27017,ac-iqku39l-shard-00-02.ujpbo5o.mongodb.net:27017/?ssl=true&replicaSet=atlas-ue5wsp-shard-0&authSource=admin&retryWrites=true&w=majority")

twtdb = client.sri
twtdb_main = twtdb.twitterproj

def main():
  tweets = 0
  st.title("Twitter Scraping")
  # 5 menus
  menu = ["Home","About","Search","Display","Download"]
  choice = st.sidebar.selectbox("Menu",menu)

  # Menu 1 => Home Page
  if choice=="Home":
    st.write('''This app is a Twitter Scraping web app created using Streamlit. 
             It scrapes the twitter data for the given hashtag/ keyword for the given period.
             The tweets are uploaded in MongoDB and can be dowloaded as CSV or a JSON file.''')

  # Menu 2 => Menu Information
  elif choice=="About":
    #Twitter Scraper
    with st.expander("Twitter Scrapper"):
      st.write('''Twitter Scraper enables you to extract large amounts of data from Twitter.
                    It collects the data like date, id, url, tweet content, users/tweeters,reply count, 
                    retweet count, language, source, like count, followers, friends and lot more information 
                    to gather insights about the data.''')

    #Snscraper
    with st.expander("Snscraper"):
      st.write('''Snscrape is a scraper for Social Networking Service (SNS). 
                  It scrapes user profiles, hashtages returns the discovered items from the relavent posts/tweets.''')

    #Mongodb
    with st.expander("Mondodb"):
      st.write('''MongoDB is an opensource document database to store unstructured data. The data is stored as BSON.''')

    #Streamlit 
    with st.expander("Streamlit"):
      st.write('''Streamlit is an opensource framework used to build highly interactive web applications using python language. 
                  It is easy to share machine learning and datasciecne web apps using streamlit.''')

  # Menu 3 => Search
  elif choice=="Search":
    # After every last tweet the database will be cleared for updating freshly scraped data
    twtdb_main.delete_many({})

    # Form for collecting user input for twitter scrape
    with st.form(key='form1'):
      # Provide input hashtag
      st.subheader("Tweet searching Form")
      st.write("Enter the hashtag or keyword to perform the twitter scraping#")
      query = st.text_input('Hashtag or keyword')

      # Provide number of tweets to be scraped
      st.write("Enter the limit for the data scraping: Maximum limit is 1000 tweets")
      limit = st.number_input('Insert a number',min_value=0,max_value=1000,step=10)

      # Provide start date and end date
      st.write("Enter the Starting date to scrap the tweet data")
      start = st.date_input('Start date')
      end = st.date_input('End date')
      
      # Enter submit to start scraping process
      submit_button = st.form_submit_button(label="Tweet Scrap")
    
    if submit_button:
      st.success(f"Tweet hashtag {query} received for scraping".format(query))

      for tweet in sntwitter.TwitterSearchScraper(f'from:{query} since:{start} until:{end}').get_items():
        # To check whether the limit is reached
        if tweets == limit:
          break
        # Stores the tweet data into MongoDB until the limit  is reached
        else:      
          new = {"date":tweet.date,"user":tweet.user.username, "url":tweet.url, "followersCount":tweet.user.followersCount, "friendsCount":tweet.user.friendsCount, "favouritesCount":tweet.user.favouritesCount,"mediaCount":tweet.user.mediaCount}
          twtdb_main.insert_one(new)
          tweets += 1
      
      # To display the tweets scraped
      df = pd.DataFrame(list(twtdb_main.find()))
      cnt = len(df)
      st.success(f"Total number of tweets scraped : {cnt}".format(cnt))

  # Menu 4 => Display 
  elif choice=="Display":
    
    df = pd.DataFrame(list(twtdb_main.find())) # To save documents in DataFrame
    st.dataframe(df)  

  # Menu 5  => Download (CSV/JSON)
  else:
    col1, col2 = st.columns(2)

    # To Download in CSV Format
    with col1:
      st.write("Download the tweet data as CSV File")
      
      df = pd.DataFrame(list(twtdb_main.find())) # save the documents in a dataframe
      
      df.to_csv('twittercsv.csv')  # Convert dataframe to csv
      def convert_df(data):
        return df.to_csv().encode('utf-8') # Cache the conversion to prevent computation on every rerun
      csv = convert_df(df)
      st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name='twtittercsv.csv',
                        mime='text/csv',
                        )
      st.success("Successfully Downloaded data as CSV")

    # To Download in JSON Format
    with col2:
      st.write("Download the tweet data as JSON File")
       
      twtjs = df.to_json(default_handler=str).encode() # Convert dataframe to json string instead as json file

      # Create Python object from JSON string data
      obj = json.loads(twtjs)
      js = json.dumps(obj, indent=4)
      st.download_button(
                        label="Download data as JSON",
                        data=js,
                        file_name='twtjs.js',
                        mime='text/js',
                        )
      st.success("Successfully Downloaded data as JSON")

# Calling the Main function
main()