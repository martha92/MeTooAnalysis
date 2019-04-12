import pandas as pd
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
from autocorrect import spell
import re

# filename='twitter/metoo_all_items.csv'
# output = 'twitter/data_preprocess'

# def process(chunk,i_):
#     file = open('test'+str(i_),'wb')
#     file.write(str(chunk).encode('utf-8'))
#     file.close()


# i=0
# chunksize = 10 ** 6
# for chunk in pd.read_csv(filename, chunksize=chunksize):
#     process(chunk,i)
#     i+=1
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')


def getStopWords(language):
    if (language in ['english', 'french', 'dutch', 'german', 'swedish', 'spanish', 'italian']):
        stop_words = set(nltk.corpus.stopwords.words(language))
        return stop_words
    return None


def chunck_generator(filename, header=False, chunk_size=10 ** 3):
    for chunk in pd.read_csv(filename, delimiter=',', iterator=True, chunksize=chunk_size, parse_dates=[1, 12]):
        yield (chunk)


def chunck_generator_json(filename, header=False, chunk_size=10 ** 3):
    for chunk in pd.read_json(filename, lines=True, chunksize=chunk_size):
        yield (chunk)


def generator_json(filename, header=False, chunk_size=10 ** 3):
    chunk = chunck_generator_json(filename, header=False, chunk_size=10 ** 3)
    for row in chunk:
        yield row


def generator(filename, header=False, chunk_size=10 ** 3):
    chunk = chunck_generator(filename, header=False, chunk_size=10 ** 3)
    for row in chunk:
        yield row


def remoteSpecialChTweets(tweet):
    # chunk_df.apply(lambda row: re.sub('(rt)', '',re.sub('(http|https|ftp)\S+(?=( |$))', '',re.sub('(?<=)# .+?(?=( |$))', '',re.sub('(?<=)@ .+?(?=( |$))', '',str(row.text).lower())))))
    lowerTweet = str(tweet).lower().rstrip('\n')
    new_string = re.sub('(?<=)@.+?(?=( |$))', '', lowerTweet)
    new_string = re.sub('(rt)', '', new_string)
    new_string = re.sub('(http|https|ftp)\S+(?=( |$))', '', new_string)
    new_string = re.sub('(?<=)#.+?(?=( |$))', '', new_string)
    new_string = re.sub('(?<=)@.+?(?=(|$))', '', new_string)
    new_string = re.sub('(http|https|ftp)\S+(?=(|$))', '', new_string)
    new_string = re.sub('(?<=)#.+?(?=(|$))', '', new_string)
    return new_string


def removeStopWords(row):
    language = row['language_desc']

    stop_words = getStopWords(str(language))
    if stop_words != None:
        # new_tweet = ' '.join([word for word in nltk.tokenize.word_tokenize(str(row['pre_proc_tweet'])) if word not in stop_words])
        space = ' '
        new_tweet = ''
        for word in nltk.tokenize.word_tokenize(str(row['pre_proc_tweet'])):
            if(word not in stop_words):
                new_tweet = new_tweet + word + space

        return new_tweet


def addPartsSpeech(tweet):
    pos_tag = str(nltk.pos_tag(nltk.tokenize.word_tokenize(str(tweet))))
    return pos_tag


def stemFilter(tweet):
    porter = nltk.stem.porter.PorterStemmer()
    stemF = ' '.join([porter.stem(word)
                      for word in nltk.tokenize.word_tokenize(str(tweet))])
    return stemF
    # df.apply(lambda row: ' '.join([porter.stem(word) for word in nltk.tokenize.word_tokenize(str(row.stop_filter))]),axis=1)


def lemmatizer(pos_tag):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lem = ' '.join([lemmatizer.lemmatize(word) if (wordnet.ADJ if pos_tag.startswith('J') else wordnet.VERB if pos_tag.startswith('V') else wordnet.NOUN if pos_tag.startswith('N') else wordnet.ADV if pos_tag.startswith('R') else None) is None else lemmatizer.lemmatize(
        word, (wordnet.ADJ if pos_tag.startswith('J') else wordnet.VERB if pos_tag.startswith('V') else wordnet.NOUN if pos_tag.startswith('N') else wordnet.ADV if pos_tag.startswith('R') else None)) for word, pos_tag in eval(pos_tag)])
    return lem


