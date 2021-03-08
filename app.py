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


consumer_key = 'G8PueI9oNJHhpsKZgdi8S9GB0' 
consumer_secret = 'zUKhkY2GtTjdxUbNQCRsolThgiL7A4ULVjIEWUFRVCDN5QRgfI' 

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
               layout = {'xaxis': {'title': 'Share of Tweets', 'range': [0, Top_Locations['percent'].max()+.15]}})

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
               layout = {'xaxis': {'title': 'Share of Tweets', 'range': [0, Top_Locations['percent'].max()+.15]}})

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

api_key = 'c275198525f07f75104d93784a5644ff'
states = ['AL',	'AK',	'AZ',	'AR',	'CA',	'CO',	'CT',	'DE',	'FL',	'GA',	'HI',	'ID',	'IL',	'IN',	'IA',	'KS',	'KY',	'LA',	'ME',	'MD',	'MA',	'MI',	'MN',	'MS',	'MO',	'MT',	'NE',	'NV',	'NH',	'NJ',	'NM',	'NY',	'NC',	'ND',	'OH',	'OK',	'OR',	'PA',	'RI',	'SC',	'SD',	'TN',	'TX',	'UT',	'VT',	'VA',	'WA',	'WV',	'WI',	'WY']
statesdf = pd.DataFrame(states, columns = ['State']) 

fred = Fred(api_key=api_key)

stateUR = pd.DataFrame()

for state in statesdf['State']:
    try:
        data = fred.get_series(state+'UR', observation_start='2019-01-01')
        data = pd.DataFrame(data) 
        data.reset_index(drop = False, inplace = True)
        data.rename(columns={"index": "Date", 0: "Unemployment Rate"}, inplace = True)
        data['State'] = state
        data['varb'] = 'Unemployment Rate'
        stateUR = stateUR.append(data, ignore_index=True)
    except:
        pass
    try:
        data = fred.get_series(state+'RPIPC', observation_start='2014-01-01')
        data = pd.DataFrame(data) 
        data.reset_index(drop = False, inplace = True)
        data.rename(columns={"index": "Date", 0: "Real Per Capita Personal Income"}, inplace = True)
        data['State'] = state
        data['varb'] = 'Real Per Capita Personal Income'
        stateUR = stateUR.append(data, ignore_index=True)
    except:
        pass

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



newJob1 = {'Title': 'Agricultural Economist', 'Details': 'This position at the USDA in Kansas City, MO involves collecting, processing, and interpreting raw data to determine the significance of the findings. You will clean, analyze, and manage large complex datasets, and utilize the following statistical or data management software to conduct economic analyses: Excel; SAS, Stata or other statistical software; R Python, SQL or other equivalent programming languages; and Tableau or other data visualizations software. Apply [here!]( https://www.usajobs.gov/GetJob/ViewDetails/581486800)', 'id': 1}
newJob2 = {'Title': 'Bain & Company\'s Texas Womxn\'s Leadership Summit', 'Details': 'Are you an undergraduate sophomore or junior womxn interested in tackling global business challenges in your career? Do you want to learn about how to work and be successful in the consulting industry? Join Bain Texas virtually this spring at our Texas Womxn’s Leadership Summit on April 29th – 30th. The Womxn’s Summit will provide you with the insight needed to thrive as a business leader and be successful as a Bain consultant. Apply [here!](http://bit.ly/21twls)', 'id': 2}


newJobs = [newJob1,
           newJob2,
          ]

jobs = jobs.append(newJobs, ignore_index=True)
jobs = jobs.sort_values(by=['id'], ascending=False)





#Academic DF

Academic = pd.DataFrame(columns = ['Title', 'Details', 'id'])


