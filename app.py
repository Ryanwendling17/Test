import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import plotly.graph_objects as go
import numpy as np
import io
import plotly.figure_factory as ff
import plotly.express as px
import datetime
from pandas.tseries.offsets import BDay
from fredapi import Fred
import lxml.html as lh
from collections import Counter
from pprint import pprint 
import operator 
import tweepy 
from flask import request
import time


consumer_key = 'DJKAOHAJzkG5JOsMSdSL1LUHL' 
consumer_secret = 'NZDLH50VVSNyx2tIx8qZ2bRsh3N6wtlKJxTy62ETlJmDScdWT9' 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)


api = tweepy.API(auth)

    
cnt = Counter() 

search_words = "#EconTwitter" + " -filter:retweets"

time_ = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(time.time()))
tweets = tweepy.Cursor(api.search,
                       q=search_words,
                       lang="en").items(5000)

users_locs = [[tweet.user.screen_name, tweet.user.location] for tweet in tweets]


tweet_text = pd.DataFrame(data=users_locs, 
                    columns=['user', "location"])
    
tweet_text['count'] = 1

Top_Users = tweet_text.groupby('user').sum()
Top_Users.reset_index(drop = False, inplace = True)
Top_Users[['user', 'count']]
Top_Users['user'] = '@' + Top_Users['user'].astype(str)
Top_Users = Top_Users.nlargest(15, 'count')
Top_Users.reset_index(drop = True, inplace = True)

Top_Locations = tweet_text.groupby('location').sum()
Top_Locations.reset_index(drop = False, inplace = True)
Top_Locations[['location', 'count']]
Top_Locations = Top_Locations[Top_Locations['location'] != ''] 
Top_Locations = Top_Locations.nlargest(15, 'count')
Top_Locations.reset_index(drop = True, inplace = True)


Top_Locations = Top_Locations.sort_values(by=['count'])
Top_Locations['percent'] = Top_Locations['count'] / 5000 * 100
x = Top_Locations['percent'].tolist()
y = Top_Locations['location'].tolist()

for i in range(0, len(x)):
    x[i] = str(round(x[i], 2)) + '%'

fig = go.Figure(data=[go.Bar(name = 'test', x=x, y=y, orientation='h', marker=dict(
        color='rgba(255, 48, 66, 0.6)',
        line=dict(
            color='rgba(255, 48, 66, 1.0)',
            width=1),
    ))],
               layout = {'xaxis': {'title': 'Share of Tweets', 'range': [0, Top_Locations['percent'].max()+.1]}})

# Source
annotations = []
annotations.append(dict(xref='paper', yref='paper', 
                        x=-.05, y=-0.24,
                        text='Source: Webscrape of 5,000 most recent #EconTwitter tweets as of '+str(time_),
                        font=dict(family='Arial', size=10, color='rgb(150,150,150)'),
                        align="left",
                        showarrow=False))

# Change the bar mode
fig.update_layout(barmode='group', title_text = 'Most Active Location Tags from #EconTwitter', xaxis_ticksuffix = "%",
                  annotations=annotations, 
                      margin=dict(l=20, r=20, t=70, b=90),
                  paper_bgcolor='rgb(248, 248, 255)',
                  plot_bgcolor='rgb(248, 248, 255)',)
fig.update_traces(texttemplate=x, textposition='outside')


TwitterLocations = fig

Top_Users = Top_Users.sort_values(by=['count'])
Top_Users['percent'] = Top_Users['count'] / 5000 * 100
x = Top_Users['percent'].tolist()
y = Top_Users['user'].tolist()

for i in range(0, len(x)):
    x[i] = str(round(x[i], 2)) + '%'

fig = go.Figure(data=[go.Bar(name = 'test', x=x, y=y, orientation='h', marker=dict(
        color='rgba(39, 103, 255, 0.6)',
        line=dict(
            color='rgba(39, 103, 255, 1.0)',
            width=1),
    ))],
               layout = {'xaxis': {'title': 'Share of Tweets', 'range': [0, Top_Locations['percent'].max()+.1]}})

