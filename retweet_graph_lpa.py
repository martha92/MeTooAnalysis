import sys
import pandas as pd
import numpy as np
import re
import os
import pyspark
from pyspark.sql import SparkSession, functions as F
from graphframes import *

spark = SparkSession.builder.appName('retweet graph lpa').getOrCreate()
sc = spark.sparkContext
sc.setLogLevel("WARN")

# Read retweet graph
df = pd.read_csv('retweetgraph.txt', sep='\t', header=None, names=['source', 'target', 'screen_name', 'retweet_user', 'count'])
sdf = spark.createDataFrame(df)

# Define nodes and edges
nodes = sdf.select('source', 'screen_name').union(sdf.select('target', 'retweet_user')).select(F.col('source').alias('id'), F.col('screen_name').alias('name')).drop_duplicates()
edges = sdf.select('source', 'target', 'count').withColumnRenamed('count', 'weight') 

# create graphframe
graph = GraphFrame(nodes, edges)

# Detect communities using LPA and display first few nodes with the cluster numbers
print('First 10 community labels')
communities = graph.labelPropagation(maxIter=5)
communities.persist().show(10)

# Detect main influencers
print('First 10 pagerank labels')
results = graph.pageRank(resetProbability=0.01, maxIter=5)
pagerank = results.vertices.persist()
pagerank.show(10)

# Write the outputs to the files
communities.drop('name').join(pagerank, ['id'], 'inner').write.parquet('retweet_lpa.parquet', mode='overwrite')
#communities.drop('name').join(pagerank, ['id'], 'inner').coalesce(1).write.csv('nodes', sep=',', header=True, mode='overwrite')
nodes.select(F.col('source').alias('id'), F.col('name').alias('label')).coalesce(1).write.csv('edges', sep=',', header=True, mode='overwrite')
edges.coalesce(1).write.csv('edges', sep=',', header=True, mode='overwrite')