newAcademic1 = {'Title': 'Tobin Center / Economics Pre-Doctoral Fellows Program', 'Details': 'The Tobin Center / Economics Pre-Doctoral Fellows Program at Yale University supports policy-relevant economics research by providing a high-quality education and training experience for individuals with bachelor’s or master’s degrees who are considering pursuing a Ph.D. in economics or a closely related discipline. Pre-doctoral fellows work for one to two years as full-time research assistants for one or more faculty mentors and engage in additional education and training activities, including taking for credit or auditing one course per semester, participating in a weekly professional development seminar, and attending department research seminars. Apply [here.](https://nam10.safelinks.protection.outlook.com/?url=https%3A%2F%2Furldefense.com%2Fv3%2F__https%3A%2F%2Ftobin.yale.edu%2Ftobin-predoctoral-fellows__%3B!!PhOWcWs!jgtuBlPYZUhcZsuq2BCp1J7HO9xcsDVUylMmANH2Dd0wz5R2rkXMVxCl6VX6jbHcKw%24&data=04%7C01%7Casiedu%40ku.edu%7C5d754ba2bf2e4b6c841b08d87f498477%7C3c176536afe643f5b96636feabbe3c1a%7C0%7C0%7C637399301025987936%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C1000&sdata=U1tg00Wtn%2Fg4Qb7F6V2NWCJkgA49fYr6X3NCbx5WIvM%3D&reserved=0)', 'id': 1}
newAcademic2 = {'Title': 'Whitcomb Essay Contest', 'Details': 'Submissions should be no longer than 5,000 words and should address "the relationship of knowledge, thought, and action in public affairs and public policy”. The committee interprets this theme broadly. In addition to receiving a $500 cash prize, the winner of the contest will have their name engraved on the Whitcomb plaque at Nunemaker Center. This contest is open to all undergraduates at KU. Further information is available [here.](https://honors.ku.edu/whitcomb-essay-contest)', 'id': 2}

newAcademic = [newAcademic1,
               newAcademic2]

Academic = Academic.append(newAcademic, ignore_index=True)
Academic = Academic.sort_values(by=['id'], ascending=False)





#Department DF

Department = pd.DataFrame(columns = ['Title', 'Details', 'id'])


newDepartment1 = {'Title': 'Economics Club', 'Details': 'The Economics Club is back and meeting regularly Thursday evenings at 6:00 PM via Zoom. Join the meetings using this [link](https://kansas.zoom.us/j/95313313570), the password is 2020. There will be a number of great events this year so anyone interested in economics, coding, or research should consider getting involved. No official joining process is required, simply start coming to meetings when you can!', 'id': 1}
newDepartment2 = {'Title': 'How to Get a Job During the Pandemic', 'Details': 'Jen Boden (KU Alum) and professional recruiter Chad Montgomery from Ecco Select to discuss “How to Get a Job During the Pandemic.” This seminar will focus on the unwritten rules of searching for a job. Topics will include how to use LinkedIn to get notice and find jobs, how to search for jobs, how to get interviews and what to expect from interviews, how to write a resume that will get you an interview, and how to develop your professional network. The seminar would be appropriate for graduate and undergraduate students. The format will be 10 minutes from Jen and Chad and then Q&A. Please use [this link]( https://kansas.zoom.us/j/98120044055) to attend, the password is 2021.', 'id': 2}

newDepartment = [newDepartment1,
                 newDepartment2
                ]

Department = Department.append(newDepartment, ignore_index=True)
Department = Department.sort_values(by=['id'], ascending=False)




#Student Resources DF

resources = pd.DataFrame(columns = ['Title', 'Details'])


