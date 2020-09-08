#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 14:38:59 2020

@author: PRIYANKA
"""

import requests
import re
import json
from collections.abc import Mapping
import csv
from datetime import datetime
import pandas as pd


def GetWDQcode(Qcode_pageTitle,rev_id):
    '''
    Given a Qcode and a revision id, this function returns all the Qcodes of the entities listed 
    in wikidata for that revision
    '''
    QcodeWD_list=list()
    claims=dict()
    url="https://www.wikidata.org/wiki/Special:EntityData/"+Qcode_pageTitle+".json?revision="+rev_id
    r = requests.get(url)
    json_data=r.json()
    claims=json_data['entities'][Qcode_pageTitle]['claims']
    for k,v in claims.items():
        v_dict=v[0]
        for u,w in v_dict.items():
            if 'mainsnak' in u:
                for s,t in w.items():
                    if 'datavalue' in s:
                        #print("datavalue=",t)
                        for p,q in t.items():
                            if 'value' in p:
                                #print("value=",q)
                                if isinstance(q, Mapping):
                                    for m,n in q.items():
                                              
                                        if 'id' == m:
                                            Qcode=n
                                            #print("Qcode=",Qcode)
                                            QcodeWD_list.append(Qcode)
                
                
            if 'references' in u:
                w_dict=w[0]
                for x,y in w_dict.items():
                    
                    if 'snaks' in x:
                        if isinstance(y, Mapping):
                            for a,b in y.items():
                                b_dict=b[0]
                                for c,d in b_dict.items():
                                   if 'datavalue' in c:
                                        #print("datavalue=",t)
                                        for p,q in d.items():
                                            if 'value' in p:
                                                #print("value=",q)
                                                if isinstance(q, Mapping):
                                                    for m,n in q.items():
                                                                                    
                                                        if 'id' == m:
                                                            Qcode=n
                                                            #print("Qcode=",Qcode)
                                                            QcodeWD_list.append(Qcode) 
                            
    return QcodeWD_list

def GetWPtext(pageTitle):
    '''
    This function retrieves the text of wikipedia of the given entity from the cource code of the 
    wikipedia article. From this text one can look for other entities
    '''
    
    #old           url="https://en.wikipedia.org/w/api.php?action=parse&page="+pageTitle+"&prop=wikitext&formatversion=2&format=json"
    #stackoverflow https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Stack%20Overflow&rvlimit=1&rvprop=content&rvdir=newer&rvstart=2016-12-20T00:00:00Z&format=json
    url = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=" + pageTitle + "&rvlimit=1&rvprop=content&rvdir=older&rvstart=2011-12-20T00:00:00Z&format=json"
    r = requests.get(url)
    json_data=r.json()
    #text=json_data['parse']['wikitext']
    try:
        for key in json_data['query']['pages']:
            text = json_data['query']['pages'][key]['revisions'][0]['*']
        return text
    except:
        return ""
    
def GetEntity(pageTitle):
    '''
    This function retrieves the list of entities mentioned/cited in the wikipedia text of the given
    "pageTitle"
    '''
    test_string=GetWPtext(pageTitle)
    #test_string="{{short description|German footballer}}\n{{Use dmy dates|date=December 2019}}\n{{Infobox football biography\n| name = Akaki Gogia\n| image = Akaki Gogia 2013 1.jpg\n| caption = Gogia while with [[FC St. Pauli]] in 2013.\n| fullname = Akaki Gogia<ref>{{Cite web |url=http://www.efl.com/documents/professional-retained-report-2015-16549-3151378.pdf |title=EFL: Retained list: 2015/16 |publisher=English Football League |page=9 |url-status=dead |archive-url=https://web.archive.org/web/20160626205750/http://www.efl.com/documents/professional-retained-report-2015-16549-3151378.pdf |archive-date=26 June 2016 |access-date=26 June 2016}}</ref>\n| birth_date = {{birth date and age|1992|1|18|df=y}}\n| birth_place = [[Rustavi]], Georgia\n| height = 1.78m<ref name=\"Soccerway\" />\n| position = [[Midfielder]]\n| currentclub = [[Union Berlin]]\n| clubnumber = 7\n| youthyears1 = 2001\n| youthclubs1 = FSV 67 Halle\n| youthyears2 = 2001–2004\n| youthclubs2 = [[Hannover 96]]\n| youthyears3 = 2004–2011\n| youthclubs3 = [[VfL Wolfsburg]]\n| years1 = 2009–2011\n| clubs1 = [[VfL Wolfsburg|VfL Wolfsburg II]]\n| caps1 = 9\n| goals1 = 0\n| years2 = 2011–2013\n| clubs2 = [[VfL Wolfsburg]]\n| caps2 = 0\n| goals2 = 0\n| years3 = 2011–2012\n| clubs3 = → [[FC Augsburg]] (loan)\n| caps3 = 12\n| goals3 = 0\n| years4 = 2012–2013\n| clubs4 = → [[FC St. Pauli]] (loan)\n| caps4 = 23\n| goals4 = 1\n| years5 = 2013\n| clubs5 = → [[FC St. Pauli#Reserve team|FC St. Pauli II]] (loan)\n| caps5 = 1\n| goals5 = 0\n| years6 = 2013–2015\n| clubs6 = [[Hallescher FC]]\n| caps6 = 71\n| goals6 = 19\n| years7 = 2015–2017\n| clubs7 = [[Brentford F.C.|Brentford]]\n| caps7 = 13\n| goals7 = 0\n| years8 = 2016–2017\n| clubs8 = → [[Dynamo Dresden]] (loan)\n| caps8 = 22\n| goals8 = 10\n| years9 = 2017–\n| clubs9 = [[1. FC Union Berlin|Union Berlin]]\n| caps9 = 53\n| goals9 = 8\n| nationalyears1 = 2010\n| nationalteam1 = [[Germany national under-18 football team|Germany U18]]\n| nationalcaps1 = 4\n| nationalgoals1 = 0\n| nationalyears2 = 2010–2011\n| nationalteam2 = [[Germany national under-19 football team|Germany U19]]\n| nationalcaps2 = 3\n| nationalgoals2 = 1\n| club-update = 19:12, 22 December 2019 (UTC)\n}}\n'''Akaki Gogia''' ({{lang-ka|აკაკი გოგია}}; born 18 January 1992) is a German professional [[Association football|footballer]] of Georgian descent who plays as a [[Midfielder (association football)|midfielder]] for [[1. FC Union Berlin|Union Berlin]]. He began his career in [[Football in Germany|Germany]] with [[VfL Wolfsburg]], before signing for [[Hallescher FC]] in 2013 and moving to [[Football in England|England]] to join [[Brentford F.C.|Brentford]] in 2015."
    #test_string = "{{short description|German footballer}}\n{{Use dmy dates|date=December 2019}}\n{{Infobox football biography\n| name = Akaki Gogia\n| image = Akaki Gogia 2013 1.jpg\n| caption = Gogia while with [[FC St. Pauli]] in 2013.\n| fullname = Akaki Gogia<ref>{{Cite web |url=http://www.efl.com/documents/professional-retained-report-2015-16549-3151378.pdf |title=EFL: Retained list: 2015/16 |publisher=English Football League |page=9 |url-status=dead |archive-url=https://web.archive.org/web/20160626205750/http://www.efl.com/documents/professional-retained-report-2015-16549-3151378.pdf |archive-date=26 June 2016 |access-date=26 June 2016}}</ref>\n| birth_date = {{birth date and age|1992|1|18|df=y}}\n| birth_place = [[Rustavi]], Georgia\n| height = 1.78m<ref name=\"Soccerway\" />\n| position = [[Midfielder]]"
    #test_string=" Bundesliga club [[1. FC Union Berlin|Union Berlin]]"
    pattern = '\[\[(.*?)\]\]'
    result = re.findall(pattern, test_string)
    new_list=[]
    for item in result:
        if '|' in item:
            x=item.rsplit('|')
            new_list.extend(x)
        else:
            new_list.append(item)
    return list(set(new_list))
    
def WPtoQcode_list(result):
    '''
    This function generates the list of all Qcodes (corresponding to the entities extracted in 
    GetEntity) that have been linked/cited in wikipedia text
    '''
    Qcode_list=[]
    for item in result:
        request_dict={}
        step1_list=[]
        url="https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&ppprop=wikibase_item&redirects=1&titles="+item+"&format=json"
        r = requests.get(url)
        if r.status_code == 200:
            if r!=None or r!='':
                try:
                    rd=r.json()
                except:
                    continue
        else:
            continue
        query = rd.get('query') 
        if query:
            pages=query.get('pages')
            if pages:
                request_dict=pages
                for k,v in request_dict.items():
                    c=0
                    for u,w in v.items():
                        if 'pageprops' in u:
                            Qcode=v[u]['wikibase_item']
                            Qcode_list.append(Qcode)
                            c=1
                            break
                    if c==1:
                        break
    return Qcode_list
   
def GetQcodeofEntity(item):
    '''
    This function generates the Qcode of a single entity sent to it as parameter
    '''
    request_dict={}
    step1_list=[]
    url="https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&ppprop=wikibase_item&redirects=1&titles="+item+"&format=json"
    r = requests.get(url)
    if r.status_code == 200:
        if r!=None or r!='':
            try:
                request_dict=r.json()
            except:
                print("No such entity in KB")
    step1_list.append(request_dict['query']['pages'])
    for k,v in step1_list[0].items():
        c=0
        for u,w in v.items():
            if 'pageprops' in u:
                Qcode=v[u]['wikibase_item']
                c=1
                break
        if c==1:
            break
    return Qcode 


def GetRevisions(Qcode_pageTitle):
    '''
    This function retrieves the whole list of revisions
    '''
    url = "https://www.wikidata.org/w/api.php?action=query&format=xml&prop=revisions&rvlimit=500&titles=" + Qcode_pageTitle
# Below for Wikipedia. The title field should be an article name, like "Akaki_Gogia" or "Germany"
    #url = "https://en.wikipedia.org/w/api.php?action=query&format=xml&prop=revisions&rvlimit=500&titles=" + pageTitle
    revisions = []                                        #list of all accumulated revisions
    next = ''                                             #information for the next request
    while True:
        response = requests.get(url + next)     #web request
        revisions += re.findall('<rev [^>]*>', str(response.text))  #adds all revisions from the current request to the list
        cont = re.search('<continue rvcontinue="([^"]+)"', str(response.text))
        if not cont:                                      #break the loop if 'continue' element missing
            break
        next = "&rvcontinue=" + cont.group(1)             #gets the revision Id from which to start the next request
    return revisions;

def GetRevisionID(Qcode_pageTitle):
    '''
    This function retrieves the revisionID and date from the list generated by GetRevisions(Qcode_pageTitle)
    '''
    ID_list=[]
    date_list=[]
    revisions = GetRevisions(Qcode_pageTitle)
    term=  Qcode_pageTitle  
    i = 0
    """
    To take year from the revisions data un-comment this
    """
    """
    r_latest=revisions[0]
    r_earliest=revisions[-1]
    date_latest=re.search('timestamp=\"(.*?)T', r_latest).group(1)
    year_latest=re.search('....',date_latest).group(0)
    
    date_earliest=re.search('timestamp=\"(.*?)T', r_earliest).group(1)
    year_earliest=re.search('....',date_earliest).group(0)
    
    """
    for x in range(0,len(revisions)):
        r=revisions[x]
        i = i+1
        found = re.search('\"(\d+)\"', r).group(1)
        date=re.search('timestamp=\"(.*?)T', r).group(1)
        year=re.search('....',date).group(0)
        
        ID_list.append(found)
        date_list.append(date)
    return ID_list,date_list

def nearest(items, pivot):
    return min(range(len(items)), key=lambda i: abs(items[i]-pivot))

def sampledRevision(ID_list,date_list,pivot_list):
    for i in range(len(date_list)):
        d=datetime.strptime(date_list[i],'%Y-%m-%d')
        date_list[i]=d
    sampled_Revlist=[]
    sampled_dateIndex=[]
    for i in range(len(pivot_list)):
        pivot=pivot_list[i]
        date_index=nearest(date_list,pivot)
        sampled_dateIndex.append(date_index)
    for i in sampled_dateIndex:
        
        sampled_Revlist.append(ID_list[i])
    return sampled_Revlist


def getDatePivotList():
    year_latest=2020
    year_earliest=2012
    pivot_list=[]
    period=(int(year_latest)-int(year_earliest)+1)
    for i in range(0,period):
        pivot_list.append(datetime.strptime((str(int(year_latest)-i)+'-7-1'),'%Y-%m-%d'))
        pivot_list.append(datetime.strptime((str(int(year_latest)-i)+'-1-1'),'%Y-%m-%d'))
    return pivot_list

def GetpageTitle(Qcode):
    url="https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=sitelinks&ids="+Qcode+"&sitefilter=enwiki"
    r = requests.get(url).json()
    entities = r.get('entities')
    title = ''
    if entities:
        entity = entities.get(Qcode)
        if entity:
            sitelinks=entity.get('sitelinks')
            if sitelinks:
                enwiki=sitelinks.get('enwiki')
                if enwiki:
                    title=enwiki.get('title')
    return title


def calculate_percentage(Qcode_pageTitle,pageTitle,pivot_list):
    '''
    This function calls all other necessary functions and finally calculates the 
    percentage and writes it to a csv file
    '''
    Qcode_WP=list()
    Qcode_WD=list() 
    #Qcode_pageTitle=GetQcodeofEntity(pageTitle)
    result=GetEntity(pageTitle)
    Qcode_WP=WPtoQcode_list(result)
    WP=set(Qcode_WP)
    WP_count=len(WP)
    revisionID_list,date_list=GetRevisionID(Qcode_pageTitle)
    sampledRevID_List=sampledRevision(revisionID_list,date_list,pivot_list)
    finalcount = -1
    percentage_list=[]
    for i in range(len(sampledRevID_List)):
        rev_id=sampledRevID_List[i]
        Qcode_WD=GetWDQcode(Qcode_pageTitle,rev_id)
        WD=set(Qcode_WD)
        p=WP & WD
        count=len(p)
        if WP_count==0:
            percentage_list.append("None")
        else:
            percentage=(count/WP_count)*100
            percentage_list.append(percentage)
        if (finalcount == -1):
            finalcount = count
    with open("revisionAnalysis_new.csv","a",newline='',encoding="utf-8") as file_result:
        csvwriter = csv.writer(file_result)     
        
        """
        printing the scores
        """
        csv_list=[]
        csv_list.append(Qcode_pageTitle)
        for i in range(len(percentage_list)):
            last_percentage=percentage_list[0]
            if ((percentage_list[i]!="None") and (last_percentage!=0)):
                csv_list.append(percentage_list[i]/last_percentage)
            else:
                csv_list.append("None")
        csv_list.append(finalcount)
        csv_list.append(WP_count)
        csvwriter.writerow(csv_list)
            

def find_pageTitle_for_all_Qcode(Qcode_inputlist,pivot_list):
    """
    This function finds the corresponding pageTitle for each Qcode in the 
    Qcode_inputlist and passes each of the Qcode, pageTitle and pivot_list to the 
    function calculate_percentage
    """
    for Qcode in Qcode_inputlist:
        pageTitle=str(GetpageTitle(Qcode))
        if (len(pageTitle)>0):
            print('  Processing ' + pageTitle)
            calculate_percentage(Qcode,pageTitle,pivot_list) 


""" Specify the input file name here in the variable topicname. Currently it has a sample file with few entries as input 
"""
topicname = 'mini_sample-input'     
infile = topicname+'.csv'          
outfile = topicname+'_out.csv'          
print(infile)
print(outfile)
        
with open(infile,"r",encoding="utf-8") as file_input:
    Qcode_inputlist=[]
    for line in file_input:
        if 'item' in str(line):
            continue
        Qcode_inputlist += re.findall('entity/(Q.+)', line)


print("Read " + str(len(Qcode_inputlist)) + ' Q-codes for processing...')        
            
pivot_list=getDatePivotList() 

with open("revisionAnalysis_new.csv","w",newline='',encoding="utf-8") as file_result:
    csvwriter = csv.writer(file_result) 
        
    """
    printing the date column
    """
    csv_list=[]
    csv_list.append('Date')
    for i in range(len(pivot_list)):
        
        date=datetime.date(pivot_list[i])
        csv_list.append(date)
    csv_list.append("count")    
    csv_list.append("wp-count")    
    csvwriter.writerow(csv_list)

find_pageTitle_for_all_Qcode(Qcode_inputlist,pivot_list)

pd.read_csv('revisionAnalysis_new.csv', header=None).T.to_csv(outfile, header=False, index=False)

df=pd.read_csv(outfile)

df['Average']=df.mean(axis=1,numeric_only=True,skipna=True)

df.to_csv(outfile,encoding='utf-8',index=False)      


# In[ ]:





# In[ ]:




