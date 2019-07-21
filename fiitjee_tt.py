import requests
import urllib.request
import time
import json
import bs4

def extract_time(time):
    time_split = time.split('-\n')
    return time_split

subject_color = {'MNP' : '9','MMSH' : '1','PRGS' : '3','CNSH' : '11','BSSN' : '10',"SDJ" : '5'}

schedule = []
url = 'http://ftje.in/URL_TT.aspx?E=18552984'
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text, "html.parser")

# for i in range(36,len(soup.findAll('a'))+1): #'a' tags are for links
soup = soup.findAll('div', 'label1')

for header in soup:
    table = header.next_sibling.contents[1].contents[2:]
    day = {}
    day['date'] = header.contents[1].string.split(", ")
    day['date'] = day['date'][1] + " " + day['date'][2]
    day['classes'] = []
    for row in table:
        if row == "\n":
            continue
        clss = {}
        time = row.contents[2].string
        clss['start'] = extract_time(time)[0]
        clss['end'] = extract_time(time)[1]
        clss['name'] = row.contents[3].string
        day['classes'].append(clss)
    schedule.append(day)

with open("tt_data_file.json", "w") as write_file:
    json.dump(schedule, write_file)