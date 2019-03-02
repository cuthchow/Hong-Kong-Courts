import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math

#Saves the unique link for each case
case_links = []

#Gets case lists for each years, scrapes links for each case
for year in range(2014,2020):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(f'http://www.hklii.org/eng/hk/cases/hkcfi/{year}/', headers = headers).text
    soup = BeautifulSoup(r, 'html.parser')

    total = len(soup.findAll('ul')[1].findAll('a'))
    for each in range(total):
        link = soup.findAll('ul')[1].findAll('a')[each]['href']
        link = link[2:]
        case_links.append(link)


#Stores the key information from each case
case_summaries = []

#Gets HTML of each case in case_links
#Extracts the key information, saves into dictionary for each case
for link in case_links:
    try:
        newlink = 'http://www.hklii.org/eng/hk/cases/hkcfi' + link
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        r = requests.get(newlink, headers = headers).text
        soup = BeautifulSoup(r, 'html.parser')

        plaintiff_rep = soup.find_all('representation')[0].find_all('p')[1].text
        defendant_rep = soup.find_all('representation')[0].find_all('p')[2].text
        decision = soup.find_all(class_ = 'para')[-2].parent.text + '\n' + soup.find_all(class_ = 'para')[-1].parent.text
        judge = soup.findAll('tr')[-2].text.strip()
        judge_title = soup.findAll('tr')[-1].text.strip()
        case = soup.find('title').text

        case_dict = {'p_rep': plaintiff_rep,
                     'd_rep': defendant_rep,
                     'decision': decision,
                     'judge': judge,
                     'judge_title': judge_title,
                     'link': link,
                     'case_name': case}

        print('just did' + case)
        case_summaries.append(case_dict)
    except:
        pass


#Convert to dataframe and export
df = pd.Dataframe(case_summaries)
df.to_csv('cases.csv', index = False)