# Source
annotations = []
annotations.append(dict(xref='paper', yref='paper', 
                        x=-.05, y=-0.24,
                        text='Source: Webscrape of 5,000 most recent #EconTwitter tweets as of '+str(time_),
                        font=dict(family='Arial', size=10, color='rgb(150,150,150)'),
                        align="left",
                        showarrow=False))

# Change the bar mode
fig.update_layout(barmode='group', title_text = 'Most Active Users from #EconTwitter', xaxis_ticksuffix = "%",
                  annotations=annotations, 
                      margin=dict(l=20, r=20, t=70, b=90),
                  paper_bgcolor='rgb(248, 248, 255)',
                  plot_bgcolor='rgb(248, 248, 255)',)
fig.update_traces(texttemplate=x, textposition='outside')

TwitterUsers = fig



url='https://www.bls.gov/emp/tables/unemployment-earnings-education.htm'
#Create a handle, page, to handle the contents of the website
page = requests.get(url)
#Store the contents of the website under doc
doc = lh.fromstring(page.content)
#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')

#Check the length of the first 12 rows
[len(T) for T in tr_elements[:12]]

tr_elements = doc.xpath('//tr')
#Create empty list
col=[]
i=0
#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    col.append((name,[]))
    
#Since out first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 10, the //tr data is not from our table 
    if len(T)!=3:
        break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1
        
Dict={title:column for (title,column) in col}
EdEconDf=pd.DataFrame(Dict)
EdEconDf = EdEconDf.astype(str)


EdEconDf.rename(columns=lambda x: x.replace('\r\n',''), inplace = True)
for col in EdEconDf.columns:
    EdEconDf[col] = EdEconDf[col].apply(lambda x: x.replace('\r\n',''))
    EdEconDf[col] = EdEconDf[col].apply(lambda x: x.replace(',',''))
    
EdEconDf['Unemployment rate (%)'] = EdEconDf['Unemployment rate (%)'].astype(float)
EdEconDf['Median usual weekly earnings ($)'] = EdEconDf['Median usual weekly earnings ($)'].astype(int)
    
EdEconDf = EdEconDf.loc[0:7]

states = ['AL',	'AK',	'AZ',	'AR',	'CA',	'CO',	'CT',	'DE',	'FL',	'GA',	'HI',	'ID',	'IL',	'IN',	'IA',	'KS',	'KY',	'LA',	'ME',	'MD',	'MA',	'MI',	'MN',	'MS',	'MO',	'MT',	'NE',	'NV',	'NH',	'NJ',	'NM',	'NY',	'NC',	'ND',	'OH',	'OK',	'OR',	'PA',	'RI',	'SC',	'SD',	'TN',	'TX',	'UT',	'VT',	'VA',	'WA',	'WV',	'WI',	'WY']
statesdf = pd.DataFrame(states, columns = ['State']) 

url = 'https://raw.githubusercontent.com/Ryanwendling17/Test/main/Data/labor_data.csv'
stateUR = pd.read_csv(url, error_bad_lines=False)

url = 'https://raw.githubusercontent.com/Ryanwendling17/Test/main/Data/EconFac.csv'
final_df = pd.read_csv(url, error_bad_lines=False)



x = final_df.columns.to_list()
x = x[0:3]

ku = final_df[final_df['Pop'] == final_df['Pop'][0]]
del ku['Pop']
ku = ku.T

ku = final_df[final_df['Pop'] == final_df['Pop'][0]]
del ku['Pop']
ku = ku.T

NatEcon = final_df[final_df['Pop'] == final_df['Pop'][1]]
del NatEcon['Pop']
NatEcon = NatEcon.T

Nat = final_df[final_df['Pop'] == final_df['Pop'][2]]
del Nat['Pop']
Nat = Nat.T

fig = go.Figure(data=[
    go.Bar(name=final_df['Pop'][0], x=x, y=ku[0], text = ku, marker=dict(
        color='rgba(39, 103, 255, 0.6)',
        line=dict(
            color='rgba(39, 103, 255, 1.0)',
            width=1),
    ),),
    go.Bar(name=final_df['Pop'][1], x=x, y=NatEcon[1], text = NatEcon,     marker=dict(
        color='rgba(255, 48, 66, 0.6)',
        line=dict(
            color='rgba(255, 48, 66, 1.0)',
            width=1),
    ),),
    go.Bar(name=final_df['Pop'][2], x=x, y=Nat[2], text = Nat, marker=dict(
        color='rgba(50, 171, 96, 0.6)',
        line=dict(
            color='rgba(50, 171, 96, 1.0)',
            width=1),
    ),)
])