newResources1 = {'Title': 'Professor Slusky\'s Office Hours', 'Details': 'Professor Slusky is the director of undergraduate studies in the economics department. Feel free to drop by his office hours this semester via Zoom if you have any questions about the economics program. You can access his office hours via [link](http://kansas.zoom.us/my/davidslusky) on Tuesdays from 11-12:30 pm and on Thursdays from 9-11 am. (Password: 1115)'}
newResources2 = {'Title': 'Ryan Wendling\'s Office Hours', 'Details': 'Ryan is a senior economics student who works for Professor Slusky. He is also available via Zoom this semester to answer any questions you may have about the economics department. You can access his office hours via this [link](https://kansas.zoom.us/j/96482325564) on Mondays and Fridays from 3-5 pm. (Password: 102891)'}
newResources3 = {'Title': 'SQL Overview and Exercises', 'Details': 'If you plan to continue to work with data after you graduate, SQL is arguably the most valuable language you can learn. SQL is how large firms process, store, and pull data. This video walks you through a SQL lesson/assignment that you can download and work through [here](https://www.youtube.com/redirect?redir_token=QUFFLUhqa2hCekxQaGF6S0hiN01zSl95M19YbzBaNFJvd3xBQ3Jtc0trWWMxRWFTR01YZ1BPMnFEMnRKdWgtM3lZa2dNaGsxOE5VQk9KMHRJQ3ZIWElKNklxWjhhT1NRZmJWV1RmSFZuZklWWDl3MWhDdjdqbzJrcDFLM2JKNnJTU2JDckRuY2NEbm5ETlBJaGE3aDcyX1p6Yw%3D%3D&v=kEevFRHiJFY&q=https%3A%2F%2Fdrive.google.com%2Fdrive%2Ffolders%2F1ACjKwvDK7i9fSxpD9-R2XpI4IsBrRlZv%3Fusp%3Dsharing&event=video_description). The setup instructions will help you get everything you need downloaded and installed, and the video will walk you through the lesson and answer the exercise questions. This is our first pass at creating instructional coding resources, if you like what you see let us know what other languages you would like resources for!'}

newResources = [newResources1,
                newResources2,
                newResources3]

resources = resources.append(newResources, ignore_index=True)




#Media DF

Media = pd.DataFrame(columns = ['Title', 'Details'])


newMedia1 = {'Title': 'Econ Twitter!', 'Details': 'If you\'re not already on Econ Twitter and have any interest in economics at all, then you should be! Econ twitter is a loosely defined community of economics professors, students, researchers, and enthusiast who tweet about cool new papers, issues in the field, economic policy, and lots of cats and dogs. A good place to get started on Econ Twitter is to follow these people:\n \n <div style="float: left; width: 50%;"><ul><li> <a href="https://twitter.com/causalinf?s=20">@causalinf </a></li><li><a href="https://twitter.com/leah_boustan?s=20">@leah_boustan </a></li><li><a href="https://twitter.com/jenniferdoleac?s=20">@jenniferdoleac</a></li><li><a href="https://twitter.com/JustinWolfers?s=20">@JustinWolfers </a></li><li><a href="https://twitter.com/graykimbrough?s=20">@graykimbrough </a></li><li><a href="https://twitter.com/ENPancotti?s=20">@ENPancotti </a></li>< li><a href="https://twitter.com/drlisadcook?s=20">@drlisadcook </a></li></ul></div><div style="float: right; width: 50%;"><ul><li><a href="https://twitter.com/JoshuaSGoodman?s=20">@JoshuaSGoodman </a></li><li><a href="https://twitter.com/dynarski?s=20">@dynarski </a></li><li><a href="https://twitter.com/Claudia_Sahm?s=20">@Claudia_Sahm </a></li><li><a href="https://twitter.com/pqblair?s=20">@pqblair </a></li><li><a href="https://twitter.com/amitabhchandra2?s=20">@amitabhchandra2</a></li><li><a href="https://twitter.com/Cutler_econ?s=20">@Cutler_econ</a></li>< li><a href="https://twitter.com/economeager?s=20">@economeager </a></li></ul></div> \n\n New members are embraced so feel free to start tweeting using #EconTwitter, but lurkers are more than welcome so don\'t be afraid to just follow and enjoy the community! If you want to learn more about Econ Twitter check out this [resource.]( https://medium.com/@mattclancy/a-beginners-guide-to-econtwitter-d237a3a4608b)'}
newMedia2 = {'Title': 'What an Economist Looks Like', 'Details': 'It is an open secret that women and underrepresented minorities face more significant roadblocks in economics than their peers. In this section, we highlight talented economists of diverse backgrounds to illustrate that the archetype of who can be an economist is outdated and irrelevant. What an Economist Looks Like is an Econ Twitter initiative that brings attention to economists who are changing the field and paving opportunities for future generations. \n\n This week, we\'re featuring Professor Monica Garica-Perez at St. Cloud State University. Professor Garcia-Perez is wrapping up her term as the 2020 president of the American Society of Hispanic Economists [ASHE](https://asheweb.org/) and is a board member of Hispanic Advocacy and Community Empowerment [HACER](https://hacer-mn.org/). Her research focuses on health, labor, and immigration. Follow her on [Twitter](https://twitter.com/econ_garcia?lang=en) or read more about her [here](https://web.stcloudstate.edu/migarciaperez/).'}
newMedia3 = {'Title': 'What We\'re Listening to This Week', 'Details': 'From Sports Direct warehouses to nail bars, awareness-raising campaigns warn that modern slavery is happening all around us. Over Christmas, fashion brand Boohoo cut ties with 64 garment suppliers in Leicester after it came out that factories were paying their workers as little as £3.50 an hour. And this month the foreign secretary said he would clamp down on companies who used forced labour in their supply chains. But how useful is the concept of ‘modern slavery’? What kinds of exploitation does it disguise? And what does it say about how we’ve designed our economy? For the first episode of a new series of the Weekly Economics Podcast, Ayeisha is joined by Emily Kenway to find out the truth about modern slavery.'}

