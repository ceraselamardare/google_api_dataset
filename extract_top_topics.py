import re

import pandas as pd

from random import randrange

from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import TfidfVectorizer

from google_api_dataset.procesare_text import procesare_text

df_train = pd.read_csv('stackoverflow_posts.csv', dtype=str)
text_original = df_train['body']

text = df_train['body']
tags = df_train['tags'].dropna()

text, tags = procesare_text(text, tags)

vectorizer_train = TfidfVectorizer(analyzer='word',
                                   min_df=0.0,
                                   max_df=1.0,
                                   max_features=1000)

TF_IDF_matrix = vectorizer_train.fit_transform(text).toarray()


def print_topics(nr_posts, text):
    text_original = text.apply(lambda x: re.sub(r'<code>.+?<\/code>', '', x))
    text_original = text_original.apply(lambda x: BeautifulSoup(x, "html.parser").get_text())

    for i in range(nr_posts):
        index = randrange(len(text))
        doc_scores = TF_IDF_matrix[index]

        df_tf_idf = pd.DataFrame(doc_scores, index=vectorizer_train.get_feature_names(),
                                 columns=['tf_idf_scores'])
        df_tf_idf = df_tf_idf.sort_values(by=['tf_idf_scores'], ascending=False)

        df_tf_idf_dict = df_tf_idf['tf_idf_scores'].to_dict()
        keys = list(df_tf_idf_dict.keys())

        print(text_original[index])
        print("\nTop 3 topics: '{}' with score {}, '{}' with score {}, '{}' with score {}\n\n\n".
              format(keys[0], df_tf_idf_dict[keys[0]],
                     keys[1], df_tf_idf_dict[keys[1]],
                     keys[2], df_tf_idf_dict[keys[2]]))


print_topics(8, text_original)