# Source
annotations = []
annotations.append(dict(xref='paper', yref='paper',
                        x=-.05, y=-0.24,
                        text='Econ Source: Faculty Page, University of Kansas, Department of Economics, November 2020'+
                             '<br>National Econ Source: American Economic Association, Committee on the Status of Women in the Economics Profession (CSWEP) Annual Report, 2019'+
                             '<br>National All Dept. Source: U.S. Department of Education, National Center for Education Statistics, Integrated Postsecondary Education Data System (IPEDS) 2019',
                        font=dict(family='Arial', size=10, color='rgb(150,150,150)'),
                        align="left",
                        showarrow=False))

# Change the bar mode
fig.update_layout(barmode='group', title_text = 'Percent of Faculty who are Women', yaxis_ticksuffix = "%", 
                  annotations=annotations, 
                      margin=dict(l=20, r=20, t=70, b=90),
                  paper_bgcolor='rgb(248, 248, 255)',
                  plot_bgcolor='rgb(248, 248, 255)',)
fig.update_traces(texttemplate='%{text}'+'%', textposition='outside')

EconFacFig = fig



metrics = stateUR['varb'].unique().tolist()

datesCCA = stateUR['Date'].unique().tolist()



#Jobs DF

jobs = pd.DataFrame(columns = ['Title', 'Details', 'id'])


newJob1 = {'Title': 'Research Assistant, Federal Reserve Bank of Chicago', 'Details': 'In this role, Research Assistants will utilize analytical skills in the areas of Economics, Finance, Statistics, Mathematics and Computer Science to support academic research and policy work by staff economists. Tasks include quantitative research analyses using economic and financial data; computer programming; preparation of briefings and educational outreach materials; and financial and economic database management. View application requirements and apply [here!](https://nam10.safelinks.protection.outlook.com/?url=https%3A%2F%2Furldefense.com%2Fv3%2F__https%3A%2F%2Fnam02.safelinks.protection.outlook.com%2F%3Furl%3Dhttps*3A*2F*2Ffrb.taleo.net*2Fcareersection*2Fjobdetail.ftl*3Fjob*3D265213*26lang*3Den*23.X1Jks6jqy6o.mailto%26data%3D02*7C01*7Cmigarciaperez*40stcloudstate.edu*7Cfef5b3aa20924c04e1ef08d854d3b173*7C5011c7c60ab446ab9ef4fae74a921a7f*7C0*7C1*7C637352615503270729%26sdata%3DevRUvYu751TTcH65voyyGkrRYcCje2JZ1TmrQVh1k1I*3D%26reserved%3D0__%3BJSUlJSUlJSUlJSUlJSUlJSUlJQ!!PhOWcWs!h3MBHaOUp9lHzyv1mv-lKMvTyR34TIfKwP9PqF5Qku6-O9oNQt56vfwdsQjjBylXTT0%24&data=02%7C01%7Casiedu%40ku.edu%7Cc5b6ab0121ce4db6c23c08d854f73c93%7C3c176536afe643f5b96636feabbe3c1a%7C0%7C0%7C637352768193288377&sdata=HVxu57DX65LssBX8wBDJsfiMw%2Bfu2DZ04NUGM97RAhM%3D&reserved=0)', 'id': 1}
newJob2 = {'Title': 'Beyond KU: Careers in Politics', 'Details': 'Sponsored by the University Career Center and the Dole Institute for Politics, this event will demonstrate how to turn your passion for politics into a career regardless of your major. From a legislative aide and policy analyst to a political reporter and lobbyist, there are dozens of careers available. Join this panel discussion and learn how to jumpstart a career working in politics alongside elected officials. You can join the live stream via [Facebook](https://www.facebook.com/kucareer) or [YouTube](https://www.youtube.com/c/TheDoleInstituteofPolitics/) this Tuesday, November 17th at 3:00 pm.', 'id': 2}

newJobs = [newJob1,
           newJob2]

