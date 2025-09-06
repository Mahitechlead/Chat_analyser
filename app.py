import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # print(data)
    df = preprocessor.preprocess(data)

    print(df)
    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user = df['user'].value_counts().to_dict()
    user['Overall'] =df.shape[0]

    user_list.insert(0,'Overall')
    selected_user =  st.sidebar.selectbox("Show analysis wrt" , user_list)

    if st.sidebar.button("Show Analysis"):
        #stats area
        num_messages ,w_count,media, links = helper.fetch_stat(selected_user, user,df)
        print(num_messages)
        st.title("Top Statistics")
        col1, col2, col3, col4, col5 = st.columns(5)
        st.title("Total Messages")



        with col1:
            st.header("Total Messages")
            st.title(num_messages )
        with col2:
            st.header("Total Words")
            st.title(w_count)
        with col3:
            st.header("Media Shared")
            st.title(media)
        with col4:
            st.header("Links Shared")
            st.title(links)

    # MonthlyTimeline
    st.title("Monthly Timeline")

    timeline = helper.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['time'],timeline['message'],color= 'green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


    #Daily timeline
    st.title("Daily Timeline")
    daily_timeline= helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
    plt.xticks(rotation= 'vertical')
    st.pyplot(fig)


    #activity map
    st.title('Activity Map')
    col1,col2 = st.columns(2)

    with col1:
        st.header("Most busy day")
        busy_day = helper.week_activity_map(selected_user, df)
        fig,ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values, color='pink')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    with col2:
        st.header("Most busy month")
        busy_month = helper.month_activity_map(selected_user, df)
        fig,ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values, color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    st.title("Weekly activity map")
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)

    # finding the busiest user in the group

    if selected_user == 'Overall':
        x,new_df = helper.most_busy_users(df)
        st.title("Most Busy Users")
        fig, ax = plt.subplots()
        ax.plot(x.index,x.values)
        st.pyplot(fig)

        col1,col2 = st.columns(2)

        with col1:
            ax.bar(x.index,x.values, color = 'orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    # Wordcloud
    st.title("Word_cloud")
    df_wc = helper.create_wordcloud(selected_user, df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    plt.imshow(df_wc)
    st.pyplot(fig)

    # most_common words
    most_common_df = helper.most_common_words(selected_user, df)

    st.dataframe(most_common_df)

    fig,ax = plt.subplots()

    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation = 'vertical')
    st.title('Most Common Words')
    st.pyplot(fig)

    # emoji analysis

    emoji_df = helper.emoji_helper(selected_user,df)

    st.title('Emoji Analysis')

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)

    with col2:
        fig,ax = plt.subplots()
        ax.pie(emoji_df["count"].head(),labels = emoji_df['emoji'].head(),autopct ="%0.2f")
        st.pyplot(fig)











