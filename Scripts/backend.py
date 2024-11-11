#needed for taking permission
from google_auth_oauthlib.flow import InstalledAppFlow
#for bulding the services
from googleapiclient.discovery import build
#import pandas
import pandas as pd
#import intensity analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
mymodel = SentimentIntensityAnalyzer()
#Taking permission from the user
f = InstalledAppFlow.from_client_secrets_file("key.json", ["https://www.googleapis.com/auth/spreadsheets"])
cred = f.run_local_server(port = 0)

#Building the service
service = build('sheets', 'v4', credentials=cred).spreadsheets().values()
k = service.get(spreadsheetId= "12BSVFaEXEIJf1tHrM9ECE54a66TCu1BvXOd6ddfGCpE", range="B:F").execute()
d = k['values']
df = pd.DataFrame(data = d[1:], columns = d[0])
l = []
for i in range(len(df)):
    t = df._get_value(i, "Opinion")
    pred = mymodel.polarity_scores(t)
    if(pred['compound'] > 0.5):
        d[i].append("Positive")
    elif(pred['compound'] < -0.5):
        d[i+1].append("Negative")
    else:
        d[i+1].append("Neutral")

h = {'values': d}
service.update(spreadsheetId="12BSVFaEXEIJf1tHrM9ECE54a66TCu1BvXOd6ddfGCpE", range="G1", valueInputOption = 'USER_ENTERED', body={'values': [["Sentiment"]]}).execute()
