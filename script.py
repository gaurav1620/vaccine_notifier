#Header
from pyfiglet import Figlet
f = Figlet(font='slant')
print('Script Created by : ')
print(f.renderText('gaurav'))

sound = int(input("Do you want sound : 1 for yes , 2 for no : "))
sound = 0 if sound == 2 else 1
if sound :
    print("Okay one beep will be played each time table is updated, and 2 beeps will be played if vaccine is available for your age group.")

#Imports
import requests
import time
from prettytable import PrettyTable
from playsound import playsound
time.sleep(2)

# Script starts here 

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
res = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states', headers=headers)
states =res.json()['states']
print('ID : Name of state')
for i in states:
    print(str(i['state_id']) + ' : '+ str(i['state_name']))

state_id = input('Enter the serial number of your state : ')

res = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/' + state_id
                   , headers=headers)
districts = res.json()['districts']

for i in range(len(districts)):
    print(str(i+1) + ' : ' +districts[i]['district_name'])

district_id = districts[int(input('Enter the serial number of your district : ')) - 1]['district_id']

print('*****************************************')
month = input('Enter the current month in number, eg 5 for May : ')

print('*****************************************')
date = input('Enter the date of the month that you want to book : ')

if len(str(date)) == 1:
    month = '0' + date
if len(str(month)) == 1:
    month = '0' + month

age_group = input('Enter 1 if your age is 45+ or 2 if your age is 18+ :')
age_group = int(age_group )

while 1:
    uri = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id='+ str(district_id) + '&date='+ str(date) + '-'+ str(month) +'-2021'
    #print(uri)
    res = requests.get(uri, headers = headers)
    if res.status_code != 200:
        print(uri)
        print("pleasse login from browser and run script again")
        break;
    centers = res.json()['centers']

    table = PrettyTable()
    table.field_names = ['Center name', 'Number of doses available','18+ dose available ? ', '45+ dose available ?','min age limit']

    play_sound = 0    

    for i in centers:
        vaccine_above_18 =  "YESSSS" if (i['sessions'][0]['available_capacity'] > 0 and i['sessions'][0]['min_age_limit'] == 18 ) else "No"
        vaccine_above_45 =  "YESSSS" if (i['sessions'][0]['available_capacity'] > 0 and i['sessions'][0]['min_age_limit'] == 45 ) else "No"
        if play_sound == 0 and (((vaccine_above_18 == "YESSSS") and (age_group == 2)) or ((vaccine_above_45 == "YESSSS") and (age_group == 1))):
            play_sound = 1
        table.add_row([i['name'], i['sessions'][0]['available_capacity'],vaccine_above_18 ,vaccine_above_45, i['sessions'][0]['min_age_limit'] ])

    if (sound == 1) and (play_sound == 1):
        playsound('beep.mp3')
        playsound('beep.mp3')
    if sound:
        playsound('beep.mp3')
    time.sleep(0.5)

    print(table)
    #print(str(i['name']) + ' has '+ str(i['sessions'][0]['available_capacity']) + ' with minimum age limit of '+ str(i['sessions'][0]['min_age_limit']))

