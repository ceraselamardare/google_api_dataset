import itertools
import re

import pandas as pd
from bs4 import BeautifulSoup
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords


def split_words(list):
    split_list = []
    for tags in list:
        tags = str(tags).split('|')
        split_list.append(tags)

    return split_list


def strip_list_noempty(mylist):
    newlist = (item.strip() if hasattr(item, 'strip') else item for item in mylist)
    return [item for item in newlist if item != '']


def clean_punct(text, top_topics):
    punct = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~-'

    text = text.lower()
    words = word_tokenize(text)
    punctuation_filtered = []
    regex = re.compile('[%s]' % re.escape(punct))
    for w in words:
        if w in top_topics:
            punctuation_filtered.append(w)
        else:
            punctuation_filtered.append(regex.sub('', w))

    filtered_list = strip_list_noempty(punctuation_filtered)

    return ' '.join(filtered_list)


def lemitize_words(text):
    lemma = WordNetLemmatizer()

    words = word_tokenize(text)
    listLemma = []
    for w in words:
        x = lemma.lemmatize(w)
        listLemma.append(x)
    return ' '.join(listLemma)


def stop_words_remove(text):
    stop_words = set(stopwords.words("english"))

    words = word_tokenize(text)

    filtered = [w for w in words if not w in stop_words]

    return ' '.join(filtered)


def remove_freq_words(text, freq_words):
    words = word_tokenize(text)

    filtered = [w for w in words if not w in freq_words]

    return ' '.join(filtered)


def procesare_text(text, tags):
    tags = split_words(tags)

    all_tags = list(itertools.chain.from_iterable(tags))

    top_topics = pd.Series(all_tags)
    top_topics = top_topics.value_counts(ascending=False)[0:200]

    codeless_text = text.apply(lambda x: re.sub(r'<code>.+?<\/code>', '', x))
    new_text = codeless_text.apply(lambda x: BeautifulSoup(x, "html.parser").get_text())

    new_text = new_text.apply(clean_punct, top_topics=top_topics)

    new_text = new_text.apply(lemitize_words)

    new_text = new_text.apply(stop_words_remove)

    freq_words = pd.Series(' '.join(new_text).split()).value_counts()[:30]
    freq_words = list(freq_words.index)

    filtered_text = new_text.apply(remove_freq_words, freq_words=freq_words)

    return filtered_text, top_topics