newMedia = [newMedia1,
            newMedia2,
            newMedia3]

Media = Media.append(newMedia, ignore_index=True)





layout_TS = go.Layout(
    hovermode = 'closest', margin=dict(l=50, r=50, t=30, b=50))


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],)
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
    ],style={'display': 'inline-block', 'max-width': '600px', 'vertical-align': 'top'}),
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
    ],style={'display': 'inline-block', 'max-width': '100%', 'margin-top': '30px', 'float':'right'}),
        
         html.Div(children = [
        html.H4(jobs.iloc[1, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(jobs.iloc[1, 1])),
    ],style={'display': 'inline-block', 'max-width': '600px', 'vertical-align': 'top', 'float':'left'}),
        

    ],style={'margin-left': 'auto', 'margin-right': 'auto'}),
    dcc.Tab(label='Academic Opportunities', children=[
        
    html.Div(children = [
    html.H4(Academic.iloc[0, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(Academic.iloc[0, 1])),
    ],style={'display': 'inline-block', 'max-width': '600px', 'vertical-align': 'top'}),
    html.Div(children = [
       dcc.Graph(id = 'EduFig', figure = EduFig),
    ],style={'display': 'inline-block', 'max-width': '100%', 'min-width':'55%', 'float': 'right', 'margin-top': '30px'}),
        
    html.Div(children = [
        html.H4(Academic.iloc[1, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(Academic.iloc[1, 1])),
    ],style={'display': 'inline-block', 'max-width': '600px', 'vertical-align': 'top', 'float': 'left'}),
        
    ]),
    dcc.Tab(label='Student Resources', children=[
    html.Div(children = [
    html.H4(resources.iloc[0, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(resources.iloc[0, 1])),
    ],style={'display': 'inline-block', 'max-width': '600px'}),
        html.Div(children = [
        html.H4(),
        
    ],style={'display': 'inline-block','width':'100px','max-width': '600px','float': 'inherit'}),
    html.Div(children = [
        html.H4(resources.iloc[1, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(resources.iloc[1, 1])),
    ],style={'display': 'inline-block', 'max-width': '600px'}),
    html.Div(children = [
        html.H4(resources.iloc[2, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(resources.iloc[2, 1])),
        html.Iframe(height="315px", width="100%",  src="https://www.youtube.com/embed/kEevFRHiJFY"),
    ],style={'display': 'inline-block', 'max-width': '600px', 'float':'left'}),
    ],style={'margin-left': 'auto', 'margin-right': 'auto'}),
    dcc.Tab(label='Departmental Events', children=[
    
    html.Div(children = [
        html.H4(Department.iloc[0, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(Department.iloc[0, 1])),
    ],style={'display': 'inline-block', 'max-width': '600px', 'float': 'left'}),
        
       html.Div(children = [
        html.H4(),
        
    ],style={'display': 'inline-block','width':'100px','max-width': '600px','float': 'inherit'}),
        
        html.Div(children = [
        html.H4(Department.iloc[1, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(Department.iloc[1, 1])),
    ],style={'display': 'inline-block', 'max-width': '600px'}),
        
    ]),
        
        dcc.Tab(label='Media', children=[
    
      html.Div(children = [
html.H4(Media.iloc[0, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(dangerously_allow_html=True, children=Media.iloc[0, 1])),
    ],style={'display': 'inline-block', 'max-width': '600px', 'vertical-align': 'top'}),
            
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
                
                ], style={'display': 'inline-block', 'min-width': '50%', 'max-width': '100%', 'margin-top': '30px', 
                          'background-color': 'rgb(248, 248, 255)', 'padding-bottom': '5px', 'padding-left': '5px', 
                          'float': 'right'}),
       
            
        html.Div(children = [
        html.H4(Media.iloc[1, 0], style={'font-size': '16pt'}),
        html.Img(id='WhatAnEconLooksLike', src='https://kulogo.s3.us-east-2.amazonaws.com/Monica_Garcia-Perez.jpg', style={'width': '33%', 'float': 'left', 'margin-top': '5px', 'margin-right': '10px'}),
        html.P(dcc.Markdown(Media.iloc[1, 1])),
            
    ],style={'display': 'inline-block', 'max-width': '600px', 'vertical-align': 'top', 'float':'left', 'margin-top': '12px'}),
            
            html.Div(children = [
        html.H4(),
        
    ],style={'display': 'inline-block','width':'100px','max-width': '600px','float': 'inherit'}),
            
                    html.Div(children = [
        html.H4(Media.iloc[2, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(Media.iloc[2, 1])),           
        html.Iframe(height="200px", width="100%",  src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/975112759&color=ff5500"),
    ],style={'display': 'inline-block', 'max-width': '600px',   'margin-left': '9.7%'}),
        
            
    ]),
        
        
    dcc.Tab(label='Other', children=[
    
      html.Div(children = [
    html.H4('Economics\' Gender Problem', style={'font-size': '16pt'}),
        html.P(dcc.Markdown('Our field has always had a gender imbalance problem, but unlike other social sciences, economics has been closing the gender gap at an incredibly slow rate. The University of Kansas is not immune to these issues. In recent years, the KU economics faculty male/female ratio has grown to be more in line with the national economics average but compared to the average academic department we still fall far behind. Bias against women has an outsized negative influence on our profession both nationally and at KU. In 2019, the American Economic Association ([AEA]( chrome-extension://oemmndcbldboiebfnladdacbdfmadadm/https:/www.aeaweb.org/resources/member-docs/climate-survey-results-mar-18-2019)) surveyed over 9,000 current and former AEA members, finding roughly half of women respondents have experienced discrimination and nearly two-thirds feel their work is taken less seriously than their male counterparts. Female students often report harassment and discrimination, and female faculty face higher standards in their research and tend to be given worse student evaluations than male instructors. ([Boring, 2017]( https://doi.org/10.1016/j.jpubeco.2016.11.006))\n\nThe economics undergraduate committee is concerned with the gender disparities evident in our field and in our department at KU. We are working to combat these issues, and to begin to address other issues of gender discrimination that our trans and non-binary students may be facing. Specifically, this past year we have worked to increase mentoring efforts for undergraduate women, increase female representation, and introduce gender neutral bathrooms to Snow Hall. Committee leadership has completed KU Safe Space training so please feel comfortable reaching out with any questions or concerns you might have. ')),
    ],style={'display': 'inline-block', 'max-width': '600px', 'vertical-align': 'top'}),
        html.Div(children = [
       dcc.Graph(id = 'EconFac', figure = EconFacFig),
        ], style={'display': 'inline-block', 'max-width': '100%', 'min-width': '55%', 'margin-top': '30px', 'float':'right'}),
        

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
  
app.title = 'KU Econ Undergrad Resources'

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-15C7GNBCP3"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
        
          gtag('config', 'G-RX0YGPMQKW');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""
    
if __name__ == '__main__':
    app.run_server(debug=False)