def cleanMentions(mentions, is_retweet):
    mentions = str(mentions)
    new_mentions = mentions.replace(
        '\'No Mentions Associated with Tweet\',', '')
    new_mentions = mentions.replace(
        '\'No Mentions Associated with Tweet\'', '')
    new_mentions = new_mentions.replace(
        '[', '').replace(']', '').replace(',', '')
    new_mentions = new_mentions.replace('nan', '')
    new_mentions = new_mentions.replace('\'', '')

    if is_retweet == 'TRUE':
        new_mentions = new_mentions.split(' ')
        new_mentions = new_mentions[1:]
        new_mentions = ' '.join(new_mentions)
        # new_mentions = list([new_mentions])
        # new_mentions = new_mentions.pop(0)

    new_mentions = new_mentions.replace(' ', ',')
    new_mentions = new_mentions.replace('[]', '')

    return new_mentions


def breakWords(tweet):
    tweet = str(tweet).lower()
    new_tweet = tweet.replace("don't", "do not")
    new_tweet = new_tweet.replace("can't", "can not")
    new_tweet = new_tweet.replace("cant", "can not")
    new_tweet = new_tweet.replace("dont", "do not")
    new_tweet = new_tweet.replace("isn't", "is not")
    new_tweet = new_tweet.replace("won't", "will not")
    new_tweet = new_tweet.replace("shouldn't", "should not")
    new_tweet = new_tweet.replace("wouldn't", "would not")
    new_tweet = new_tweet.replace("it's", "it is")
    new_tweet = new_tweet.replace("you're", "you are")
    new_tweet = new_tweet.replace("i'm", "i am")
    new_tweet = new_tweet.replace("aren't", "are not")
    new_tweet = new_tweet.replace("doesn't", "does not")
    new_tweet = new_tweet.replace("where's", "where is")
    new_tweet = new_tweet.replace("haven't", "have not")
    new_tweet = new_tweet.replace("i've", "i have")
    new_tweet = new_tweet.replace("you've", "you have")
    new_tweet = new_tweet.replace('``', '')
    return new_tweet


def removeNotSupportedLang(lang):
    language = str(lang)
    if(language in('english', 'french', 'dutch', 'german', 'swedish', 'spanish', 'italian', 'hindi')):
        return 1
    else:
        return 0


def concatTweet_Retweet(tweet, retweet):
    t = str(tweet).replace('nan', '')
    rt = str(retweet).replace('nan', '')
    new_tweet = t + rt
    return new_tweet


