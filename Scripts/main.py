import streamlit as st
#needed for taking permission
from google_auth_oauthlib.flow import InstalledAppFlow
#for bulding the services
from googleapiclient.discovery import build
#import pandas
import pandas as pd
#import intensity analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
st.set_page_config(page_title = "Sentiment Analysis System", page_icon = "https://cdn-icons-png.flaticon.com/512/12373/12373911.png")

st.title("Sentiment Analysis System")
choice = st.sidebar.selectbox("My Menu", ("HOME", "ANALYSIS", "RESULTS"))

if(choice == "HOME"):
    st.image("https://miro.medium.com/v2/1*_JW1JaMpK_fVGld8pd1_JQ.gif")
    st.write("1.It is a natural language Processing Application which can analyze the sentiment on the text data.")
    st.write("2.This application predicts the sentiment into 3 categories Positive, Negative and Neutral.")
    st.write("3.This application then visualizes the results based on different factors such as age, gender, language, city.")
elif(choice == "ANALYSIS"):
    sid = st.text_input("Enter your Google Sheet ID")
    r = st.text_input("Enter the Range between first column and last column.")
    c = st.text_input("Enter column name that is to be analyzed.")
    btn = st.button("Analyze")
    if(btn):
        if 'cred' not in st.session_state:
            f = InstalledAppFlow.from_client_secrets_file("key.json", ["https://www.googleapis.com/auth/spreadsheets"])
            st.session_state.cred = f.run_local_server(port = 0)
        mymodel = SentimentIntensityAnalyzer()
        #Building the service
        service = build('sheets', 'v4', credentials=st.session_state.cred).spreadsheets().values()
        k = service.get(spreadsheetId= sid, range=r).execute()
        d = k['values']
        df = pd.DataFrame(data = d[1:], columns = d[0])
        l = []
        for i in range(0, len(df)):
            t = df._get_value(i, c)
            pred = mymodel.polarity_scores(t)
            if(pred['compound'] > 0.5):
                l.append("Positive")
            elif(pred['compound'] < -0.5):
                l.append("Negative")
            else:
                l.append("Neutral")
        df['Sentiment'] = l  
        df.to_csv("results.csv", index=False)  
        st.subheader("The Analysis results are saved by the name results.csv")
elif(choice == "RESULTS"):
    df = pd.read_csv("results.csv")
    choice2 = st.selectbox("Choose Visualization", ("NONE", "Pie Chart", "Histogram", "Scatter Plot"))
    st.dataframe(df)     
    if(choice2 == "Pie Chart"):
        #Pie chart
        prosper = (len(df[df["Sentiment"] == "Positive"])/len(df))*100
        negper = (len(df[df["Sentiment"] == "Negative"])/len(df))*100
        neuper = (len(df[df["Sentiment"] == "Neutral"])/len(df))*100
        pc = px.pie(values=[prosper, negper, neuper], names=['Positive', 'Negative', 'Neutral'])
        st.plotly_chart(pc)
    if(choice2 == "Histogram"):
        #histogram for categorical value
        k = st.selectbox("Choose column", df.columns)
        if(k):
            ht = px.histogram(x=df[k], color=df['Sentiment'])
            st.plotly_chart(ht)
    if(choice2 == "Scatter Plot"):
        k = st.selectbox("Choose column x", df.columns)
        sc = px.scatter(x=df[k], y=df["Sentiment"])  
        st.plotly_chart(sc)
         


           

