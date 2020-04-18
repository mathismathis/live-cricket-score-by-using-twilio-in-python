# live-cricket-score-by-using-twilio-in-python
import requests
from datetime import datetime

class ScoreGet:
    def __init__(self):
        self.url_get_all_matches = "http://cricapi.com/api/matches"
        self.url_get_score="http://cricapi.com/api/cricketScore"
        self.api_key = "6oJAancpaAfM1bhyRnHZN9JFFTX2"
        self.unique_id = ""  # unique to every match

    def get_unique_id(self):
        permiter= {"apikey": self.api_key}
        resp = requests.get(self.url_get_all_matches, params=permiter)
        resp_dict = resp.json()
        f=0
        for i in resp_dict['matches']:
            if (i['team-1'] == "Nepal Army Club" or i['team-2'] == "Nepal Police Club") and i['matchStarted']:
                todays_date = datetime.today().strftime('%Y-%m-%d')
               
                if todays_date == i['date'].split("T")[0]:
                    f=1
                    self.unique_id=i['unique_id']
                    print(self.unique_id)
                    break
        if not f:
            self.unique_id=-1

        data=self.get_score(self.unique_id)
        return data
    def get_score(self,unique_id):
        data="" 
        if unique_id == -1:
            data="No live matches today"
        else:
            permiter = {"apikey": self.api_key, "unique_id": self.unique_id}
            resp=requests.get(self.url_get_score,params=permiter)
            data=resp.json()
            data="Here's the score : "+'\n' + data['score']
        return data



if __name__ == "__main__":
  
    match=ScoreGet()
    send_message=match.get_unique_id()
    print(send_message)
    from twilio.rest import Client
    account_sid = 'ACc86666f6bbf72b3ae6bfc6df'
    auth_token = '1542b4b2b19df88f8cc8b5ebd'
    client = Client(account_sid, auth_token)
    message = client.messages.create( body=send_message, from_='+19173326', to='+9189006')
