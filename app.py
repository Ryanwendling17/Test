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
        data.rename(columns={"index": "Date", 0: "UR"}, inplace = True)
        data['State'] = state
        stateUR = stateUR.append(data, ignore_index=True)
    except:
        pass

datesCCA = stateUR['Date'].unique().tolist()


KS = stateUR[stateUR['State'] == 'KS'] 
trace_1CCA = go.Scatter(x = KS.Date, y = KS['UR'],
                    name = 'KS Unemployment Rate',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))
layoutCCA = go.Layout(hovermode = 'closest', margin=dict(l=50, r=50, t=20, b=50))
figCCA = go.Figure(data = [trace_1CCA], layout = layoutCCA)
layout_TS = go.Layout(
                      yaxis=dict(
    title=dict(
      text='Unemployement Rate'
    )
  ),
    hovermode = 'closest', margin=dict(l=50, r=50, t=20, b=50))


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

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
    html.H4("Professor Slusky’s Office Hours", style={'font-size': '16pt'}),
        html.P('Professor Slusky is the director of undergraduate studies in the economics department. Feel free to drop by his office hours this semester via Zoom if you have any questions about the economics program. You can access his office hours via this link on Tuesdays from 2-4 pm and on Thursdays from 9-11 am. (Password: 1115)'),
    ],style={'display': 'inline-block', 'width': '40%', 'vertical-align': 'top'}),
    html.Div(children = [
       dcc.Graph(id = 'PlayerComWeek'),
    # dropdown
        html.Div(children = [
            html.Label("State 1"),
            html.Label("State 2")
        ], style={'width':'100%',
                 'display': 'inline-flex'}),
        html.Div(
        [
            dcc.Dropdown(
                id="MyPick",
                options=[{
                    'label': i,
                    'value': i
                } for i in states],
                value="KS"),
            
            dcc.Dropdown(
                id="Counterfactual",
                options=[{
                    'label': i,
                    'value': i
                } for i in states],
                value=states[1]),
        ],
        style={'width': '100%',
               'margin-right':'20%',
               'display': 'inline-flex'}),
    
                   
    # range slider
    #html.P([
    #    html.Label("Time Period"),
    #    dcc.RangeSlider(id = 'sliderCCA',
    #                    marks = {i : datesCCA[i] for i in range(0, len(datesCCA))},
    #                    min = 0,
    #                    max = len(datesCCA),
    #                    value = [1, len(datesCCA)])
     #       ], style = {'width' : '90%',
    #                    'fontSize' : '18px',
    #                    'padding-left' : '100px'}),
    ],style={'display': 'inline-block', 'width': '40%', 'margin-left': '100px'}),
    ],style={'margin-left': 'auto', 'margin-right': 'auto'}),
    dcc.Tab(label='Academic Opportunities', children=[
    html.H4("Undergraduate Resources2", style={'font-size': '16pt'}),
    ]),
    dcc.Tab(label='Student Resources', children=[
    html.Div(children = [
    html.H4("Professor Slusky’s Office Hours", style={'font-size': '16pt'}),
        html.P('Professor Slusky is the director of undergraduate studies in the economics department. Feel free to drop by his office hours this semester via Zoom if you have any questions about the economics program. You can access his office hours via this link on Tuesdays from 2-4 pm and on Thursdays from 9-11 am. (Password: 1115)'),
    ],style={'display': 'inline-block', 'width': '40%'}),
    html.Div(children = [
        html.H4("Ryan Wendling’s Office Hours", style={'font-size': '16pt'}),
        html.P('Ryan is a senior economics student who works for Professor Slusky. He is also available via Zoom this semester to answer any questions you may have about the economics department. You can access his office hours via this link on Mondays and Fridays from 3-5 pm.  (Password: 102891)'),
    ],style={'display': 'inline-block', 'width': '40%', 'margin-left': '100px'}),
    html.Div(children = [
        html.H4("Stata Webinar: Creating customized reports in Word, Excel, and PDF", style={'font-size': '16pt'}),
        html.P('Join Gabriela Ortiz, Applied Statistician, as she demonstrates how to create Word documents with Stata summary statistics, regression tables, and graphs. Find out how to interact Stata\'s features with Word\'s features and how to automate your work when you want to regularly update reports. You will also see how easy it is to use putpdf and putexcel to similarly create reproducible reports in PDF and Excel formats. Register for this free event here.'),
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
             Input('Counterfactual', 'value')])
def update_figure(input1, input2):
    # filtering the data
    data1 = stateUR[stateUR.State == input1]
    data2 = stateUR[stateUR.State == input2]
    # updating the plot
    trace_1 = go.Scatter(x = data1.Date, y = data1["UR"],
                        name = input1,
                        line = dict(width = 2,
                                    color = 'rgb(229, 151, 50)'))
    trace_2 = go.Scatter(x = data2.Date, y = data2["UR"],
                        name = input2,
                        line = dict(width = 2,
                                    color = 'rgb(106, 181, 135)'))
    figCCA = go.Figure(data = [trace_1, trace_2], layout = layout_TS)
    return figCCA
  


    
if __name__ == '__main__':
    app.run_server(debug=False)
