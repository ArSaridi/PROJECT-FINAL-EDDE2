!python -m spacy download el_core_news_sm

from google.colab import drive
drive.mount('/content/gdrive')

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
# %matplotlib inline
import numpy as np
import re
from datetime import datetime
import glob
from sklearn.feature_extraction.text import CountVectorizer
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('ggplot')

filepath = "https://raw.githubusercontent.com/datajour-gr/Data_journalism/master/week10/NRC_GREEK_Translated_6_2020.csv"
emolex_df = pd.read_csv(filepath)
emolex_df.head()

emolex_df = emolex_df.drop_duplicates(subset=['word'])
emolex_df = emolex_df.dropna()
emolex_df.reset_index(drop = True, inplace = True)

import spacy
nlp = spacy.load('el_core_news_sm')

df = pd.read_csv("/content/gdrive/My Drive/Colab Notebooks/gynaikoktonia_scraping_efsyn.csv")
df

df['Time'] = pd.to_datetime(df.Time , format='%d.%m.%Y, %H:%M')
df['Time']
df

df['year'] = pd.DatetimeIndex(df['Time']).year
df['month'] = pd.DatetimeIndex(df['Time']).month
df['day'] = pd.DatetimeIndex(df['Time']).day
df

df['month'] = pd.to_datetime(df['month'], format='%m').dt.month_name().str.slice(stop=3)

df.dtypes

def cleanTxt(text):
  text = re.sub(r'[^\w\s]', '', text)   #Removing puncuations
  text = text.lower()                     #Converting letters to lowercase
  text = text.replace('\xa0','')       #Removing \xa0 character(it means space)
  text = text.replace('\t','')        #Removing \t character(similar to the indentation function in the document,Tab key)
  text = text.replace('\n','')
  #text = re.sub('\d+', '', text)      #Removing numbers
# Return the cleaned text
  return text
#Clean the tweets
df['Summary'] = df['Summary'].apply(cleanTxt)
df['Title'] =  df['Title'].apply(cleanTxt)
#Show the cleaned tweets
df

emolex_df['word'].head(3)

vec = CountVectorizer(analyzer = 'word', vocabulary = emolex_df.word,
                      strip_accents = 'unicode',
                      stop_words= nlp.Defaults.stop_words,
                      ngram_range=(1, 2))

matrix = vec.fit_transform(df['Summary'])
vocab = vec.get_feature_names()
wordcount_df = pd.DataFrame(matrix.toarray(), columns=vocab)
wordcount_df.head()

emolex_df.head()

angry_words = emolex_df[emolex_df.Anger == 1]['word']

positive_words = emolex_df[emolex_df.Positive == 1]['word']


# Φτιάξε μια λίστα με sadness words
sadness_words = emolex_df[emolex_df.Sadness == 1]['word']


# Φτιάξε μια λίστα με surprise words
surprise_words = emolex_df[emolex_df.Surprise == 1]['word']


# Φτιάξε μια λίστα με disgust words
disgust_words = emolex_df[emolex_df.Disgust == 1]['word']


# Φτιάξε μια λίστα με anticipation(προσδοκία) words
anticipation_words = emolex_df[emolex_df.Anticipation == 1]['word']


# Φτιάξε μια λίστα με negative words
negative_words = emolex_df[emolex_df.Negative == 1]['word']



# Φτιάξε μια λίστα με joy words
joy_words = emolex_df[emolex_df.Joy == 1]['word']


# Φτιάξε μια λίστα με trust words
trust_words = emolex_df[emolex_df.Trust == 1]['word']



# Φτιάξε μια λίστα με fear words
fear_words = emolex_df[emolex_df.Fear == 1]['word']

df['anger'] = wordcount_df[angry_words].sum(axis=1)

df['positivity'] = wordcount_df[positive_words].sum(axis=1)


df['joy'] = wordcount_df[joy_words].sum(axis=1)


df['disgust'] = wordcount_df[disgust_words].sum(axis=1)


df['surprise'] = wordcount_df[surprise_words].sum(axis=1)

df['trust'] = wordcount_df[trust_words].sum(axis=1)


df['anticipation'] = wordcount_df[anticipation_words].sum(axis=1)


df['sadness'] = wordcount_df[sadness_words].sum(axis=1)

df['negative'] = wordcount_df[negative_words].sum(axis=1)

df['fear'] = wordcount_df[fear_words].sum(axis=1)

#We don't have NaN values...
df.isnull().values.any()

df.set_index('Time' , inplace=True)
df

from google.colab import drive
drive.mount('/content/gdrive')

df.to_csv('/content/gdrive/My Drive/Colab Notebooks/efsyn_new_sent.csv' )
df

ax = df['positivity'].resample('M').sum().plot(figsize=(16,4), color = 'green',label='pos', )
df['negative'].resample('M').sum().plot(figsize=(20,4), ax = ax, color = 'red',label= 'neg')
df['trust'].resample('M').sum().plot(figsize=(20,8), ax = ax, color = 'blue')
df['anger'].resample('M').sum().plot(figsize=(20,8), ax = ax, color = 'yellow')
df['fear'].resample('M').sum().plot(figsize=(20,8), ax = ax, color = 'black').legend()

#Resamle Time Series from daily to weekly (7d)
df_new = df.resample('7d').sum()

df_new

df_new.to_csv('/content/gdrive/My Drive/Colab Notebooks/efsyn_analysis_final.csv' )
