import matplotlib.pyplot as plt
from urlextract import URLExtract
from wordcloud import WordCloud

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
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    wc = WordCloud(width = 500,height = 500,min_font_size=10,background_color='White')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