jobs = jobs.append(newJobs, ignore_index=True)
jobs = jobs.sort_values(by=['id'], ascending=False)





#Academic DF

Academic = pd.DataFrame(columns = ['Title', 'Details', 'id'])


newAcademic1 = {'Title': 'AEA Summer Training Program & Scholarship Program', 'Details': 'This promotes diversity by preparing talented undergraduates for doctoral programs in Economics and related disciplines. Hosted at Howard University, students receive eight weeks of intensive training in microeconomics, mathematics, econometrics, and research methods from prominent faculty and economists at the Federal Reserve Board. Students have the opportunity to earn up to 12 college credits, participate in experiential learning, and join inclusive mentoring groups. Click [here](https://nam10.safelinks.protection.outlook.com/?url=https%3A%2F%2Furldefense.com%2Fv3%2F__https%3A%2F%2Fnam04.safelinks.protection.outlook.com%2F%3Furl%3Dhttp*3A*2F*2Feconomics.howard.edu*2Faeasp%26data%3D02*7C01*7Coswinton*40howard.edu*7C81b4fb3379bf47a0c0ce08d853f42e90*7C02ac0c07b75f46bf9b133630ba94bb69*7C0*7C0*7C637351655503414001%26sdata%3DLPjHIX1nN2B*2BBbL*2FKDIzP7mIggZRZEUGDSJ9OGwmBjE*3D%26reserved%3D0__%3BJSUlJSUlJSUlJSUlJSUl!!PhOWcWs!hDAWigW9ZLzgDbXtU2NbcAz5D9pmuRIVF2giTw1Buee2sAZi_JpQW4Z5k7AxNc_a33g%24&data=02%7C01%7Casiedu%40ku.edu%7C3d6c0492c81f4c2c8a1a08d86a2a9e91%7C3c176536afe643f5b96636feabbe3c1a%7C0%7C1%7C637376078584039853&sdata=EiaEfmjtQUlxpBUcT%2FJjERnx%2FielhfWP07w4c1me5MY%3D&reserved=0) for more information and to apply. The anticipated application deadline is January 31, 2021.', 'id': 1}
newAcademic2 = {'Title': 'Tobin Center / Economics Pre-Doctoral Fellows Program', 'Details': 'The Tobin Center / Economics Pre-Doctoral Fellows Program at Yale University supports policy-relevant economics research by providing a high-quality education and training experience for individuals with bachelor’s or master’s degrees who are considering pursuing a Ph.D. in economics or a closely related discipline. Pre-doctoral fellows work for one to two years as full-time research assistants for one or more faculty mentors and engage in additional education and training activities, including taking for credit or auditing one course per semester, participating in a weekly professional development seminar, and attending department research seminars. Apply [here.](https://nam10.safelinks.protection.outlook.com/?url=https%3A%2F%2Furldefense.com%2Fv3%2F__https%3A%2F%2Ftobin.yale.edu%2Ftobin-predoctoral-fellows__%3B!!PhOWcWs!jgtuBlPYZUhcZsuq2BCp1J7HO9xcsDVUylMmANH2Dd0wz5R2rkXMVxCl6VX6jbHcKw%24&data=04%7C01%7Casiedu%40ku.edu%7C5d754ba2bf2e4b6c841b08d87f498477%7C3c176536afe643f5b96636feabbe3c1a%7C0%7C0%7C637399301025987936%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C1000&sdata=U1tg00Wtn%2Fg4Qb7F6V2NWCJkgA49fYr6X3NCbx5WIvM%3D&reserved=0)', 'id': 2}

newAcademic = [newAcademic1,
               newAcademic2]

Academic = Academic.append(newAcademic, ignore_index=True)
Academic = Academic.sort_values(by=['id'], ascending=False)





#Department DF

Department = pd.DataFrame(columns = ['Title', 'Details', 'id'])


newDepartment1 = {'Title': 'Economics Club', 'Details': 'The Economics Club is back and meeting regularly Thursday evenings at 6:00 PM via Zoom. Join the meetings using this [link](https://kansas.zoom.us/j/95313313570), the password is 2020. There will be a number of great events this year so anyone interested in economics, coding, or research should consider getting involved. No official joining process is required, simply start coming to meetings when you can!', 'id': 2}

