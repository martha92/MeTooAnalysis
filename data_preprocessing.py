
import pandas as pd
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
from autocorrect import spell
import re

#filename='twitter/metoo_all_items.csv'
#output = 'twitter/data_preprocess'

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
stop_words_en = set(nltk.corpus.stopwords.words('english'))
stop_words_fr = set(nltk.corpus.stopwords.words('french'))
stop_words_dutch = set(nltk.corpus.stopwords.words('dutch'))
stop_words_gm = set(nltk.corpus.stopwords.words('german'))
stop_words_sw = set(nltk.corpus.stopwords.words('swedish'))
stop_words_sp = set(nltk.corpus.stopwords.words('spanish'))
stop_words_it = set(nltk.corpus.stopwords.words('italian'))

def getStopWords(language):
    if (language in ['english','french','dutch','german','swedish','spanish','italian']):
        stop_words = set(nltk.corpus.stopwords.words(language))
        return stop_words
    return None

def chunck_generator(filename, header=False,chunk_size = 10 ** 5):
    for chunk in pd.read_csv(filename,delimiter=',', iterator=True, chunksize=chunk_size, parse_dates=[1,12] ): 
        yield (chunk)

def generator( filename, header=False,chunk_size = 10 ** 5):
    chunk = chunck_generator(filename, header=False,chunk_size = 10 ** 5)
    for row in chunk:
        yield row

def remoteSpecialChTweets(tweet):
    #chunk_df.apply(lambda row: re.sub('(rt)', '',re.sub('(http|https|ftp)\S+(?=( |$))', '',re.sub('(?<=)# .+?(?=( |$))', '',re.sub('(?<=)@ .+?(?=( |$))', '',str(row.text).lower())))))
    lowerTweet  = str(tweet).lower().rstrip('\n')
    new_string = re.sub('(?<=)@.+?(?=( |$))', '', lowerTweet)
    new_string = re.sub('(rt)','',new_string)
    new_string = re.sub('(http|https|ftp)\S+(?=( |$))','',new_string)
    new_string = re.sub('(?<=)#.+?(?=( |$))','',new_string)
    return new_string

def removeStopWords(row):
    language = row['language_desc']
    stop_words = getStopWords(str(language))
    if stop_words != None:
        new_tweet = ' '.join([word for word in nltk.tokenize.word_tokenize(str(row['pre_proc_tweet'])) if not word in stop_words])
        return new_tweet
def addPartsSpeech(tweet):
    pos_tag = str(nltk.pos_tag(nltk.tokenize.word_tokenize(str(tweet))))
    return pos_tag

def stemFilter(tweet):
    porter = nltk.stem.porter.PorterStemmer()
    stemF = ' '.join([porter.stem(word) for word in nltk.tokenize.word_tokenize(str(tweet))] )
    return stemF
    #df.apply(lambda row: ' '.join([porter.stem(word) for word in nltk.tokenize.word_tokenize(str(row.stop_filter))]),axis=1)

def lemmatizer(pos_tag):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lem = ' '.join([lemmatizer.lemmatize(word) if (wordnet.ADJ if pos_tag.startswith('J') else wordnet.VERB if pos_tag.startswith('V') else wordnet.NOUN if pos_tag.startswith('N') else wordnet.ADV if pos_tag.startswith('R') else None) is None else lemmatizer.lemmatize(word, (wordnet.ADJ if pos_tag.startswith('J') else wordnet.VERB if pos_tag.startswith('V') else wordnet.NOUN if pos_tag.startswith('N') else wordnet.ADV if pos_tag.startswith('R') else None)) for word, pos_tag in eval(pos_tag)])
    return lem

def cleanMentions(mentions):
    new_mentions = mentions.replace('No Mentions Associated with Tweet', '')
    #new_mentions = mentions.replace('|','').replace(']','')
    return new_mentions

def breakWords(tweet):
    tweet = str(tweet)
    new_tweet =tweet.replace("don't","do not")
    new_tweet =new_tweet.replace("can't","can not")
    new_tweet =new_tweet.replace("cant","can not")
    new_tweet =new_tweet.replace("dont","do not")
    new_tweet =new_tweet.replace("isn't","is not")
    new_tweet =new_tweet.replace("won't","will not")
    new_tweet =new_tweet.replace("shouldn't","should not")
    new_tweet =new_tweet.replace("wouldn't","would not")
    return new_tweet
def clean(chunk_df, file_name):
    chunk_df['language_desc'] = chunk_df['language'].map({'en': 'english', 'und': 'unidentified', 'fr': 'french', 'nl': 'Dutch',
                                'de': 'german', 'sv': 'swedish', 'ja': 'japanese', 'es': 'spanish', 'ko': 'korean',
                                'it': 'italian'})
    
    chunk_df['tweet_full'] =  chunk_df[['text', 'text_retweet']].apply(lambda x: ''.join(str(x)), axis=1) 
    chunk_df['tweet_full'] = chunk_df['tweet_full'].apply(breakWords)
    chunk_df['mentions'] =  chunk_df['mentions'].apply(cleanMentions)
    chunk_df['pre_proc_tweet'] = chunk_df['tweet_full'].apply(remoteSpecialChTweets)
    chunk_df['stop_filter_tweet'] = chunk_df.apply(removeStopWords,axis=1)
    chunk_df['pos_tags'] = chunk_df['stop_filter_tweet'].apply(addPartsSpeech)
    chunk_df['stem_filter'] = chunk_df['stop_filter_tweet'].apply(stemFilter)
    chunk_df['lemma_filter'] = chunk_df['pos_tags'].apply(lemmatizer)

    chunk_df.to_csv(file_name, sep=',', encoding='utf-8', index = False, header=True)

if __name__ == "__main__":
    filename = r'twitter/metoo_all_items.csv'
    generator = generator(filename=filename)
    
    i=0
    
    while True:
        try:
            outputFile='twitter/data_preprocess/tweet_clean_' + str(i) + '.csv'
            clean(next(generator), outputFile)
            i+=1
        except StopIteration:
            break
        