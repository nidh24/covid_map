import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import requests
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
# init_notebook_mode(connected=True)

url="https://www.worldometers.info/coronavirus/"
req=requests.get(url)
soup=BeautifulSoup(req.text,'lxml')


table=soup.find('table')


columns=[]
for i in table.find_all('th'):
    columns.append(i.text)

s=str(table)

rows=[]
tbd=table.find('tbody')
for i in tbd.find_all('tr'):
    r=[]
    for j in i.find_all('td'):
        r.append(j.text)
    rows.append(r)


df = pd.DataFrame(rows, columns = columns)

continents=df[:6]
world=df[7:8]
countries=df[8:]


def rep(li):
    if(li=='' or li==' ' or li=='N/A'):
        return 0
    return li.replace(',','')

for i in columns[2:10]:
    countries[str(i)]=list(map(int,(map(rep,countries[str(i)]))))
countries[columns[12]]=list(map(int,(map(rep,countries[columns[12]]))))
countries[columns[14]]=list(map(int,(map(rep,countries[columns[14]]))))
for i in columns[16:19]:
    countries[str(i)]=list(map(int,(map(rep,countries[str(i)]))))

colscale='Greys,YlGnBu,Greens,YlOrRd,Bluered,RdBu,Reds,Blues,Picnic,Rainbow,Portland,Jet,Hot,Blackbody,Earth,Electric,Viridis,Cividis'
colscalist=colscale.split(',')


alldata=[]
for i in columns[2:10]:
    data = dict(type='choropleth',colorscale=colscalist[10],reversescale = True,locations=countries['Country,Other'],locationmode="country names",z=countries[i],text=countries['#'],colorbar=dict(title = i,lenmode = 'pixels'))
    alldata.append(data)
data = dict(type='choropleth',colorscale=colscalist[10],reversescale = True,locations=countries['Country,Other'],locationmode="country names",z=countries[columns[12]],text=countries['#'],colorbar=dict(title = columns[12],lenmode = 'pixels'))
alldata.append(data)
data = dict(type='choropleth',colorscale=colscalist[10],reversescale = True,locations=countries['Country,Other'],locationmode="country names",z=countries[columns[14]],text=countries['#'],colorbar=dict(title = columns[14],lenmode = 'pixels'))
alldata.append(data)
for i in columns[16:19]:
    data = dict(type='choropleth',colorscale=colscalist[10],reversescale = True,locations=countries['Country,Other'],locationmode="country names",z=countries[i],text=countries['#'],colorbar=dict(title = i,lenmode = 'pixels'))
    alldata.append(data)
    
##0,10,12,16,17




projtypes=['equirectangular', 'mercator', 'orthographic', 'natural earth', 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 'azimuthal equidistant', 'conic equal area', 'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff','sinusoidal']
layout=dict(title='Covid Data',geo=dict(showocean=True, oceancolor="LightBlue",projection={'type':projtypes[3]}))
##2,3,5,15



allchoro=[]
for i in range(len(alldata)):
    choromap=go.Figure(data=[alldata[i]],layout=layout)
    allchoro.append(choromap)


refdict=dict()
dictref=dict()

for i in range(8):
    refdict[columns[i+2]]=i
refdict[columns[12]]=8
refdict[columns[14]]=9
for i in range(10,13):
    refdict[columns[i+6]]=i
    
for i in range(8):
    dictref[i]=columns[i+2]
dictref[i+1]=columns[12]
dictref[i+2]=columns[14]
for i in range(10,13):
    dictref[i]=columns[i+6]



while True:
    print("=======================================================================")
    for i in range(len(alldata)):
        print(str(i+1)+'. '+dictref[i])
    ask=int(input("choose one of the following between 1 to 13: \n"))
    iplot(allchoro[ask-1])
    plot(allchoro[ask-1])

    askagain=input("Try again (Y/N) ?")
    if(askagain=='Y' or askagain=='y'):
        continue
    elif(askagain=='N' or askagain=='n'):
        print('Exiting')
        break
    else:
        print("Wrong Choice. Choose again")
        continue


