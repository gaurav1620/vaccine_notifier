#!/bin/env python
#Header
from pyfiglet import Figlet
f = Figlet(font='slant')
print('Script Created by : ')
print(f.renderText('gaurav'))

sound = int(input("Do you want sound : 1 for yes , 2 for no : "))
sound = 0 if sound == 2 else 1
print('****************************************************')
if sound :
    print("Sound is set to on ! \nOne beep each second will be played regularly \n3 beeps per second will be played as soon as vaccine for your age group is available")

else :
    print("As no sound will be played, you need to manually keep observing the table ;)")

input("press Enter to continue")
#Imports
import requests
import time
from prettytable import PrettyTable
from playsound import playsound

# Code to clear screen 
from os import system, name
from time import sleep
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


# Script starts here 

# Do not change headers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
res = 1

#Fetch a list of states
try :
    res = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states', headers=headers)
except :
    # If request fails, stop executing the script
    print("Check your internet connection and try again !")
    exit()

# Load the state data
states =res.json()['states']

# Show a list of states along with index to user
print('ID : Name of state')
for i in states:
    print(str(i['state_id']) + ' : '+ str(i['state_name']))

# ask the user to enter the index of state he wants
state_id = input('Enter the serial number of your state : ')

#Fetch a list of districts in that state
try :
    res = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/' + state_id
                       , headers=headers)
except :
    # If request fails, stop executing the script
    print("Check your internet connection and try again !")
    exit()

# Load the districts data
districts = res.json()['districts']

# Show a list of districts to the users
for i in range(len(districts)):
    print(str(i+1) + ' : ' +districts[i]['district_name'])

# Ask the user to enter the district he is in
district_id = districts[int(input('Enter the serial number of your district : ')) - 1]['district_id']

print('****************************************************')
month = input('Enter the current month in number, eg 5 for May : ')

print('****************************************************')
date = input('Enter the date of the month that you want to book : ')

# append neccessary zeros before single digits
if len(str(date)) == 1:
    date = '0' + date
if len(str(month)) == 1:
    month = '0' + month

# Input users age group
print('What age group you belong to : ')
print('1. 18-44')
print('2. 45+')
age_group = input('Enter your choice :')
age_group = int(age_group)
age_group = 2 if age_group == 1 else 1

show_all_info = int(input('Do you want to display info for just your age group(press 1) or all age groups(press 2) : ')) -1

def yes_or_no(inp):
    if inp:
        return "YESSSS"
    else :
        return "NO"

aa = 1
while 1:
    uri = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id='+ str(district_id) + '&date='+ str(date) + '-'+ str(month) +'-2021'
    print(uri)
    res = requests.get(uri, headers = headers)
    if res.status_code != 200:
        #print(uri)
        print("Failed to fetch details !")
        print("Please check your Internet connectivity. If the script does not work for you email me the screenshot on gauravak007@gmail.com")
        continue

    centers = res.json()['centers']

    table = PrettyTable()
    table.field_names = ['Center name', 'Number of doses available','18+ dose available ? ', '45+ dose available ?','min age limit']

    play_sound = 0    

    for i in centers:

        min_age_limit = i['sessions'][0]['min_age_limit']
        available_capacity = i['sessions'][0]['available_capacity']

        vaccine_above_18 = ( available_capacity > 0 and min_age_limit == 18 )
        vaccine_above_45 = ( available_capacity > 0 and min_age_limit == 45 ) 
        if play_sound == 0 and ((vaccine_above_18  and (age_group == 2)) or (vaccine_above_45 and (age_group == 1))):
            play_sound = 1
        if(i['sessions'][0]['min_age_limit'] == 18 and age_group == 2) or show_all_info:
            table.add_row([i['name'], available_capacity, yes_or_no(vaccine_above_18), yes_or_no(vaccine_above_45), min_age_limit])
        if(i['sessions'][0]['min_age_limit'] == 45 and age_group == 1) or show_all_info:
            table.add_row([i['name'], available_capacity, yes_or_no(vaccine_above_18), yes_or_no(vaccine_above_45), min_age_limit])


    if (sound == 1) and (play_sound == 1):
        playsound('beep.mp3')
        playsound('beep.mp3')
    if sound:
        playsound('beep.mp3')
    time.sleep(0.5)
    clear()
    print(table)
    #print("Vaccination drive for 18-45 has been stopped. So you may not see any vaccination centres in the table if you selected that age group.")
    #print(str(i['name']) + ' has '+ str(i['sessions'][0]['available_capacity']) + ' with minimum age limit of '+ str(i['sessions'][0]['min_age_limit']))

