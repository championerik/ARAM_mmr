# -- coding: ISO-8859-1 --
import requests, json, os, urllib3
from bs4 import BeautifulSoup


cmd = 'mode 74,71'
os.system(cmd)

### No SSL Waring
urllib3.disable_warnings()

### Colors
class style:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class mmr_url:
    USERNAME = ""
    euw = "https://euw.whatismymmr.com/api/v1/summoner?name={}"
    na = "https://na.whatismymmr.com/api/v1/summoner?name={}"
    eune = "https://eune.whatismymmr.com/api/v1/summoner?name={}"

class top500_url:
    euw = f"https://aram.moe/euw"
    na = f"https://aram.moe"
    eune = f"https://aram.moe/eune"



def jsonprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(json.loads(response), indent=4, sort_keys=True)
    print(text)

def getaramrank(USERNAME, CHAMPION, TEAM, curruser, mmrregion, top500region):
    rank = requests.get((mmrregion).format(USERNAME)).text
    response = json.loads(rank)
    youmarker = ""
    best500 = ""
    if TEAM == "CHAOS":
        colorTEAM = style.RED + "Red" + style.RESET
    else:
        colorTEAM = style.BLUE + "Blue" + style.RESET
    if USERNAME == curruser:
        youmarker = style.GREEN + "You ->" + style.RESET
    if USERNAME in gettop500(top500region):
        best500 = style.RED + "--Top500--" + style.RESET
        pass
    print(f"\n{youmarker}\t({CHAMPION}) {USERNAME} {best500}\n\tTeam: {colorTEAM}")
    if "ARAM" in response:
        print("\t"+str(response["ARAM"]["avg"]))
        print("\t"+str(response["ARAM"]["closestRank"])+"\n")
    else:
        print("\tUnranked\n")

def getplayerlist(curruser, mmrregion, top500region):
    print(style.GREEN + "\nSuccess - Getting Playerlist\n" + style.RESET)
    data = requests.get(f"https://127.0.0.1:2999/liveclientdata/playerlist", verify=False)
    response = json.loads(data.text)
    for summoner in response:
        getaramrank(summoner["summonerName"], summoner["championName"], summoner["team"], curruser, mmrregion, top500region)

def getcurrentuser():
    data = requests.get(f"https://127.0.0.1:2999/liveclientdata/activeplayername", verify=False)
    curruser = json.loads(data.text)
    return curruser

def gettop500(top500region):
    page = requests.get(top500region)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(class_="cards-container")
    job_elements = results.find_all("div", class_="player-container")
    top500 = []
    for job_element in job_elements:
        name_element = job_element.find("span", class_="name")
        entry =  name_element.text.strip()
        top500.append(entry)
    return top500

class program:

    print("Copyright hold by © 2022 Erik Börner\nContact: championerik#4209\n")
    print(style.CYAN + "--------------------------------" + style.BLUE + "MMR Reader" + style.CYAN +"--------------------------------" + style.RESET)     
    inputregion = input("What region are you in? (euw, na, eune): ")
    print(style.YELLOW + "\nTrying to connect to client 127.0.0.1" + style.RESET)
    end = False
    while end != True:
        if inputregion == "euw":
            mmrregion = mmr_url.euw
            top500region = top500_url.euw
            break
        elif inputregion == "na":
            mmrregion = mmr_url.na
            top500region = top500_url.na
            break
        elif inputregion == "eune":
            mmrregion = mmr_url.eune
            top500region = top500_url.eune
            break
        else:
            print("Please input a valid Region.")
            end = True
            quit()
    try:
        
        getplayerlist(getcurrentuser(), mmrregion, top500region)
        input("Press Any Key to Close")
    except:
    
        print(style.RED + "\nNo Game Running...\n" + style.RESET)
        choice = input("\tWant to see the messy error? Enter \"y\": ")
        if choice == "y":
            raise
        else:
            print("Closing Program.")
            input("Press Any Key to Close")
            quit()

program