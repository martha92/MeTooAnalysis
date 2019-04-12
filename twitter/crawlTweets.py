import tweepy
import csv


def crawlTweets(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # MeToo
    # Open/Create a file to append data
    x=0
    csvFile = open('metoo_2019.csv', 'w')
    # # Use csv Writer
    csvWriter = csv.writer(csvFile)

    csvWriter.writerow(['created_date', 'is_retweet?', 'text', 'text_retweet', 'language', 'hashtags', 'mentions', 'location', 'geo_location','geo_country','geo_coordinates', 'user_created_at', 'screen_name','name','profile_description', 'total_number_of_tweets', 'is_verified', 'followers_count', 'friends_count', 'retweets_count', 'favorite_count','url','listed_count','default_profile','default_profile_image','has_extended_profile'])

    for tweet in tweepy.Cursor(api.search,q="{}+OR+{}".format("#MeToo", "#MeTooMovement"),
                               lang="{}+OR+{}+OR+{}".format("en", "fr", "es"), count=200,
                               since="2017-01-01", include_entities=True, tweet_mode='extended').items():  # ,
            hashtags = []
            try:
                for k, v in tweet.entities.items():
                    if k == 'hashtags':
                        hashtags.append([li['text'] for li in v])
                    else:
                        pass
                    if len(hashtags) == 0:
                        hashtags = "No Hashtags Associated with Tweet"
            except AttributeError as f:
                print(f)
                hashtags = "No Hashtags Associated with Tweet"

            mentions = []
            try:

                for k, v in tweet.entities.items():
                    if k == 'user_mentions':
                        mentions.append([li['screen_name'] for li in v])
                    else:
                        pass
                    #if len(mentions) == 0:
                        #mentions.append("No Mentions Associated with Tweet")
            except AttributeError as f:
                print(f)

            hashtags = str(hashtags).strip('[[]]')
            mentions = str(mentions).strip('[[]]')
            full_text_rt = ''
            retweeted = False
            try:
                full_text_retweeted = tweet.retweeted_status
                full_text_rt = full_text_retweeted.full_text
                retweeted = True
            except AttributeError as f:
                print(f)
                # print("It is not a retweet")

            geo_full_name = ''
            geo_country = ''
            geo_coordinates = ''
            try:
                geo_full_name = tweet.place.full_name
                geo_country = tweet.place.geo_country
                geo_coordinates = tweet.coordinates
            except AttributeError as f:
                print(f)
                # print("It doesnt have place")

            if retweeted:
                csvWriter.writerow(
                    [tweet.created_at, retweeted, '', tweet.full_text, tweet.lang, hashtags, mentions, tweet.user.location, geo_full_name, geo_country, geo_coordinates, tweet.user.created_at, tweet.user.screen_name,tweet.user.name ,tweet.user.description, tweet.user.statuses_count, tweet.user.verified, tweet.user.followers_count, tweet.user.friends_count, tweet.retweet_count, tweet.favorite_count, tweet.user.url, tweet.user.listed_count, tweet.user.default_profile, tweet.user.default_profile_image, tweet.user.has_extended_profile])
            else:
                csvWriter.writerow(
                    [tweet.created_at, retweeted, tweet.full_text, '', tweet.lang, hashtags, mentions, tweet.user.location, geo_full_name, geo_country, geo_coordinates, tweet.user.created_at, tweet.user.screen_name,tweet.user.name, tweet.user.description, tweet.user.statuses_count, tweet.user.verified, tweet.user.followers_count, tweet.user.friends_count, tweet.retweet_count, tweet.favorite_count, tweet.user.url, tweet.user.listed_count, tweet.user.default_profile, tweet.user.default_profile_image, tweet.user.has_extended_profile])
            
        


def getTweets2018(consumer_key, consumer_secret, access_token, access_token_secret, filename):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    data = {}
    with open(filename, 'rU') as infile:
        # read the file as a dictionary for each row ({header : value})
        reader = csv.DictReader(infile)
        for row in reader:
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]

    # extract the variables you want
    csvFile = open('metoo_2018_2017.csv', 'a')
    # # Use csv Writer
    csvWriter = csv.writer(csvFile)

    id_tweet = data['tweetid']
    print(len(id_tweet))
    for id_ in id_tweet:
        try:
            tweet = api.get_status(id_, tweet_mode='extended')
            # print(tweet)
            hashtags = []
            try:
                for k, v in tweet.entities.items():
                    if k == 'hashtags':
                        hashtags.append([li['text'] for li in v])
                    else:
                        pass
                    if len(hashtags) == 0:
                        hashtags = "No Hashtags Associated with Tweet"
            except AttributeError as f:
                print(f)
                hashtags = "No Hashtags Associated with Tweet"

            mentions = []
            try:

                for k, v in tweet.entities.items():
                    if k == 'user_mentions':
                        mentions.append([li['screen_name'] for li in v])
                    else:
                        pass
                    #if len(mentions) == 0:
                    #    mentions.append("No Mentions Associated with Tweet")
            except AttributeError as f:
                print(f)
                #mentions.append("No Mentions Associated with Tweet")

            hashtags = str(hashtags).strip('[[]]')
            mentions = str(mentions).strip('[[]]')
            full_text_rt = ''
            retweeted = False
            try:
                full_text_retweeted = tweet.retweeted_status
                full_text_rt = full_text_retweeted.full_text
                retweeted = True
            except AttributeError as f:
                print(f)
                # print("It is not a retweet")

            geo_full_name = ''
            geo_country = ''
            geo_coordinates = ''
            try:
                geo_full_name = tweet.place.full_name
                geo_country = tweet.place.geo_country
                geo_coordinates = tweet.coordinates
            except AttributeError as f:
                print(f)
                # print("It doesnt have place")

            if retweeted:
                csvWriter.writerow(
                    [tweet.created_at, retweeted, '', tweet.full_text, tweet.lang, hashtags, mentions, tweet.user.location, geo_full_name, geo_country, geo_coordinates, tweet.user.created_at, tweet.user.screen_name, tweet.user.name, tweet.user.description, tweet.user.statuses_count, tweet.user.verified, tweet.user.followers_count, tweet.user.friends_count, tweet.retweet_count, tweet.favorite_count])
            else:
                csvWriter.writerow(
                    [tweet.created_at, retweeted, tweet.full_text, '', tweet.lang, hashtags, mentions, tweet.user.location, geo_full_name, geo_country, geo_coordinates, tweet.user.created_at, tweet.user.screen_name,tweet.user.name, tweet.user.description, tweet.user.statuses_count, tweet.user.verified, tweet.user.followers_count, tweet.user.friends_count, tweet.retweet_count, tweet.favorite_count])
        except:
            print("ERROR, no ID found")

    # print(len(tweets))
    # search = 0

    # for tweet in tweepy.Cursor(
    #         api.user_timeline, screen_name="@mchris4duke", tweet_mode="extended").items():
    #     hashtags = []
    #     search += 1
    #     try:
    #         for k, v in tweet.entities.items():
    #             if k == 'hashtags':
    #                 ref = [li['text'] for li in v]
    #                 new_list = [x.lower() for x in ref]
    #                 if ('metoo' in new_list or 'metoomovement' in new_list):
    #                     print("metoo found")
    #             else:
    #                 pass
    #             if len(hashtags) == 0:
    #                 hashtags = "No Hashtags Associated with Tweet"
    #     except AttributeError as f:
    #         print(f)
    #         hashtags = "No Hashtags Associated with Tweet"
    # print(search)