newDepartment = [newDepartment1]

Department = Department.append(newDepartment, ignore_index=True)
Department = Department.sort_values(by=['id'], ascending=False)




#Student Resources DF

resources = pd.DataFrame(columns = ['Title', 'Details'])


newResources1 = {'Title': 'Professor Slusky\'s Office Hours', 'Details': 'Professor Slusky is the director of undergraduate studies in the economics department. Feel free to drop by his office hours this semester via Zoom if you have any questions about the economics program. You can access his office hours via [link](http://kansas.zoom.us/my/davidslusky) on Tuesdays from 2-4 pm and on Thursdays from 9-11 am. (Password: 1115)'}
newResources2 = {'Title': 'Ryan Wendling\'s Office Hours', 'Details': 'Ryan is a senior economics student who works for Professor Slusky. He is also available via Zoom this semester to answer any questions you may have about the economics department. You can access his office hours via this [link](https://kansas.zoom.us/j/96482325564) on Mondays and Fridays from 3-5 pm. (Password: 102891)'}
newResources3 = {'Title': 'Stata Webinar: Creating customized reports in Word, Excel, and PDF', 'Details': 'Join Gabriela Ortiz, Applied Statistician, as she demonstrates how to create Word documents with Stata summary statistics, regression tables, and graphs. Find out how to interact Stata\'s features with Word\'s features and how to automate your work when you want to regularly update reports. You will also see how easy it is to use putpdf and putexcel to similarly create reproducible reports in PDF and Excel formats. Register for this free event [here](https://www.stata.com/training/webinar/reproducible-reporting-putdocx/).'}

newResources = [newResources1,
                newResources2,
                newResources3]

resources = resources.append(newResources, ignore_index=True)




#Media DF

Media = pd.DataFrame(columns = ['Title', 'Details'])


newMedia1 = {'Title': 'Econ Twitter!', 'Details': 'If you\'re not already on Econ Twitter and have any interest in economics at all, then you should be! Econ twitter is a loosely defined community of economics professors, students, researchers, and enthusiast who tweet about cool new papers, issues in the field, economic policy, and lots of cats and dogs. A good place to get started on Econ Twitter is to follow these people:\n \n &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - [@causalinf]( https://twitter.com/causalinf?s=20) \n\n &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - [@leah_boustan]( https://twitter.com/leah_boustan?s=20) \n\n &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  - [@jenniferdoleac]( https://twitter.com/jenniferdoleac?s=20) \n\n &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  - [@JustinWolfers]( https://twitter.com/JustinWolfers?s=20) \n\n &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  - [@graykimbrough]( https://twitter.com/graykimbrough?s=20) \n\n &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  - [@ENPancotti]( https://twitter.com/ENPancotti?s=20) \n\n &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  - [@drlisadcook]( https://twitter.com/drlisadcook?s=20) \n\n New members are embraced so feel free to start tweeting using #EconTwitter, but lurkers are more than welcome so don\'t be afraid to just follow and enjoy the community!'}
newMedia2 = {'Title': 'What an Economist Looks Like', 'Details': 'Representation matters, and due to economics\' diversity problem along both racial and gender lines, many very talented people from diverse backgrounds never get to see themselves represented in our field. At the end of the day, economics is about people, and driving people away from our field who bring a wide array of research interests and perspectives hurts our profession and society. *What an Economist Looks Like* is an Econ Twitter initiative to increase the representation of women and underrepresented minorities in economics. Our first featured economist is our very own Professor Elizabeth Asiedu. Professor Asiedu is an Associate Chair, Director of Graduate Studies, and the founder and president of the Association for the Advancement of African Women Economists ([AAAWE]( http://www.aaawe.org/)). Professor Asiedu is the recipient of the 2020 [Sadie Collective]( https://www.sadiecollective.org/) award for Academic Scholarship and Mentorship. Professor Asiedu\'s research focuses on Foreign Direct Investment, Foreign Aid, and Gender. You can read more about Professor Asiedu [here.]( http://people.ku.edu/~asiedu/)'}
newMedia3 = {'Title': 'What We\'re Listening to This Week', 'Details': 'Capitalisn\'t is a podcast led by Professor Kate Waldock from Georgetown University and Professor Luigi Zingales from the University of Chicago. They debunk common misconceptions of capitalism, where it goes wrong, and how it impacts the world we live in. In this episode, they discuss how capitalism will impact the dissemination of the COVID-19 vaccine.'}

