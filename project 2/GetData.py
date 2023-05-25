import tweepy
from textblob import TextBlob
import pandas as pd
import time
import pandas as pd
from sqlalchemy import create_engine
access_token= ''
access_token_secret = ''
consumer_key= ''
consumer_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
df = pd.DataFrame()

def save_df(df):
    import mysql.connector
    df = df.iloc[:2000,:]
    df.column = ['TText', 'label', 'Date']
    df['TText'] = df['TText'].apply(lambda x: x[:500])
    host = 'localhost'
    port = 3306
    database = 'twitter_sent'
    username = 'root'
    password = 'root'
    table_name = 'Suicis'

    # Establish MySQL connection
    cnx = mysql.connector.connect(host=host, port=port, database=database, user=username, password=password)

    # Create a cursor
    cursor = cnx.cursor()

    # Create table if it doesn't exist
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (TText VARCHAR(2550), label VARCHAR(255), Date DATE)"
    cursor.execute(create_table_query)

    # Convert the 'Date' column to a suitable format
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

    # Insert DataFrame records into the table
    insert_query = f"INSERT INTO {table_name} (TText, label, Date) VALUES (%s, %s, %s)"
    values = df.loc[:,['TText', 'label', 'Date']].values.tolist()
    cursor.executemany(insert_query, values)

    # Commit the changes
    cnx.commit()

    # Close the cursor and MySQL connection
    cursor.close()
    cnx.close()

def get_sentiment_analysis(query_list, since_date, until_date):
    for query in query_list:
        tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", since_id=since_date, until=until_date, tweet_mode="extended").items(200)
        j = 0
        for tweet in tweets:
            j = j +1
            analysis = TextBlob(tweet.full_text)
            sentiment = analysis.sentiment.polarity
            global df
            df = df.append({
                "Tweet":tweet.full_text,
                "Sentiment": sentiment
            }, ignore_index =  True)
        print(query, since_date, until_date, j)
def main():
    query_list = ["suicide",  "mental health",  "depressed","struggle","life"]
    
    # Define seasonal ranges based on your preference
    seasons = [
        ("Spring", "2022-05-10", "2022-08-31"),
        ("Summer", "2022-09-01", "2022-11-30"),
        ("Autumn", "2022-12-01", "2023-02-28"),
        ("Winter", "2023-03-01", "2023-05-10")
    ]
    
    for season in seasons:
        season_name, season_start, season_end = season
        print(f"--- {season_name} Season ---")
        try:
            get_sentiment_analysis(query_list, season_start, season_end)
        except tweepy.RateLimitError:
            print("Rate limit exceeded. Waiting for 15 minutes...")
            time.sleep(15 * 60)  # Wait for 15 minutes to continue
            get_sentiment_analysis(query_list, season_start, season_end)
        global df
        # df.to_csv('SuicideRawData.csv', index = False)
        
        save_df(df)

if __name__ == "__main__":
    main()
