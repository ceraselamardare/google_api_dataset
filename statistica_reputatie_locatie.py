import re

import pandas as pd
import matplotlib.pyplot as plt

df_train = pd.read_csv('location_reputation.csv', dtype=str)
df_train = df_train[df_train['location'].notna()]
info = df_train.info()
print(info)

loc_rep = df_train[['location', 'reputation']]


def usa_states(location):
    # state_names = [state.name for state in us.states.STATES_AND_TERRITORIES]
    states = ["US", "USA", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    for state in states:
        if state in location:
            location = 'United States'
            break

    location = re.findall(r'[^,]+$', location)[0]

    return location.strip()


loc_rep['location'] = loc_rep['location'].apply(usa_states)
loc_rep['location'] = loc_rep['location'].apply(lambda s: s.replace('UK', 'United Kingdom'))

# unique_locations = np.unique(location) #506
top_locations = loc_rep['location'].value_counts(ascending=False)[:50]
loc_rep['reputation'] = loc_rep['reputation'].apply(lambda s: int(s))

plt.figure(figsize=(12, 10))
plt.style.use('ggplot')
loc_rep['location'].value_counts()[:50].sort_values().plot(kind='barh')
plt.title('Distribution of users by country')
plt.ylabel('Country')
plt.xlabel('Number of users')
plt.show()

means = {

}

for i in range(top_locations.keys().size):
    country = top_locations.keys()[i]

    mean_rep_country = loc_rep[loc_rep['location'] == country]['reputation'].mean()

    means[country] = mean_rep_country

countries = list(means.keys())
values = list(means.values())

plt.figure(figsize=(12, 10))
plt.style.use('ggplot')
plt.bar(countries, values)
plt.xticks(rotation='vertical')
plt.title('Distribution of reputation by most popular countries')
plt.ylabel('Average reputation')
plt.xlabel('Country')
plt.show()
