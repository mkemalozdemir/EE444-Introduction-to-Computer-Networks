import requests
import json
import random
from election.election_lib import *

# Fetch function of regions
def fetchRegions():
    result = requests.get('http://127.0.0.1:5000/election/regions')
    return json.loads(result.text)

# Fetch function of parties
def fetchParties():
    result = requests.get('http://127.0.0.1:5000/election/parties')
    return json.loads(result.text)

# Function to add a new region - The code 200 means that succesful HTTP request
def putRegion(region_name, number_of_seats):
    url = 'http://127.0.0.1:5000/election/regions'
    data = {'region_name': region_name, 'number_of_seats': number_of_seats}
    response = requests.put(url, json=data)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Error ({response.status_code}): {response.text}")

# Function to delete a region - The code 200 means that succesful HTTP request
def deleteRegion(region_name):
    url = 'http://127.0.0.1:5000/election/regions'
    data = {'region_name': region_name}
    response = requests.delete(url, json=data)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Error ({response.status_code}): {response.text}")

# Function to add a new party - The code 200 means that succesful HTTP request
def putParty(party_name):
    url = 'http://127.0.0.1:5000/election/parties'
    data = {'party_name': party_name}
    response = requests.put(url, json=data)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Error ({response.status_code}): {response.text}")

# Function to delete a party - The code 200 means that succesful HTTP request
def deleteParty(party_name):
    url = 'http://127.0.0.1:5000/election/parties'
    data = {'party_name': party_name}
    response = requests.delete(url, json=data)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Error ({response.status_code}): {response.text}")


if __name__ == "__main__":
    
    # Fetch regions
    regions = fetchRegions()
    print("Regions:", regions)
    print("*********************************************************")
    
    #Add METU and EEE regions with seats 10 and 3
    putRegion("METU",10)
    putRegion("EEE",3)
    print("*********************************************************")

    #Fetch regions
    regions = fetchRegions()
    print("Regions:", regions)
    print("*********************************************************")

    #Try to add METU again - gives the error message
    #Delete the EEE region
    putRegion("METU",10)
    deleteRegion("EEE")
    print("*********************************************************")

    #Fetch regions
    regions = fetchRegions()
    print("Regions:", regions)
    print("*********************************************************")

    # Fetch parties - Have to be empty
    parties = fetchParties()
    print("Parties:", parties)
    print("*********************************************************")

    #Add Party1, Party2, Party3, Party4
    putParty("Party1")
    putParty("Party2")
    putParty("Party3")
    putParty("Party4")
    print("*********************************************************")

    # Fetch parties
    parties = fetchParties()
    print("Parties:", parties)
    print("*********************************************************")

    #Try to add Party4 again - gives error message
    #Delete Party4 
    putParty("Party4")
    deleteParty("Party4")
    print("*********************************************************")

    # Fetch parties
    parties = fetchParties()
    print("Parties:", parties)
    print("*********************************************************")

    #Create lists for regions and seats.
    region_list=[]
    seat_list=[]
    count_regions=len(regions)

    #For loop provides generate random numbers to choose regions randomly
    for i in range(3):
        a=random.randint(0,count_regions-i-1)
        region_list.append(regions[a]["region_name"])
        seat_list.append(regions[a]["seats"])
        regions.pop(a)

    #vote_data is printed to debug with the final seat results
    vote_data = {
    region_list[0]: {'seats': seat_list[0], 'votes': 10000},
    region_list[1]: {'seats': seat_list[1], 'votes': 50000},
    region_list[2]: {'seats': seat_list[2], 'votes': 100000}
    }

    print(vote_data)
    print("*********************************************************")

    council= [i['party_name'] for i in parties]
    
    #Call the simulator for the first selected region
    first_percentage = {council[0]:49,council[1]: 46, council[2]: 5}
    seat_counts=simulate_election(vote_data,council,region_list[0],first_percentage)
    for party, seats in seat_counts.items():
        print(f'{party}: {seats} seats')  

    print("*********************************************************")

    #Call the simulator for the second selected region
    second_percentage = {council[0]:33,council[1]: 34, council[2]: 33}
    seat_counts1=simulate_election(vote_data,council,region_list[1],second_percentage)
    for party, seats in seat_counts1.items():
        print(f'{party}: {seats} seats')  

    print("*********************************************************")

    #Call the simulator for the third selected region
    third_percentage = {council[0]:38,council[1]: 21, council[2]: 41}
    seat_counts2=simulate_election(vote_data,council,region_list[2],third_percentage)
    for party, seats in seat_counts2.items():
        print(f'{party}: {seats} seats')  