newMedia = [newMedia1,
            newMedia2,
            newMedia3]

Media = Media.append(newMedia, ignore_index=True)





layout_TS = go.Layout(
    hovermode = 'closest', margin=dict(l=50, r=50, t=30, b=50))


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


#Edu Fig
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import numpy as np

y_UR = EdEconDf['Unemployment rate (%)'].tolist()
y_Earn = EdEconDf['Median usual weekly earnings ($)'].tolist()

x = EdEconDf['Educational attainment'].tolist()


# Creating two subplots
fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                    shared_yaxes=False, vertical_spacing=0.001)

fig.append_trace(go.Bar(
    x=y_UR,
    y=x,
    marker=dict(
        color='rgba(255, 48, 66, 0.6)',
        line=dict(
            color='rgba(255, 48, 66, 1.0)',
            width=1),
    ),
    name='Unemployment Rate',
    orientation='h',
), 1, 1)

fig.append_trace(go.Bar(
    x=y_Earn,
    y=x,
    marker=dict(
        color='rgba(39, 103, 255, 0.6)',
        line=dict(
            color='rgba(39, 103, 255, 1.0)',
            width=1),
    ),
    name='Median Usual Weekly Earnings',
    orientation='h',
), 1, 2)

fig.update_layout(
    title='Unemployment Rates and Earnings by Educational Attainment',
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        domain=[0, 0.85],
    ),
    yaxis2=dict(
        showgrid=False,
        showline=True,
        showticklabels=False,
        linecolor='rgba(102, 102, 102, 0.8)',
        linewidth=2,
        domain=[0, 0.85],
    ),
    xaxis=dict(
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0, 0.42],
    ),
    xaxis2=dict(
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0.47, 1],
        side='top',
    ),
    legend=dict(x=0.029, y=1.038, font_size=10),
    margin=dict(l=20, r=20, t=70, b=90),
    paper_bgcolor='rgb(248, 248, 255)',
    plot_bgcolor='rgb(248, 248, 255)',
)

annotations = []

y_s = np.round(y_UR, decimals=2)
y_nw = np.round(y_Earn, decimals=0)

# Adding labels
for ydn, yd, xd in zip(y_nw, y_s, x):
    # labeling the scatter savings
    annotations.append(dict(xref='x2', yref='y2',
                            y=xd, x=ydn + 160,
                            text='$'+'{:,}'.format(ydn) ,
                            font=dict(family='Arial', size=12,
                                      color='rgb(0, 52, 89)'),
                            showarrow=False))
    # labeling the bar net worth
    annotations.append(dict(xref='x1', yref='y1',
                            y=xd, x=yd + .5,
                            text=str(yd) + '%',
                            font=dict(family='Arial', size=12,
                                      color='rgb(151, 27, 47)'),
                            showarrow=False))
# Source
annotations.append(dict(xref='paper', yref='paper',
                        x=-.05, y=-0.24,
                        text='Source: Current Population Survey, U.S. Department of Labor, U.S. Bureau of Labor Statistics',
                        font=dict(family='Arial', size=10, color='rgb(150,150,150)'),
                        showarrow=False))

EduFig = fig.update_layout(annotations=annotations)



