import botometer
import pandas as pd
import json
import glob
import os
import tweepy


mashape_key = "a60b491990msh747ba224608681cp1a7c43jsnc199bf716bff"
twitter_app_auth = {
    'consumer_key': 'Nv4v8rMM0EgEN8A4BhyvVlFZO',
    'consumer_secret': 'LSKJYisimrn6miy0Om8ndUvgN5jzqkkmFll0k63ZkClyv2sl4L',
    'access_token': '272599379-ZqaPKdzYJ7bAqdR0ubw975gBT1bbWXJz4JISo6Tu',
    'access_token_secret': 'UG5HsGKxeq8Dhq5zPUJEZZSBEOOMQaOoziKMxKBodNl84',
}
bom = botometer.Botometer(wait_on_ratelimit=True,
                          mashape_key=mashape_key,
                          **twitter_app_auth)


def checkBotOrHuman(screen_name):
    try:
        bot = 0
        # Check a single account by screen name
        result = bom.check_account(screen_name)
        if(result['cap']['english'] > 0.50 or result['cap']['universal'] > 0.50):
            bot = 1
    except tweepy.TweepError:
        print("Failed to run the command on that user, Skipping...")
        bot = 1

    print(bot)
    return bot


if __name__ == "__main__":

    folder_path = 'data/train/trainfiles'
    for filename in glob.glob(os.path.join(folder_path, '*.csv')):
        with open(filename, 'r') as f:
            df = pd.read_csv(filename, delimiter=';',  encoding='utf8', engine='python',
                             parse_dates=[1, 12])
            df['bot'] = df['screen_name'].apply(checkBotOrHuman)
            df.to_csv("train.csv", sep=';', encoding='utf-8',
                      index=False, header=True)

    # bot_prediction(df)
