import re
import pandas as pd

def preprocess(data):
    # print(data)
    # f=open(data,'r')
    # data=f.read()
    pattern = r"(\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s(?:am|pm))\s-\s([^:]+:\s.*)"
    matches = re.findall(pattern, data)
    messages = [match[1] for match in matches]
    dates = [match[0] for match in matches]
    messages = [match[1] for match in matches]
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['user'] = df['user_message'].str.split(':').str[0].str.strip()
    df['message'] = df['user_message'].str.split(':').str[1].str.strip()
    df["message_time"] = df["message_date"].str.split(", ").str[1]
    df["message_date"] = df["message_date"].str.split(", ").str[0]
    df['message_date'] = pd.to_datetime(df['message_date'], format='mixed')

    df['message_time'] = df['message_time'].str.replace('\u202f', ' ', regex=False)

    df['message_time'] = pd.to_datetime(df['message_time'], format="%I:%M %p", errors='coerce')
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_time'].dt.hour
    df['minute'] = df['message_time'].dt.minute

    df = df.drop(['user_message', 'message_date','message_time'], axis=1)
    df = df[['user', 'message',  'day', 'month', 'year', 'hour', 'minute']]
    return df