# Populate the layout with HTML and graph components
app.layout = html.Div(children = [
    html.Div(children = [
        html.Img(id='KuLogo', src='https://kulogo.s3.us-east-2.amazonaws.com/KuLogo.PNG'),
    html.Div(children = [
    html.H2("Department of Economics", style={'font-size': '28pt', 'background-color': '#0051ba'}),
    html.H3("Undergraduate Resources", style={'font-size': '18pt', 'background-color': '#0051ba'}),
    ], style={'width':'100%', 'margin-right': '-10px'}),], style={'display': 'inline-flex', 'width':'100%', 'margin-left': '-10px'}),
    dcc.Tabs([
    dcc.Tab(label='Job Opportunities', children=[
    html.Div(children = [
    html.H4(jobs.iloc[0, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(jobs.iloc[0, 1])),
    ],style={'display': 'inline-block', 'width': '40%', 'vertical-align': 'top'}),
    html.Div(children = [
       dcc.Graph(id = 'PlayerComWeek'),
    # dropdown
        html.Div(children = [
            html.Label("State 1"),
            html.Label("State 2"),
            html.Label("Metric")
        ], style={'width':'100%',
                 'display': 'inline-flex'}),
        html.Div(
        [
            html.Div(children = [
            dcc.Dropdown(
                id="MyPick",
                options=[{
                    'label': i,
                    'value': i
                } for i in states],
                value="KS"),], style={'margin-right':'75px','width': '120px'}),
            
            html.Div(children = [
            dcc.Dropdown(
                id="Counterfactual",
                options=[{
                    'label': i,
                    'value': i
                } for i in states],
                value=states[1]),], style={'margin-right':'75px','width': '120px'}),
            
            
            html.Div(children = [
            dcc.Dropdown(
                id="METRIC",
                options=[{
                    'label': i,
                    'value': i
                } for i in metrics],
                value="Unemployment Rate"),], style={'width': '300px'}),
        ],
        style={'width': '100%',
               'margin-right':'20%',
               'display': 'inline-flex'}),
    ],style={'display': 'inline-block', 'width': '50%', 'margin-left': '100px', 'margin-top': '30px'}),
        
         html.Div(children = [
        html.H4(jobs.iloc[1, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(jobs.iloc[1, 1])),
    ],style={'display': 'inline-block', 'width': '40%', 'vertical-align': 'top', 'margin-top': '-21.5%'}),
        
    ],style={'margin-left': 'auto', 'margin-right': 'auto'}),
    dcc.Tab(label='Academic Opportunities', children=[
        
    html.Div(children = [
    html.H4(Academic.iloc[0, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(Academic.iloc[0, 1])),
    ],style={'display': 'inline-block', 'width': '40%', 'vertical-align': 'top'}),
    html.Div(children = [
       dcc.Graph(id = 'EduFig', figure = EduFig),
    ],style={'display': 'inline-block', 'width': '50%', 'margin-left': '100px', 'margin-top': '30px'}),
        
    html.Div(children = [
        html.H4(Academic.iloc[1, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(Academic.iloc[1, 1])),
    ],style={'display': 'inline-block', 'width': '40%', 'vertical-align': 'top', 'margin-top': '-15%'}),
        
    ]),
    dcc.Tab(label='Student Resources', children=[
    html.Div(children = [
    html.H4(resources.iloc[0, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(resources.iloc[0, 1])),
    ],style={'display': 'inline-block', 'width': '40%'}),
    html.Div(children = [
        html.H4(resources.iloc[1, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(resources.iloc[1, 1])),
    ],style={'display': 'inline-block', 'width': '40%', 'margin-left': '100px'}),
    html.Div(children = [
        html.H4(resources.iloc[2, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(resources.iloc[2, 1])),
    ],style={'display': 'inline-block', 'width': '40%'}),
    ],style={'margin-left': 'auto', 'margin-right': 'auto'}),
    dcc.Tab(label='Departmental Events', children=[
    
    html.Div(children = [
        html.H4(Department.iloc[0, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(Department.iloc[0, 1])),
    ],style={'display': 'inline-block', 'width': '40%'}),
        
    ]),
        
        dcc.Tab(label='Media', children=[
    
      html.Div(children = [
html.H4(Media.iloc[0, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(Media.iloc[0, 1])),
    ],style={'display': 'inline-block', 'width': '40%', 'vertical-align': 'top'}),
            
            html.Div(children = [
                dcc.Graph(id = 'TwitterGraph'),
 
            
        html.Div(children = [
            dcc.Dropdown(
                id="TweetVar",
                options=[{
                    'label': i,
                    'value': i
                } for i in ['Location', 'Users']],
                value="Location"),], style={'width': '300px'}),
                
                ], style={'display': 'inline-block', 'width': '50%', 'margin-left': '100px', 'margin-top': '30px'}),
       
            
        html.Div(children = [
        html.H4(Media.iloc[1, 0], style={'font-size': '16pt'}),
        html.Img(id='WhatAnEconLooksLike', src='https://kulogo.s3.us-east-2.amazonaws.com/ElizabethAsiedu.jpeg', style={'width': '33%', 'float': 'left', 'margin-top': '10px'}),
        html.P(dcc.Markdown(Media.iloc[1, 1])),
    ],style={'display': 'inline-block', 'width': '40%', 'vertical-align': 'top'}),
            
                    html.Div(children = [
        html.H4(Media.iloc[2, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(Media.iloc[2, 1])),
        html.Iframe(height="200px", width="100%",  src="https://player.simplecast.com/3f569c22-cd49-4002-9196-61f520232977?dark=false"),
    ],style={'display': 'inline-block', 'width': '40%', 'margin-left': '100px'}),
            
    ]),
        
        
    dcc.Tab(label='Other', children=[
    
      html.Div(children = [
    html.H4('Economics\' Gender Problem', style={'font-size': '16pt'}),
        html.P(dcc.Markdown('Our field has always had a gender imbalance problem, but unlike other social sciences, economics has been closing the gender gap at an incredibly slow rate. The University of Kansas is not immune to these issues. In recent years, the KU economics faculty male/female ratio has grown to be more in line with the national economics average but compared to the average academic department we still fall far behind. Bias against women has an outsized negative influence on our profession both nationally and at KU. In 2019, the American Economic Association ([AEA]( chrome-extension://oemmndcbldboiebfnladdacbdfmadadm/https:/www.aeaweb.org/resources/member-docs/climate-survey-results-mar-18-2019)) surveyed over 9,000 current and former AEA members, finding roughly half of women respondents have experienced discrimination and nearly two-thirds feel their work is taken less seriously than their male counterparts. Female students often report harassment and discrimination, and female faculty face higher standards in their research and tend to be given worse student evaluations than male instructors. ([Boring, 2017]( https://doi.org/10.1016/j.jpubeco.2016.11.006))\n\nThe economics undergraduate committee is concerned with the gender disparities evident in our field and in our department at KU. We are working to combat these issues, and to begin to address other issues of gender discrimination that our trans and non-binary students may be facing. Specifically, this past year we have worked to increase mentoring efforts for undergraduate women, increase female representation, and introduce gender neutral bathrooms to Snow Hall. Committee leadership has completed KU Safe Space training so please feel comfortable reaching out with any questions or concerns you might have. ')),
    ],style={'display': 'inline-block', 'width': '40%', 'vertical-align': 'top'}),
        html.Div(children = [
       dcc.Graph(id = 'EconFac', figure = EconFacFig),
        ], style={'display': 'inline-block', 'width': '50%', 'margin-left': '100px', 'margin-top': '30px'}),
        

    ]),]),])
    
    
    
#Add callback functions
@app.callback(Output('TwitterGraph', 'figure'),
             [Input('TweetVar', 'value')])
def update_figure(input1):
    if input1 == 'Location':
        TwitterFig = TwitterLocations
    else:
        TwitterFig = TwitterUsers
    return TwitterFig





#Add callback functions
@app.callback(Output('PlayerComWeek', 'figure'),
             [Input('MyPick', 'value'),
             Input('Counterfactual', 'value'),
             Input('METRIC', 'value')])
def update_figure(input1, input2, input3):
    # filtering the data
    data  = stateUR[stateUR.varb == input3]
    data1 = data[data.State == input1]
    data2 = data[data.State == input2]
    # updating the plot
    trace_1 = go.Scatter(x = data1.Date, y = data1[input3],
                        name = input1,
                         mode='lines+markers',
                         marker={
                'size': 10,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
                        )
    trace_2 = go.Scatter(x = data2.Date, y = data2[input3],
                        name = input2,
                         mode='lines+markers',
                        marker={
                'size': 10,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            })
    figCCA = go.Figure(data = [trace_1, trace_2], layout = layout_TS)
    if input3 == 'Unemployment Rate':
        figCCA.update_layout(yaxis_ticksuffix = "%")
    figCCA.update_layout(title_text=input3)
    return figCCA
  
app.title('KU Econ Undergrad Resources')
    
if __name__ == '__main__':
    app.run_server(debug=False)
