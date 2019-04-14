import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import warnings
import time
from sklearn import metrics
mpl.rcParams['patch.force_edgecolor'] = True
warnings.filterwarnings("ignore")
# %matplotlib inline


class twitter_bot(object):
    def __init__(self):
        pass

    def perform_train_test_split(df):
        msk = np.random.rand(len(df)) < 0.75
        train, test = df[msk], df[~msk]
        X_train, y_train = train, train.ix[:, -2]
        X_test, y_test = test, test.ix[:, -2]
        return (X_train, y_train, X_test, y_test)

    def bot_prediction_algorithm(df):
        # creating copy of dataframe
        train_df = df.copy()
        train_df['id'] = train_df.index
        train_df['bot'] = ''
        if train_df.shape[0] > 600:
            # bag_of_words_for_bot
            bag_of_words_bot = r'bot|b0t|cannabis|tweet me|mishear|follow me|updates every|gorilla|yes_ofc|forget' \
                r'expos|kill|clit|bbb|butt|fuck|XXX|sex|truthe|fake|anony|free|virus|funky|RNA|kuck|jargon' \
                r'nerd|swag|jack|bang|bonsai|chick|prison|paper|pokem|xx|freak|ffd|dunia|clone|genie|bbb' \
                r'ffd|onlyman|emoji|joke|troll|droop|free|every|wow|cheese|yeah|bio|magic|wizard|face'
        else:
            # bag_of_words_for_bot
            bag_of_words_bot = r'bot|b0t|cannabis|mishear|updates every'

        listBots = pd.read_csv('listBots.csv').values
        # check if the name contains bot or screenname contains b0t
        condition = ((train_df.name.str.contains(bag_of_words_bot, case=False, na=False)) |
                     (train_df.profile_description.str.contains(bag_of_words_bot, case=False, na=False)) |
                     (train_df.screen_name.str.contains(bag_of_words_bot, case=False, na=False)) |
                     (train_df.tweet_full.str.contains(
                         bag_of_words_bot, case=False, na=False))

                     )  # these all are bots
        predicted_df = train_df[condition]  # these all are bots
        predicted_df['bot'] = 1
        predicted_df = predicted_df[['id', 'bot']]

        # check if the user is verified
        verified_df = train_df[~condition]
        condition = (verified_df.is_verified == 1)  # these all are nonbots
        predicted_df1 = verified_df[condition][['id', 'bot']]
        predicted_df1['bot'] = 0
        predicted_df = pd.concat([predicted_df, predicted_df1])

        # check if description contains buzzfeed
        buzzfeed_df = verified_df[~condition]
        condition = (buzzfeed_df.profile_description.str.contains(
            "buzzfeed", case=False, na=False))  # these all are nonbots
        predicted_df1 = buzzfeed_df[buzzfeed_df.profile_description.str.contains(
            "buzzfeed", case=False, na=False)][['id', 'bot']]
        predicted_df1['bot'] = 0
        predicted_df = pd.concat([predicted_df, predicted_df1])

        listed_count_df = buzzfeed_df[~condition]
        condition = (listed_count_df.listed_count >
                     16000)  # these all are nonbots
        predicted_df1 = listed_count_df[condition][['id', 'bot']]
        predicted_df1['bot'] = 0
        predicted_df = pd.concat([predicted_df, predicted_df1])

        # remaining
        predicted_df1 = listed_count_df[~condition][['id', 'bot']]
        predicted_df1['bot'] = 0  # these all are nonbots
        predicted_df = pd.concat([predicted_df, predicted_df1])
        return predicted_df

    def bot_prediction_test(df):
        # creating copy of dataframe
        train_df = df.copy()
        train_df['id'] = train_df.index
        train_df['bot'] = ''
        if train_df.shape[0] > 600:
            # bag_of_words_for_bot
            bag_of_words_bot = r'bot|b0t|cannabis|tweet me|mishear|follow me|updates every|gorilla|yes_ofc|forget' \
                r'expos|kill|clit|bbb|butt|fuck|XXX|sex|truthe|fake|anony|free|virus|funky|RNA|kuck|jargon' \
                r'nerd|swag|jack|bang|bonsai|chick|prison|paper|pokem|xx|freak|ffd|dunia|clone|genie|bbb' \
                r'ffd|onlyman|emoji|joke|troll|droop|free|every|wow|cheese|yeah|bio|magic|wizard|face'
        else:
            # bag_of_words_for_bot
            bag_of_words_bot = r'bot|b0t|cannabis|mishear|updates every'

        listBots = pd.read_csv('listBots.csv').values
        # check if the name contains bot or screenname contains b0t
        condition = ((train_df.name.str.contains(bag_of_words_bot, case=False, na=False)) |
                     (train_df.profile_description.str.contains(bag_of_words_bot, case=False, na=False)) |
                     (train_df.screen_name.str.contains(bag_of_words_bot, case=False, na=False)) |
                     (train_df.tweet_full.str.contains(
                         bag_of_words_bot, case=False, na=False))

                     )  # these all are bots
        predicted_df = train_df[condition]  # these all are bots
        predicted_df['bot'] = 1

        predicted_df = predicted_df[['id',
                                     'source',
                                     'created_date',
                                     'is_retweet',
                                     'text',
                                     'text_retweet',
                                     'language',
                                     'hashtags',
                                     'mentions',
                                     'location',
                                     'geo_location',
                                     'geo_country',
                                     'geo_coordinates',
                                     'user_created_at',
                                     'screen_name',
                                     'name',
                                     'profile_description',
                                     'total_number_of_tweets',
                                     'is_verified',
                                     'followers_count',
                                     'friends_count',
                                     'retweets_count',
                                     'favorite_count',
                                     'url',
                                     'listed_count',
                                     'default_profile',
                                     'default_profile_image',
                                     'has_extended_profile',
                                     'language_desc',
                                     'tweet_full',
                                     'pre_proc_tweet',
                                     'stop_filter_tweet',
                                     'pos_tags',
                                     'stem_filter',
                                     'lemma_filter',
                                     'bot']]

        # check if the user is verified
        verified_df = train_df[~condition]
        condition = (verified_df.is_verified == 1)  # these all are nonbots
        predicted_df1 = verified_df[condition][['id',
                                                'source',
                                                'created_date',
                                                'is_retweet',
                                                'text',
                                                'text_retweet',
                                                'language',
                                                'hashtags',
                                                'mentions',
                                                'location',
                                                'geo_location',
                                                'geo_country',
                                                'geo_coordinates',
                                                'user_created_at',
                                                'screen_name',
                                                'name',
                                                'profile_description',
                                                'total_number_of_tweets',
                                                'is_verified',
                                                'followers_count',
                                                'friends_count',
                                                'retweets_count',
                                                'favorite_count',
                                                'url',
                                                'listed_count',
                                                'default_profile',
                                                'default_profile_image',
                                                'has_extended_profile',
                                                'language_desc',
                                                'tweet_full',
                                                'pre_proc_tweet',
                                                'stop_filter_tweet',
                                                'pos_tags',
                                                'stem_filter',
                                                'lemma_filter',
                                                'bot']]
        predicted_df1['bot'] = 0
        predicted_df = pd.concat([predicted_df, predicted_df1])

        # check if description contains buzzfeed
        buzzfeed_df = verified_df[~condition]
        condition = (buzzfeed_df.profile_description.str.contains(
            "buzzfeed", case=False, na=False))  # these all are nonbots
        predicted_df1 = buzzfeed_df[buzzfeed_df.profile_description.str.contains(
            "buzzfeed", case=False, na=False)][['id',
                                                'source',
                                                'created_date',
                                                'is_retweet',
                                                'text',
                                                'text_retweet',
                                                'language',
                                                'hashtags',
                                                'mentions',
                                                'location',
                                                'geo_location',
                                                'geo_country',
                                                'geo_coordinates',
                                                'user_created_at',
                                                'screen_name',
                                                'name',
                                                'profile_description',
                                                'total_number_of_tweets',
                                                'is_verified',
                                                'followers_count',
                                                'friends_count',
                                                'retweets_count',
                                                'favorite_count',
                                                'url',
                                                'listed_count',
                                                'default_profile',
                                                'default_profile_image',
                                                'has_extended_profile',
                                                'language_desc',
                                                'tweet_full',
                                                'pre_proc_tweet',
                                                'stop_filter_tweet',
                                                'pos_tags',
                                                'stem_filter',
                                                'lemma_filter',
                                                'bot']]
        predicted_df1['bot'] = 0
        predicted_df = pd.concat([predicted_df, predicted_df1])

        listed_count_df = buzzfeed_df[~condition]
        condition = (listed_count_df.listed_count >
                     16000)  # these all are nonbots
        predicted_df1 = listed_count_df[condition][['id',
                                                    'source',
                                                    'created_date',
                                                    'is_retweet',
                                                    'text',
                                                    'text_retweet',
                                                    'language',
                                                    'hashtags',
                                                    'mentions',
                                                    'location',
                                                    'geo_location',
                                                    'geo_country',
                                                    'geo_coordinates',
                                                    'user_created_at',
                                                    'screen_name',
                                                    'name',
                                                    'profile_description',
                                                    'total_number_of_tweets',
                                                    'is_verified',
                                                    'followers_count',
                                                    'friends_count',
                                                    'retweets_count',
                                                    'favorite_count',
                                                    'url',
                                                    'listed_count',
                                                    'default_profile',
                                                    'default_profile_image',
                                                    'has_extended_profile',
                                                    'language_desc',
                                                    'tweet_full',
                                                    'pre_proc_tweet',
                                                    'stop_filter_tweet',
                                                    'pos_tags',
                                                    'stem_filter',
                                                    'lemma_filter',
                                                    'bot']]
        predicted_df1['bot'] = 0
        predicted_df = pd.concat([predicted_df, predicted_df1])

        # remaining
        predicted_df1 = listed_count_df[~condition][['id',
                                                     'source',
                                                     'created_date',
                                                     'is_retweet',
                                                     'text',
                                                     'text_retweet',
                                                     'language',
                                                     'hashtags',
                                                     'mentions',
                                                     'location',
                                                     'geo_location',
                                                     'geo_country',
                                                     'geo_coordinates',
                                                     'user_created_at',
                                                     'screen_name',
                                                     'name',
                                                     'profile_description',
                                                     'total_number_of_tweets',
                                                     'is_verified',
                                                     'followers_count',
                                                     'friends_count',
                                                     'retweets_count',
                                                     'favorite_count',
                                                     'url',
                                                     'listed_count',
                                                     'default_profile',
                                                     'default_profile_image',
                                                     'has_extended_profile',
                                                     'language_desc',
                                                     'tweet_full',
                                                     'pre_proc_tweet',
                                                     'stop_filter_tweet',
                                                     'pos_tags',
                                                     'stem_filter',
                                                     'lemma_filter',
                                                     'bot']]
        predicted_df1['bot'] = 0  # these all are nonbots
        predicted_df = pd.concat([predicted_df, predicted_df1])
        return predicted_df

    def get_predicted_and_true_values(features, target):
        y_pred, y_true = twitter_bot.bot_prediction_algorithm(
            features).bot.tolist(), target.tolist()
        return (y_pred, y_true)

    def get_accuracy_score(df):
        (X_train, y_train, X_test, y_test) = twitter_bot.perform_train_test_split(df)
        # predictions on training data
        y_pred_train, y_true_train = twitter_bot.get_predicted_and_true_values(
            X_train, y_train)
        train_acc = metrics.accuracy_score(y_pred_train, y_true_train)
        # predictions on test data
        y_pred_test, y_true_test = twitter_bot.get_predicted_and_true_values(
            X_test, y_test)
        test_acc = metrics.accuracy_score(y_pred_test, y_true_test)
        return (train_acc, test_acc)


if __name__ == '__main__':
    start = time.time()
    epochs = 10

    train_df = pd.read_csv('data/train/train.csv', delimiter=';',
                           encoding='utf8', engine='python')
    test_df = pd.read_csv('data/test/metoodata.csv', delimiter=';',
                          encoding='utf8', engine='python')

    while(epochs > 0):
        print("Epoch : " + str(epochs))
        print("Train Accuracy: ",
              twitter_bot.get_accuracy_score(train_df)[0])
        print("Test Accuracy: ",
              twitter_bot.get_accuracy_score(train_df)[1])
        print("\n")
        epochs -= 1

    predicted_df = twitter_bot.bot_prediction_test(test_df)
    predicted_df.to_csv('prediction_bot_humans.csv', sep=';', encoding='utf-8',
                        index=False, header=True)
    humans = predicted_df[predicted_df['bot'] == 0]
    humans.to_csv('humans.csv', sep=';', encoding='utf-8',
                  index=False, header=True)
