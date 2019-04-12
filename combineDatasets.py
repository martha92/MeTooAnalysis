import pandas as pd
import glob
import sys
import os


dfGlobal = pd.DataFrame()
if __name__ == "__main__":
    folder_path_list = ['twitter/data_preprocess/twitter/2019/',
                        'twitter/data_preprocess/twitter/2018_2017/', 'twitter/data_preprocess/instagram/']
    for folder_path in folder_path_list:
        for filename in glob.glob(os.path.join(folder_path, '*.csv')):
            with open(filename, 'r') as f:
                print('doing ' + str(filename))
                df = pd.read_csv(filename, delimiter=';',  encoding='utf8', engine='python',
                                 parse_dates=[3, 14])

                dfGlobal = pd.concat([dfGlobal, df])

    dfGlobal.to_csv('metoodata.csv', sep=';', encoding='utf-8',
                    index=False, header=True)
