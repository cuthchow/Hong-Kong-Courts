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
def get_links(year_start, year_end)
    for year in range(year_start, year_end):
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
failed_links = []

#Gets HTML of each case in case_links
#Extracts the key information, saves into dictionary for each case

def get_summaries(links):
for link in case_links: 
    try:
        newlink = 'http://www.hklii.org/eng/hk/cases/hkcfi' + link
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        r = requests.get(newlink, headers = headers).text
        soup = BeautifulSoup(r, 'html.parser')

        representation = soup.find_all('representation')[0].text
        paras = len(soup.find_all(class_ = 'para'))
        if paras > 2:
            decision = soup.find_all(class_ = 'para')[-3].parent.text + ' ' + soup.find_all(class_ = 'para')[-2].parent.text + ' ' + soup.find_all(class_ = 'para')[-1].parent.text
        elif paras == 2:
            decision = soup.find_all(class_ = 'para')[-2].parent.text + ' ' + soup.find_all(class_ = 'para')[-1].parent.text
        elif pars == 1:
            decision = soup.find_all(class_ = 'para')[-1].parent.text
        judge = soup.findAll('tr')[-3].text.strip() + soup.findAll('tr')[-2].text.strip()
        judge_title = soup.findAll('tr')[-1].text.strip()
        case = soup.find('title').text

        case_dict = {'representation': representation,
                     'decision': decision,
                     'judge': judge,
                     'judge_title': judge_title,
                     'link': link,
                     'case_name': case}

        print('just did: ' + case)
        case_summaries.append(case_dict)

    except:
        failed_links.append(link)
        print('FAIL')
    
    tot -= 1
    print(str(tot) + ' remaining')


    
    
#Convert to dataframe and export
df = pd.Dataframe(case_summaries)
df.to_csv('cases.csv', index = False)




#Find p_rep and d_rep from Representation
def find_rep(x):
    x = x.lower()
    try:
        first = re.findall('((mr|ms)?\.? .{0,39}),( (instructed|assigned) by (.{0,40}))?,? for the .{0,25}?(respondent|plaintiff|defendant|appellant|petitioner|applicant|HKSAR)?', x)[0]
        return first[0]
    except:
        if 'in person' in x:
            return 'in person'
        else:
            return np.nan

cases['p_rep'] = cases['representation'].apply(find_rep)
    
#Find Name of barrister:
def find_bar(x):
    try:
        return re.findall('(Mr|Ms) (.{0,20}),', x)[0][1]
    except: 
        return 'Unrepresented'
    
cases2['p_bar'] = cases2['p_rep'].apply(find_bar)
cases2['d_bar'] = cases2['d_rep'].apply(find_bar)

Find Name of Law firm

#def find_firm(x):
    try:
        x = x.replace('\n', ' ')
        return re.findall('instructed by (.{0,25}),', x)[0]
    except:
        return np.nan
cases2['d_firm'] = cases2['d_rep'].apply(find_firm)
cases2['p_firm'] = cases2['p_rep'].apply(find_firm)