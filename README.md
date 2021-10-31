# Google_api_dataset

The project consisted of 2 parts: a part where the top 3 topics had to be extracted from a Stackoverflow post and a data analysis part.

### 1. Top topics
The .cvs file with the dataset consisted of 20 columns and 9063 rows, columns include: id, title, body, accepted_answer_id, answer_count, comment_count, tags and others. 
To solve this problem, I decided to start by processing the text in the body, to do this I also had to take into account that there are topics like C++, C# that should not be removed. I extracted the column of tags and noticed that they were separated by the "|" character, so using the split function, I processed the tags and added them to a list from which I later kept only the 200 most popular entries using the 
value_counts() function. Using a regular expression, I removed all the code inside the Stackoverflow posts, this being useless information that wouldn't help us find the main topics. After removing the code, I used the BeautifulSoup function to remove the html formatting, as the text was not properly formatted for processing. 

I have defined a clean_punct function to remove punctuation marks from a defined list using a regular expression but not to remove previously saved tags. In this function, the .lower function is applied to all the posts to convert uppercase to lowercase, after this step, each word is extracted using the word_tokenize function and tested if it is part of the tag list. 
After this step, the posts are lemmatized using the lemitize_words function, this brings each word to its base form and makes sure that this base form exists in the dictionary. The next step is to remove stop_words from the classic stopwords.words("english") list, followed by removing the most frequent words from the processed text. The list of most frequent words includes: nt, code, like, using, file, use, get, want, would etc, these words are not useful information for our problem.

After processing the text, I used TfidfVectorizer which received as a parameter the list of posts by on Stackoverflow, it will know how to calculate the occurrences matrix, the IDF matrix and finally the return the Tf-Idf score matrix. The parameters chosen for the TfidfVectorizer are:
- analyzer = 'word' - parsing the text by words
- min_df=0.0, ignores terms that have a frequency strictly less than the given threshold.
- max_df = 1.0, ignores terms that have a frequency strictly higher than the given threshold.
- max_features=1000, builds a vocabulary that considers only the first max_features ordered by the frequency of the terms in the corpus, I consider 1000 to be a sufficient number of features for this problem.

I made a function that returns the top 3 topics of a post, as well as the original post without html formatting and without code. For the top 3 topics, I consider these to be the words with the highest tf_idf_scores. The function also takes as a parameter a number of posts to be returned, these posts are chosen randomly from the database.

### 2. Analysis part 
The .csv file contains 13 columns with 5035 entries, among these columns are 
id, display_name, about_me, location, reputation, up_votes, down_votes, etc. 
For my analysis, I decided to interpret the reputation of Stackoverflow users according to country of origin. To do this, I extracted from the .csv file the location column, this contained names of cities, regions, states and countries and required some processing to understand really understand the data.
To begin with, I processed the data in which state acronyms from the United States or different spellings for this country (US, USA). After this using an expression regular expression, we could also process the rest of the countries by extracting the last word, after the last comma, which was in most cases a country name. This step was followed by replacing all the acronyms "UK" with the whole form United Kingdom to have all entries under the same name. Using value_counts function, we were able to find out which were the most popular countries with the most users active on Stackoverflow.
Next, I defined a dictionary where I saved the names of countries and assigned an average reputation score to each. This score represents the average reputation of all users in that country, the values for reputations find extracted from the dataset in the "reputation" column. 

###Datasets: https://www.kaggle.com/stackoverflow/stackoverflow
