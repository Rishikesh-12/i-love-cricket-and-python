import requests
from datetime import datetime
from twilio.rest import Client

def get_score(url_get_score,api_key,unique_id,teamname):
        data=""
        if unique_id == -1:
            data="your favourite team " + str(teamname.title()) + " is not playing today"
        else:
            uri_params = {"apikey": api_key, "unique_id":unique_id}
            resp=requests.get(url_get_score,params=uri_params)
            data_json=resp.json()
            #print(data_json)
            try:
                data="Here's the score : "+ "\n" + data_json['stat'] +'\n' + data_json['score']
            except KeyError as e:
                data="Something went wrong.\n No worries we will update you soon\n Or you may contact developer contactrishikeshhere@gmail.com"
        return data


def get_unique_id(url_get_all_matches,api_key,teamname):        
        uri_params = {"apikey": api_key}
        resp = requests.get(url_get_all_matches, params=uri_params)
        resp_dict = resp.json()
        uid_found=0
        for i in resp_dict['matches']:
            if (i['team-1'] == teamname.title() or i['team-2'] == teamname.title()) and i['matchStarted']:
                todays_date = datetime.today().strftime('%Y-%m-%d')
                if todays_date == i['date'].split("T")[0]:
                    uid_found=1
                    unique_id=i['unique_id']
                    break
        if not uid_found:
            unique_id=-1

        url_get_score="http://cricapi.com/api/cricketScore"
        send_data=get_score(url_get_score,api_key,unique_id,teamname)
        return send_data




r = requests.get('https://powerful-garden-07163.herokuapp.com/')
databe = r.json()
arrdata=[]
for eachDictonary in databe:
    for j in eachDictonary:
        arrdata.append(eachDictonary[j])


teamName=[]
whatsappNum=[]



for i in range(0,len(arrdata)-2,3):
    if (bool(arrdata[i]) and bool(arrdata[i+1])):
        teamName.append(arrdata[i])
        whatsappNum.append(arrdata[i+1])





url_get_all_matches = "http://cricapi.com/api/matches"
api_key = "Sm7guOGwvpeljJ5KyBNlQhd6J813"




for index in range(0,len(teamName)):    
    whatsapp_message=get_unique_id(url_get_all_matches,api_key,teamName[index])
    account_sid = "AC286b95e9721739e939d7b38995b308da"
    auth_token = "72f26c8612f299a3e9de6416e8ebf4b9"
    client = Client(account_sid, auth_token)
    message = client.messages.create( body=whatsapp_message, from_='whatsapp:+14155238886', to=f'whatsapp:+91 {int(whatsappNum[index])} ')