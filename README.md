# Twitter Scraping using Streamlit and Mongodb

This project is about scraping twitter data using Streamlit. Streamlit scrapes the twitter data for the given hashtag/keyword for the given period with the helo of snscrape library.
The data from the scraped tweets are uploaded in MongoDB. It can be downloaded either as CSV or JSON file.

![Best-Twitter-Scrapers-min](https://github.com/Srivathsan221/Twitter-Scraping/assets/61115411/07654125-ebc9-4e0b-96ac-1050b3f38fe8)

## Technology Stack

Language: Python
Libraries: Snscrape,pandas,pymongo
Database: MongoDB
GUI Framework: Streamlit

### Scraping the tweet
   -To scrap the data Snscrape python library is used. The TweetSearchScraper() method scrape the Twitter data without Twitter API. The method is passed with a query conating the hashtag to be search and the search dates (From start date to end date)

### Uploading data in MongoDB
   -Tweets that are scraped using the Snscrape library is inserted into the MongoDB database by establishing the clinet connection. The tweet datas are strored under the twitter db collections.

### Creating the UI
   - UI is implemented with Streamlit. 

## Menu 1 --> Home
Home page displays the title of the Application.

## Menu 2 --> About
Description about the Twitter Scraping, Snscrape librray, MongoDB and Streamlit framework.

## Menu 3 --> Search
Search menu which is used to search the tweet data usng the #hashtag and for given dates. Everytime the search menu deletes the existing datas while searching the new tweet in order to retrive the tweet information correctly.

## Menu 4 --> Display
The scraped data from the MongoDB database are dispalyed as a DataFrame

## Menu 5 --> Download
The scraped data from the MongoDB database is downloaded as CSV/ JSON file formats as per the requirement. 
