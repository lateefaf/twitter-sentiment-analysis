from kafka import KafkaProducer, producer
import tweepy
import config
# Configure the Kafka producer
bootstrap_servers = config.bootstrap_servers
kafkaproducer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# Set the API keys and access tokens as environment variables or directly pass them to the producer.
api_key = config.api_key
api_secret_key = config.api_secret_key
access_token = config.access_token
access_token_secret = config.access_token_secret

# Set up a connection to the Twitter API using your API keys and access tokens.
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

# Twitter API object
api = tweepy.API(auth)

# Use the Twitter API to fetch tweets based on specific search criteria
search_query = 'us politics'
tweets = api.search_tweets(q=search_query, count=10)  # Fetch 10 tweets

# Publish the fetched tweets to Kafka topics
topic = 'politics'
for tweet in tweets:
    tweet_data = tweet.text.encode('utf-8')
    kafkaproducer.send(topic, value=tweet_data)
    kafkaproducer.flush()
