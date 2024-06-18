import requests
import json

#Main function 
if __name__ == "__main__":

    res = requests.get('http://127.0.0.1:5000/election/regions')
    response = json.loads(res.text)
    print(response)