def getTweets2017(consumer_key, consumer_secret, access_token, access_token_secret, filename):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    data = {}
    with open(filename, 'rU') as infile:
        # read the file as a dictionary for each row ({header : value})
        reader = csv.DictReader(infile)
        for row in reader:
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]

    # extract the variables you want
    csvFile = open('metoo_2017.csv', 'a')
    # # Use csv Writer
    csvWriter = csv.writer(csvFile)

    id_tweet = data['id']
    print(len(id_tweet))
    for id_ in id_tweet:
        try:
            tweet = api.get_status(id_, tweet_mode='extended')
            # print(tweet)
            hashtags = []
            try:
                for k, v in tweet.entities.items():
                    if k == 'hashtags':
                        hashtags.append([li['text'] for li in v])
                    else:
                        pass
                    #if len(hashtags) == 0:
                    #    hashtags = "No Hashtags Associated with Tweet"
            except AttributeError as f:
                print(f)
                #hashtags = "No Hashtags Associated with Tweet"

            mentions = []
            try:

                for k, v in tweet.entities.items():
                    if k == 'user_mentions':
                        mentions.append([li['screen_name'] for li in v])
                    else:
                        pass
                    if len(mentions) == 0:
                        mentions.append("No Mentions Associated with Tweet")
            except AttributeError as f:
                print(f)
                mentions.append("No Mentions Associated with Tweet")

            hashtags = str(hashtags).strip('[[]]')
            mentions = str(mentions).strip('[[]]')
            full_text_rt = ''
            retweeted = False
            try:
                full_text_retweeted = tweet.retweeted_status
                full_text_rt = full_text_retweeted.full_text
                retweeted = True
            except AttributeError as f:
                print(f)
                # print("It is not a retweet")

            geo_full_name = ''
            geo_country = ''
            geo_coordinates = ''
            try:
                geo_full_name = tweet.place.full_name
                geo_country = tweet.place.geo_country
                geo_coordinates = tweet.coordinates
            except AttributeError as f:
                print(f)
                # print("It doesnt have place")

            if retweeted:
                csvWriter.writerow(
                    [tweet.created_at, retweeted, '', tweet.full_text, tweet.lang, hashtags, mentions, tweet.user.location, geo_full_name, geo_country, geo_coordinates, tweet.user.created_at, tweet.user.screen_name, tweet.user.description, tweet.user.statuses_count, tweet.user.verified, tweet.user.followers_count, tweet.user.friends_count, tweet.retweet_count, tweet.favorite_count])
            else:
                csvWriter.writerow(
                    [tweet.created_at, retweeted, tweet.full_text, '', tweet.lang, hashtags, mentions, tweet.user.location, geo_full_name, geo_country, geo_coordinates, tweet.user.created_at, tweet.user.screen_name, tweet.user.description, tweet.user.statuses_count, tweet.user.verified, tweet.user.followers_count, tweet.user.friends_count, tweet.retweet_count, tweet.favorite_count])
        except:
            print("ERROR, no ID found")


if __name__ == '__main__':
    # input your credentials here
    consumer_key = 'Nv4v8rMM0EgEN8A4BhyvVlFZO'
    consumer_secret = 'LSKJYisimrn6miy0Om8ndUvgN5jzqkkmFll0k63ZkClyv2sl4L'
    access_token = '272599379-ZqaPKdzYJ7bAqdR0ubw975gBT1bbWXJz4JISo6Tu'
    access_token_secret = 'UG5HsGKxeq8Dhq5zPUJEZZSBEOOMQaOoziKMxKBodNl84'

    crawlTweets(consumer_key, consumer_secret,
                access_token, access_token_secret)
    getTweets2018(consumer_key, consumer_secret,
                 access_token, access_token_secret, 'sources/metootweets_2018.csv')
    # getTweets2017(consumer_key, consumer_secret,
    #              access_token, access_token_secret, 'sources/metoo_tweets_dec2017.csv')
