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





#Student Resources DF

resources = pd.DataFrame(columns = ['Title', 'Details'])


newResources1 = {'Title': 'Professor Slusky\'s Office Hours', 'Details': 'Professor Slusky is the director of undergraduate studies in the economics department. Feel free to drop by his office hours this semester via Zoom if you have any questions about the economics program. You can access his office hours via [link](http://kansas.zoom.us/my/davidslusky) on Tuesdays from 2-4 pm and on Thursdays from 9-11 am. (Password: 1115)'}
newResources2 = {'Title': 'Ryan Wendling\'s Office Hours', 'Details': 'Ryan is a senior economics student who works for Professor Slusky. He is also available via Zoom this semester to answer any questions you may have about the economics department. You can access his office hours via this [link](https://kansas.zoom.us/j/96482325564) on Mondays and Fridays from 3-5 pm. (Password: 102891)'}
newResources3 = {'Title': 'Stata Webinar: Creating customized reports in Word, Excel, and PDF', 'Details': 'Join Gabriela Ortiz, Applied Statistician, as she demonstrates how to create Word documents with Stata summary statistics, regression tables, and graphs. Find out how to interact Stata\'s features with Word\'s features and how to automate your work when you want to regularly update reports. You will also see how easy it is to use putpdf and putexcel to similarly create reproducible reports in PDF and Excel formats. Register for this free event [here](https://www.stata.com/training/webinar/reproducible-reporting-putdocx/).'}

newResources = [newResources1,
                newResources2,
                newResources3]

resources = resources.append(newResources, ignore_index=True)




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
    margin=dict(l=100, r=20, t=70, b=70),
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
                        x=-0.2, y=-0.109,
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
    ],style={'display': 'inline-block', 'width': '40%', 'margin-left': '100px', 'margin-top': '30px'}),
        
         html.Div(children = [
        html.H4(jobs.iloc[1, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(jobs.iloc[1, 1])),
    ],style={'display': 'inline-block', 'width': '40%', 'vertical-align': 'top', 'margin-top': '-21.5%'}),
        
    ],style={'margin-left': 'auto', 'margin-right': 'auto'}),
    dcc.Tab(label='Academic Opportunities', children=[
        
    html.Div(children = [
    html.H4(jobs.iloc[0, 0], style={'font-size': '16pt'}),
        html.P(dcc.Markdown(jobs.iloc[0, 1])),
    ],style={'display': 'inline-block', 'width': '40%', 'vertical-align': 'top'}),
    html.Div(children = [
       dcc.Graph(id = 'EduFig', figure = EduFig),
    ],style={'display': 'inline-block', 'width': '50%', 'margin-left': '100px', 'margin-top': '30px'}),
        
        
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
    html.H4("Undergraduate Resources4", style={'font-size': '16pt'}),
    ]),
    dcc.Tab(label='Other', children=[
    html.H4("Undergraduate Resources5", style={'font-size': '16pt'}),
    ]),]),
    
    
      ])





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
  


    
if __name__ == '__main__':
    app.run_server(debug=False)
