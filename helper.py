import matplotlib.pyplot as plt
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


extract = URLExtract()

def fetch_stat(selected_user,user_list,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    print(user_list)
    # return user_list[selected_user]
    w_count = 0
    media = 0
    links = 0
    for x  in df['message']:
    # fetching words
        w_count+=len(x.split())
    # fetching shared media
        if x=='<Media omitted>':
            media+=1

# fetch links shared
    for message in df['message']:
        links+= len(extract.find_urls(message))


    return user_list[selected_user],w_count,media, links


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})

    return x,df

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != '<Media omitted>\n']
    temp = temp[temp['message'] != '<media omitted>\n']

    wc = WordCloud(width = 500,height = 500,min_font_size=10,background_color='White')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


    temp = df[df['user'] != '<Media omitted>\n']
    temp = temp[temp['message']!='<Media omitted>\n']


    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = {}
    for message in df['message']:
        # emojis.extend([e for e in message if emoji.is_emoji(e)])
        for e in message:
            if emoji.is_emoji(e):
                emojis[e] = emojis.get(e,0)+1
    print(emojis)
    emojidf = pd.DataFrame(emojis.items(), columns=['emoji', 'count'])
    return emojidf.sort_values(by='count', ascending=False)