def clean(chunk_df, file_name, source):
    chunk_df['language_desc'] = chunk_df['language'].map({'en': 'english', 'und': 'unidentified', 'fr': 'french', 'nl': 'Dutch',
                                                          'de': 'german', 'sv': 'swedish', 'ja': 'japanese', 'es': 'spanish', 'ko': 'korean',
                                                          'it': 'italian', 'hi': 'hindi'})

    #chunk_df.replace('\n', '', regex=True, inplace=True)
    # chunk_df['text'] = chunk_df['text'].replace(
    #     r'\r\n', ' ', regex=True, inplace=True)
    # chunk_df['text_retweet'] = chunk_df['text_retweet'].replace(
    #     r'\r\n', ' ', regex=True, inplace=True)
    # chunk_df['location'] = chunk_df['location'].replace(
    #     r'\r\n', ' ', regex=True, inplace=True)
    # chunk_df['profile_description'] = chunk_df['profile_description'].replace(
    #     r'\r\n', ' ', regex=True, inplace=True)
    chunk_df['text'] = chunk_df['text'].str.replace(
        '\r', '').replace('\n').replace('\r\n')
    chunk_df['text_retweet'] = chunk_df['text_retweet'].str.replace(
        '\r', '').replace('\n').replace('\r\n')
    chunk_df['location'] = chunk_df['location'].str.replace(
        '\r', '').replace('\n').replace('\r\n')
    chunk_df['profile_description'] = chunk_df['profile_description'].str.replace(
        '\r', '').replace('\n').replace('\r\n')
    # chunk_df['text_retweet'] = chunk_df['text_retweet'].str.replace(
    #     '\r\n', ' ', regex=True)
    # chunk_df['location'] = chunk_df['location'].str.replace(
    #     '\r\n', ' ', regex=True)
    # chunk_df['profile_description'] = chunk_df['profile_description'].str.replace(
    #     '\r\n', ' ', regex=True)
    #chunk_df['tweet_full'] = chunk_df['text'] + chunk_df['text_retweet']
    chunk_df['tweet_full'] = chunk_df.apply(
        lambda x: concatTweet_Retweet(x.text, x.text_retweet), axis=1)
    if(source == 'twitter'):
        # chunk_df_text = chunk_df['text']  # .dropna()
        # chunk_df_textrt = chunk_df['text_retweet']  # .dropna()
        # chunk_df_full = chunk_df_text.append(chunk_df_textrt)  # .reset_index()
        # chunk_df['tweet_full'] = chunk_df_full
        chunk_df = chunk_df[chunk_df['language_desc'].apply(
            removeNotSupportedLang) != 0]
        chunk_df['mentions'] = chunk_df.apply(
            lambda x: cleanMentions(x.mentions, x.is_retweet), axis=1)
    else:
        chunk_df['created_date'] = chunk_df['created_at']

    chunk_df['tweet_full'] = chunk_df['tweet_full'].apply(breakWords)

    chunk_df['hashtags'] = chunk_df['hashtags'].apply(
        lambda x: str(x).replace('\'', '').replace('nan', ''))

    chunk_df['mentions'] = chunk_df['mentions'].apply(
        lambda x: str(x).replace('\'', '').replace('nan', ''))

    chunk_df['pre_proc_tweet'] = chunk_df['tweet_full'].apply(
        remoteSpecialChTweets)

    chunk_df['stop_filter_tweet'] = chunk_df.apply(removeStopWords, axis=1)
    chunk_df['pos_tags'] = chunk_df['stop_filter_tweet'].apply(addPartsSpeech)
    chunk_df['stem_filter'] = chunk_df['stop_filter_tweet'].apply(stemFilter)
    chunk_df['lemma_filter'] = chunk_df['pos_tags'].apply(lemmatizer)
    chunk_df['lemma_filter'] = chunk_df['lemma_filter'].map(
        lambda x: str(x).replace('“', '').replace('”', '').replace('\"', '').replace("``", ''))
    chunk_df = chunk_df.apply(lambda x: x.replace(';', ''))

    chunk_df['id'] = chunk_df.index
    chunk_df['source'] = source

    columnsTitles = ['id', 'source', 'created_date', 'is_retweet', 'text', 'text_retweet', 'language', 'hashtags', 'mentions', 'location', 'geo_location',
                     'geo_country', 'geo_coordinates', 'user_created_at', 'screen_name', 'name',	'profile_description', 'total_number_of_tweets', 'is_verified',
                     'followers_count', 'friends_count', 'retweets_count', 'favorite_count', 'url', 'listed_count', 'default_profile', 'default_profile_image', 'has_extended_profile',
                     'language_desc', 'tweet_full', 'pre_proc_tweet', 'stop_filter_tweet', 'pos_tags', 'stem_filter', 'lemma_filter']

    chunk_df = chunk_df.reindex(columns=columnsTitles)
    # chunk_df.to_csv('test.csv', sep=';', encoding='utf-8',
    #                 index=False, header=True)
    chunk_df.to_csv(file_name, sep=';', encoding='utf-8',
                    index=False, header=True, quotechar="\"")


def combineInstagram_TwitterDatasets():
    filename = r'instagram/scrapy_instagram/scraped/metoo/metoo/metoo_2019.json'
    generator = generator_json(filename=filename)
    i = 0
    while True:
        try:
            # print(next(generator))
            outputFile = 'twitter/data_preprocess/instagram/insta_clean_' + \
                str(i) + '.csv'
            new_df = match_twitterdata(next(generator))
            clean(new_df, outputFile, 'instagram')
            i += 1
        except StopIteration:
            break


def populateTweet(tweet):
    t = str(tweet).lower()
    new_t = ''
    if 'repost' not in t and 'regram' not in t:
        new_t = t
    return new_t


def populateReTweet(tweet):
    t = str(tweet).lower()
    new_t = ''
    if 'repost' in t or 'regram' in t:
        new_t = t
    return new_t


def is_retweet(tweet):
    rt = str(tweet).lower()
    if 'repost' in rt or 'regram' in rt:
        return 'TRUE'
    else:
        return 'FALSE'


def getHashtags(tweet):
    t = str(tweet)
    list_hashtags = [i for i in t.split() if i.startswith("#")]
    return list_hashtags


def getMentions(tweet):
    t = str(tweet)
    list_mentions = [i for i in t.split() if i.startswith("@")]
    return list_mentions


