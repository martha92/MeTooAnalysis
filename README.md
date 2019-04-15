# MeTooAnalysis

Welcome to the Me Too Analysis repository.
This project has the intend of suggest a targeted approach to spread awareness and help in the society.

We followed the following pipeline:
1. Data Collection. We collected data from twitter and instagram
2. Data Integration. Combined both schemas into a twitter format.
3. Data Cleansing. Remove unecessary characters, stopwords, lemmentation, etc.
4. Perform EDA.
5. Detect Fake vs Real accounts.Custom algorithm to predict if an account is a bot or a human. Generate new file only with humans.
6. Apply topic modelling algorithms like LDA, MalletLDA
7. Create network clusters. Design community clusters of Retweet and Topic network and find primary influencers.
8. Calculate sentiments of each topic cluster based on weighted average of sentiments scores of hashtags network through loopy belief propagation algorithm and lexical scores of the tweets given by textblob.
9. Create visualization component in D3 with final findings.
10. Create an webapp of the datascience process flow along with visualizations.


Steps to execute:  
Pre-requisites.  
* Generate your developer keys from twitter's site.  

Data Collection:    
1. Open the crawlTweets.py file and modify the keys to match yours.  
2. Run -> python crawlTweets.py. This will generate 2 files metoo_2019.csv and metoo_2018_2017.csv  
3. Run the scrapper -> scrapy crawl #metoo . This will generate a file called metoo_2019.json  

Data Cleaning and Integration  
4. Run -> python data_preprocessing.py. This will generate a bunch of files that will do the data cleansing piece.  
5. Run -> python combineDatasets.py . This will integrate instagram and twitter schema into one consolidated one.  

Algorithms: Identify fake accounts. Classify Fake(Bot) vs Real(human) account  
6. Run -> python labelData.py . This will call the botometer library to label some of the data as bot or human.  
7. Run -> python bot_human_custom.py . This will generate 2 files, 1 called prediction_bot_humans.csv with the classification predicted by the algorithm and a file called humans.csv which will only contain the records that were classified as non-fake accounts.  
8. Run-> bot_human.ipynb. This will contain the Random Forest and Decision Tree classifiers.

Algorithms: Retweet Network Analysis  
The Retweet Network folder contains all the output files, visualization and the code for Retweet Network Analysis  
8. Run -> Retweet Network/retweet_graph.ipynb . This python notebook maps data graphically and performs network analysis. In the process it calls retweet_graph_lpa.py which is a pyspark implementation for detecting community clusters and finding influencers.  

Algorithm: Topic Modelling,clustering,sentiments analysis  
Topic_modelling_clustering_sentiments contains all the files for this analysis.  
9. Run -> Topic_modelling_clustering_sentiments/input_HG.ipynb . This python notebook prepares input for Hashtag network  
10. Run -> Topic_modelling_clustering_sentiments/LBP.ipynb . This python notebook prepares runs loopy belief algorithm to compute sentiment scores for Hashtag network  
11. Run -> Topic_modelling_clustering_sentiments/topic_modelling_clustering_sentiments.ipynb . This python notebook performs topic modelling, detects topic community and calculates sentiments of each of the communities using outputs from above two processes.  

Overall EDA and Visualization  
Exploratory Data Analysis and Visualization  
12. Open the notebook MeToo_EDA.ipynb and run all the EDA tasks. This will generate html files that will be used by the visualization app in the future.  


