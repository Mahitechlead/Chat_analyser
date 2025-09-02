import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choosse a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # print(data)
    df = preprocessor.preprocess(data)
    st.dataframe(df)
    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user = df['user'].value_counts().to_dict()
    user['Overall'] =df.shape[0]

    user_list.insert(0,'Overall')
    selected_user =  st.sidebar.selectbox("Show analysis wrt" , user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages ,w_count,media, links = helper.fetch_stat(selected_user, user,df)
        print(num_messages)

        col1, col2, col3, col4, col5 = st.columns(5)

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
    # finding the busiest user in the group

    if selected_user == 'Overall':
        x,new_df = helper.most_busy_users(df)
        st.title("Most Busy Users")
        fig, ax = plt.subplots()
        ax.plot(x.index,x.values)
        st.pyplot(fig)

        col1,col2 = st.columns(2)

        with col1:
            ax.bar(x.index,x.values, color = 'red')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    # Wordcloud
    df_wc = helper.create_wordcloud(selected_user, df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    plt.imshow(df_wc)
    st.pyplot(fig)