def match_twitterdata(chunk_df):
    # ['caption', 'comment_count', 'display_url', 'id_', 'is_ad',
    #  'likes_count', 'loc_id', 'loc_lat', 'loc_lon', 'loc_name',
    #  'owner_fullname', 'owner_id', 'owner_username', 'shortcode',
    #  'tagged_user', 'taken_at_timestamp']
    chunk_df['created_at'] = pd.to_datetime(
        chunk_df['taken_at_timestamp'], unit='s')

    chunk_df['is_retweet'] = chunk_df['caption'].apply(is_retweet)
    chunk_df['text'] = chunk_df['caption'].apply(populateTweet)
    chunk_df['text_retweet'] = chunk_df['caption'].apply(populateReTweet)
    chunk_df['language'] = 'en'
    chunk_df['hashtags'] = chunk_df['caption'].apply(getHashtags)
    chunk_df['hashtags'] = chunk_df['hashtags'].apply(
        lambda x: str(x).replace('[', '').replace(']', ''))
    # chunk_df['caption'].apply(getMentions)
    chunk_df['mentions'] = chunk_df['caption'].apply(getMentions)
    chunk_df['mentions'] = chunk_df['mentions'].apply(
        lambda x: str(x).replace('[', '').replace(']', ''))
    chunk_df['location'] = ''
    chunk_df['geo_location'] = ''
    chunk_df['geo_country'] = ''
    chunk_df['geo_coordinates'] = chunk_df['loc_lat'] + chunk_df['loc_lon']
    chunk_df['user_created_at'] = ''
    chunk_df['screen_name'] = chunk_df['owner_username']
    chunk_df['name'] = chunk_df['owner_fullname']
    chunk_df['profile_description'] = ''
    chunk_df['total_number_of_tweets'] = 0
    chunk_df['is_verified'] = chunk_df['is_ad']
    chunk_df['followers_count'] = chunk_df['comment_count']
    chunk_df['friends_count'] = 0
    chunk_df['retweets_count'] = 0
    chunk_df['favorite_count'] = chunk_df['likes_count']
    chunk_df['url'] = chunk_df['display_url']
    chunk_df['listed_count'] = 0
    chunk_df['default_profile'] = 'FALSE'
    chunk_df['default_profile_image'] = 'FALSE'
    chunk_df['has_extended_profile'] = 'FALSE'

    columnsTitles = ['id_', 'created_at', 'is_retweet',
                     'text', 'text_retweet', 'language', 'hashtags', 'mentions', 'location', 'geo_location', 'geo_country', 'geo_coordinates', 'user_created_at',
                     'screen_name', 'name', 'profile_description', 'total_number_of_tweets', 'is_verified', 'followers_count', 'friends_count', 'retweets_count',
                     'favorite_count', 'url', 'listed_count', 'default_profile', 'default_profile_image', 'has_extended_profile']
    chunk_df = chunk_df.reindex(columns=columnsTitles)
    chunk_df.apply(lambda x: str(x).replace(';', ''))
    print('Finished transforming instagram dataset')
    print('Starting matching twitter schema')
    # chunk_df.to_csv('out.csv', sep=';', encoding='utf-8',
    #                 index=False, header=True)
    return chunk_df


def twitterClean2019():
    filename = r'twitter/metoo_2019.csv'

    generatorVar = generator(filename=filename)
    i = 0
    while True:
        try:
            outputFile = 'twitter/data_preprocess/twitter/2019/tweet_clean_' + \
                str(i) + '.csv'
            clean(next(generatorVar), outputFile, 'twitter')
            i += 1
        except StopIteration:
            break


def twitterClean2018_2017():
    filename = r'twitter/metoo_2018_2017.csv'
    generatorVar = generator(filename=filename)
    i = 0
    while True:
        try:
            outputFile = 'twitter/data_preprocess/twitter/2018_2017/tweet_clean_' + \
                str(i) + '.csv'
            clean(next(generatorVar), outputFile, 'twitter')
            i += 1
        except StopIteration:
            break


if __name__ == "__main__":
    print('Starting transforming instagram dataset')
    combineInstagram_TwitterDatasets()
    print('Finished matching twitter schema')
    print('Starting cleaning twitter 2019 dataset')
    twitterClean2019()
    print('Finished cleaning twitter 2019 dataset')
    print('Starting cleaning twitter 2018 and 2017 dataset')
    twitterClean2018_2017()
    print('Finished cleaning twitter 2018 and 2017 dataset')
