import requests
import json
import pandas as pd
from datetime import datetime

# Start edit parameters
login = ''
password = ''
hrv_csv_file=r""
startdate = datetime(2022, 1, 1)
date = datetime.now() # Getting the current date and time
# End edit 

ContentType = 'application/json'
secretkey = 'F7AAB28F-8B9E-2CD6-FFEC-A4A8A598A000'
applicationid = '9088AF67-1648-1726-FF09-A51862BF1A00'

headers = {
     'Content-Type': ContentType,
     'secret-key': secretkey,
     'application-id': applicationid,     
}

json_data = {
    'login': login,
    'password': password,
}

loginresponse = requests.post('https://api.backendless.com/v1/users/login', headers=headers, json=json_data)
#loginresponse.text

reponsejson = json.loads(loginresponse.text)

#Specific for user
header_usertoken = {
    'user-token': reponsejson["user-token"],
}

#Build new header with user token
headers.update(header_usertoken)

# Create timestamp
# getting the timestamp in milliseconds
ts = str(round(datetime.timestamp(date) * 1000))
#print("Date and time is:", date)
#print("Timestamp is:", ts)
#print("Corresponding date for the integer timestamp is:", date)

# Build Timestamp for given date
#first_date = (datetime(2022, 10, 18))
first_date = startdate
ts_first = str(round(datetime.timestamp(first_date) * 1000))
#print("Corresponding date for the integer timestamp is:", first_date)

print("Collecting HRV data between:", first_date.date(), "and", date.date())
print("Collecting HRV data for:", (date - first_date).days, "days")

hrvdata_json_allpages=[]
count=0
page=(f'https://api.backendless.com/v1/data/DailySummaryNoCoreData?pageSize=100&sortBy=timestamp%20ASC&where=timestamp%20%3E%20{ts_first}%20and%20timestamp%20%3C%20{ts}%20and%20email%20%3D%20%27{login}%27')
hrvdata = requests.get(page, headers=headers)
hrvdata_json = json.loads(hrvdata.text)
hrvdata_json_allpages.append(hrvdata_json)
print("Collect page:", page)

while True:
    count += 1
    if count >= 1000:
        break
    if hrvdata_json.get('nextPage') == None:
        break
    if hrvdata_json.get('nextPage'):
        print("Collect page:", (hrvdata_json.get('nextPage')))
        hrvdata = requests.get((hrvdata_json.get('nextPage')), headers=headers)
        hrvdata_json = json.loads(hrvdata.text)
        hrvdata_json_allpages.append(hrvdata_json)
print(f"Total pages: {len(hrvdata_json_allpages)}")

properties=[]
for i in hrvdata_json_allpages:
    #with open(r"C:\Users\Ben Coremans\Documents\hrv4training12.json", 'a', encoding='utf8') as f:
    #    json.dump(hrvdata_json_allpages[count], f, ensure_ascii=False, indent=4)
    property = {}
    for obj in i.get('data'):
        if obj.get('heartrateTimestamp'):
            timestamp_measurement=(datetime.fromtimestamp(obj.get('heartrateTimestamp')/1000)).isoformat(sep='T',timespec='auto')
        else:
            timestamp_measurement=obj.get('heartrateTimestamp')
        property = {'timestamp_measurement':timestamp_measurement,
                    'HR':round(obj.get('heartrate'),2),
                    'AVNN':round(obj.get('avnn'),2),
                    'SDNN':round(obj.get('sdnn'),2),
                    'rMSSD':round(obj.get('rmssd'),2),
                    'pNN50':round(obj.get('pnn50'),2),
                    'LF':round(obj.get('lf'),4),
                    'HF':round(obj.get('hf'),4),
                    'LFHF':round(obj.get('lfhf'),2),
                    'HRV4T_Recovery_Points':round(obj.get('recoveryPoints'),2)
        }
        properties.append(property)

#write to csv file
df = pd.DataFrame(properties)
df.to_csv(hrv_csv_file, index=False, header=True, sep=';')
