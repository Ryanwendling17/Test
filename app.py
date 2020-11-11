import pandas as pd
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import plotly.graph_objects as go
import numpy as np
import io
import plotly.figure_factory as ff

# ## Call Data and Format

# In[5]:


password = '8675309'

# Username of your GitHub account

username = 'Ryanwendling17'

# Personal Access Token (PAO) from your GitHub account

token = '68a815925ec38e2b318aa0f453ee225f8740194e'

# Creates a re-usable session object with your creds in-built

github_session = requests.Session()
github_session.auth = (username, token)



# Downloading the csv file from your GitHub
url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/Change_IBCCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

ChangeIBCCA = pd.read_csv(io.StringIO(download.decode('utf-8')))


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/Change_webtab_IBCCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

Change_webtabIBCCA = pd.read_csv(io.StringIO(download.decode('utf-8')))
Change_webtabIBCCA = Change_webtabIBCCA.rename(columns = {'Unnamed: 0': ''})


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/PercentChange_IBCCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

PercentChangeIBCCA = pd.read_csv(io.StringIO(download.decode('utf-8')))


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/PercentChange_webtab_IBCCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

PercentChange_webtabIBCCA = pd.read_csv(io.StringIO(download.decode('utf-8')))
PercentChange_webtabIBCCA = PercentChange_webtabIBCCA.rename(columns = {'Unnamed: 0': ''})


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/TS_IBCCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

stIBCCA = pd.read_csv(io.StringIO(download.decode('utf-8')))
del stIBCCA['Position']






# dropdown options
featuresIBCCA = stIBCCA.columns[1:-1]
optsIBCCA = [{'label' : i, 'value' : i} for i in featuresIBCCA]

stIBCCA['Date'] = pd.to_datetime(stIBCCA.Date)


datesIBCCA = pd.DataFrame()
datesIBCCA["Dates"] = stIBCCA['Date']
datesIBCCA["DOW"] = datesIBCCA["Dates"] - datesIBCCA["Dates"].dt.weekday * np.timedelta64(1, 'D')
dates2IBCCA = pd.DataFrame()
dates2IBCCA['DOW'] = datesIBCCA["DOW"]
dates2IBCCA = dates2IBCCA.drop_duplicates()
dates2IBCCA['DOW'] = dates2IBCCA['DOW'].astype(str)
datesIBCCA = dates2IBCCA['DOW'].tolist()


fig3_dfIBCCA = stIBCCA.copy()
rowsIBCCA = len(fig3_dfIBCCA.index)
fig3_dfIBCCA['Average Daily Calls'] = fig3_dfIBCCA['Calls'].sum() / rowsIBCCA
fig3_dfIBCCA['Average Daily Contacts'] = fig3_dfIBCCA['Contacts'].sum() / rowsIBCCA
fig3_dfIBCCA['Average Daily Contact Rate'] = fig3_dfIBCCA['Average Daily Contacts'] / fig3_dfIBCCA['Average Daily Calls']
fig3_dfIBCCA['Average Daily Unique Accounts Called'] = fig3_dfIBCCA['Unique Accounts Called'].sum() / rowsIBCCA
fig3_dfIBCCA['Average Daily Unique Accounts Contacted'] = fig3_dfIBCCA['Unique Accounts Contacted'].sum() / rowsIBCCA
fig3_dfIBCCA['Average Daily Account Contact Rate'] = fig3_dfIBCCA['Average Daily Unique Accounts Contacted'] / fig3_dfIBCCA['Average Daily Unique Accounts Called']
fig3_dfIBCCA['Average Daily Transfers'] = fig3_dfIBCCA['Transfers'].sum() / rowsIBCCA
fig3_dfIBCCA['Average Daily Call Transfer Rate'] = fig3_dfIBCCA['Average Daily Transfers'] / fig3_dfIBCCA['Average Daily Calls']
fig3_dfIBCCA['Average Daily Account Transfer Rate'] = fig3_dfIBCCA['Average Daily Transfers'] / fig3_dfIBCCA['Average Daily Unique Accounts Called']
fig3_dfIBCCA['Average Daily Enrollments'] = fig3_dfIBCCA['Enrollments'].sum() / rowsIBCCA
fig3_dfIBCCA.drop(fig3_dfIBCCA.columns[0:13], axis=1, inplace = True) 
fig3_dfIBCCA = fig3_dfIBCCA[:1]
fig3_dfIBCCA = fig3_dfIBCCA.round(decimals = 2)
fig3_dfIBCCA = fig3_dfIBCCA.T
fig3_dfIBCCA = fig3_dfIBCCA.rename(columns = {0: 'Over Selected Date Range'})
fig3_dfIBCCA.reset_index(drop = False, inplace = True)
fig3_dfIBCCA = fig3_dfIBCCA.rename(columns = {'index': ''})
figure3IBCCA = ff.create_table(fig3_dfIBCCA)


# Create a plotly figure
trace_1IBCCA = go.Scatter(x = stIBCCA.Date, y = stIBCCA['Calls'],
                    name = 'Calls',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))
layoutIBCCA = go.Layout(hovermode = 'closest', margin=dict(l=50, r=50, t=20, b=50))
figIBCCA = go.Figure(data = [trace_1IBCCA], layout = layoutIBCCA)





# Get a list of all the districts
metrics = PercentChange_webtabIBCCA[""].unique()



figureIBCCA = ff.create_table(PercentChange_webtabIBCCA)
figureIBCCA.layout.width = 800

figure2IBCCA = ff.create_table(Change_webtabIBCCA)
figure2IBCCA.layout.width = 800

# Downloading the csv file from your GitHub
url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/Change_AEPCCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

ChangeAEPCCA = pd.read_csv(io.StringIO(download.decode('utf-8')))


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/Change_webtab_AEPCCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

Change_webtabAEPCCA = pd.read_csv(io.StringIO(download.decode('utf-8')))
Change_webtabAEPCCA = Change_webtabAEPCCA.rename(columns = {'Unnamed: 0': ''})


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/PercentChange_AEPCCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

PercentChangeAEPCCA = pd.read_csv(io.StringIO(download.decode('utf-8')))


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/PercentChange_webtab_AEPCCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

PercentChange_webtabAEPCCA = pd.read_csv(io.StringIO(download.decode('utf-8')))
PercentChange_webtabAEPCCA = PercentChange_webtabAEPCCA.rename(columns = {'Unnamed: 0': ''})


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/TS_AEPCCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

stAEPCCA = pd.read_csv(io.StringIO(download.decode('utf-8')))
del stAEPCCA['Position']






# dropdown options
featuresAEPCCA = stAEPCCA.columns[1:-1]
optsAEPCCA = [{'label' : i, 'value' : i} for i in featuresAEPCCA]

stAEPCCA['Date'] = pd.to_datetime(stAEPCCA.Date)


datesAEPCCA = pd.DataFrame()
datesAEPCCA["Dates"] = stAEPCCA['Date']
datesAEPCCA["DOW"] = datesAEPCCA["Dates"] - datesAEPCCA["Dates"].dt.weekday * np.timedelta64(1, 'D')
dates2AEPCCA = pd.DataFrame()
dates2AEPCCA['DOW'] = datesAEPCCA["DOW"]
dates2AEPCCA = dates2AEPCCA.drop_duplicates()
dates2AEPCCA['DOW'] = dates2AEPCCA['DOW'].astype(str)
datesAEPCCA = dates2AEPCCA['DOW'].tolist()


fig3_dfAEPCCA = stAEPCCA.copy()
rowsAEPCCA = len(fig3_dfAEPCCA.index)
fig3_dfAEPCCA['Average Daily Calls'] = fig3_dfAEPCCA['Calls'].sum() / rowsAEPCCA
fig3_dfAEPCCA['Average Daily Contacts'] = fig3_dfAEPCCA['Contacts'].sum() / rowsAEPCCA
fig3_dfAEPCCA['Average Daily Contact Rate'] = fig3_dfAEPCCA['Average Daily Contacts'] / fig3_dfAEPCCA['Average Daily Calls']
fig3_dfAEPCCA['Average Daily Unique Accounts Called'] = fig3_dfAEPCCA['Unique Accounts Called'].sum() / rowsAEPCCA
fig3_dfAEPCCA['Average Daily Unique Accounts Contacted'] = fig3_dfAEPCCA['Unique Accounts Contacted'].sum() / rowsAEPCCA
fig3_dfAEPCCA['Average Daily Account Contact Rate'] = fig3_dfAEPCCA['Average Daily Unique Accounts Contacted'] / fig3_dfAEPCCA['Average Daily Unique Accounts Called']
fig3_dfAEPCCA['Average Daily Transfers'] = fig3_dfAEPCCA['Transfers'].sum() / rowsAEPCCA
fig3_dfAEPCCA['Average Daily Call Transfer Rate'] = fig3_dfAEPCCA['Average Daily Transfers'] / fig3_dfAEPCCA['Average Daily Calls']
fig3_dfAEPCCA['Average Daily Account Transfer Rate'] = fig3_dfAEPCCA['Average Daily Transfers'] / fig3_dfAEPCCA['Average Daily Unique Accounts Called']
fig3_dfAEPCCA['Average Daily Enrollments'] = fig3_dfAEPCCA['Enrollments'].sum() / rowsAEPCCA
fig3_dfAEPCCA.drop(fig3_dfAEPCCA.columns[0:13], axis=1, inplace = True) 
fig3_dfAEPCCA = fig3_dfAEPCCA[:1]
fig3_dfAEPCCA = fig3_dfAEPCCA.round(decimals = 2)
fig3_dfAEPCCA = fig3_dfAEPCCA.T
fig3_dfAEPCCA = fig3_dfAEPCCA.rename(columns = {0: 'Over Selected Date Range'})
fig3_dfAEPCCA.reset_index(drop = False, inplace = True)
fig3_dfAEPCCA = fig3_dfAEPCCA.rename(columns = {'index': ''})
figure3AEPCCA = ff.create_table(fig3_dfAEPCCA)


# Create a plotly figure
trace_1AEPCCA = go.Scatter(x = stAEPCCA.Date, y = stAEPCCA['Calls'],
                    name = 'Calls',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))
layoutAEPCCA = go.Layout(hovermode = 'closest', margin=dict(l=50, r=50, t=20, b=50))
figAEPCCA = go.Figure(data = [trace_1AEPCCA], layout = layoutAEPCCA)


figureAEPCCA = ff.create_table(PercentChange_webtabAEPCCA)
figureAEPCCA.layout.width = 800

figure2AEPCCA = ff.create_table(Change_webtabAEPCCA)
figure2AEPCCA.layout.width = 800
    
# Downloading the csv file from your GitHub
url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/Change_CCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

ChangeCCA = pd.read_csv(io.StringIO(download.decode('utf-8')))


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/Change_webtab_CCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

Change_webtabCCA = pd.read_csv(io.StringIO(download.decode('utf-8')))
Change_webtabCCA = Change_webtabCCA.rename(columns = {'Unnamed: 0': ''})


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/PercentChange_CCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

PercentChangeCCA = pd.read_csv(io.StringIO(download.decode('utf-8')))


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/PercentChange_webtab_CCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

PercentChange_webtabCCA = pd.read_csv(io.StringIO(download.decode('utf-8')))
PercentChange_webtabCCA = PercentChange_webtabCCA.rename(columns = {'Unnamed: 0': ''})


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/TS_CCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

stCCA = pd.read_csv(io.StringIO(download.decode('utf-8')))
del stCCA['Position']






# dropdown options
featuresCCA = stCCA.columns[1:-1]
optsCCA = [{'label' : i, 'value' : i} for i in featuresCCA]

stCCA['Date'] = pd.to_datetime(stCCA.Date)


datesCCA = pd.DataFrame()
datesCCA["Dates"] = stCCA['Date']
Yesterday = datesCCA["Dates"].astype(str).tolist()
datesCCA["DOW"] = datesCCA["Dates"] - datesCCA["Dates"].dt.weekday * np.timedelta64(1, 'D')
dates2CCA = pd.DataFrame()
dates2CCA['DOW'] = datesCCA["DOW"]
dates2CCA = dates2CCA.drop_duplicates()
dates2CCA['DOW'] = dates2CCA['DOW'].astype(str)
datesCCA = dates2CCA['DOW'].tolist()
yesterday = Yesterday[-1]


fig3_dfCCA = stCCA.copy()
rowsCCA = len(fig3_dfCCA.index)
fig3_dfCCA['Average Daily Calls'] = fig3_dfCCA['Calls'].sum() / rowsCCA
fig3_dfCCA['Average Daily Contacts'] = fig3_dfCCA['Contacts'].sum() / rowsCCA
fig3_dfCCA['Average Daily Contact Rate'] = fig3_dfCCA['Average Daily Contacts'] / fig3_dfCCA['Average Daily Calls']
fig3_dfCCA['Average Daily Unique Accounts Called'] = fig3_dfCCA['Unique Accounts Called'].sum() / rowsCCA
fig3_dfCCA['Average Daily Unique Accounts Contacted'] = fig3_dfCCA['Unique Accounts Contacted'].sum() / rowsCCA
fig3_dfCCA['Average Daily Account Contact Rate'] = fig3_dfCCA['Average Daily Unique Accounts Contacted'] / fig3_dfCCA['Average Daily Unique Accounts Called']
fig3_dfCCA['Average Daily Transfers'] = fig3_dfCCA['Transfers'].sum() / rowsCCA
fig3_dfCCA['Average Daily Call Transfer Rate'] = fig3_dfCCA['Average Daily Transfers'] / fig3_dfCCA['Average Daily Calls']
fig3_dfCCA['Average Daily Account Transfer Rate'] = fig3_dfCCA['Average Daily Transfers'] / fig3_dfCCA['Average Daily Unique Accounts Called']
fig3_dfCCA['Average Daily Enrollments'] = fig3_dfCCA['Enrollments'].sum() / rowsCCA
fig3_dfCCA.drop(fig3_dfCCA.columns[0:13], axis=1, inplace = True) 
fig3_dfCCA = fig3_dfCCA[:1]
fig3_dfCCA = fig3_dfCCA.round(decimals = 2)
fig3_dfCCA = fig3_dfCCA.T
fig3_dfCCA = fig3_dfCCA.rename(columns = {0: 'Over Selected Date Range'})
fig3_dfCCA.reset_index(drop = False, inplace = True)
fig3_dfCCA = fig3_dfCCA.rename(columns = {'index': ''})
figure3CCA = ff.create_table(fig3_dfCCA)


# Create a plotly figure
trace_1CCA = go.Scatter(x = stCCA.Date, y = stCCA['Calls'],
                    name = 'Calls',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))
layoutCCA = go.Layout(hovermode = 'closest', margin=dict(l=50, r=50, t=20, b=50))
figCCA = go.Figure(data = [trace_1CCA], layout = layoutCCA)



# In[6]:


def generate_table(dataframe, max_rows=12):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


# ## App Layout

# In[7]:


# Get a list of all the districts
metrics = PercentChange_webtabCCA[""].unique()



figureCCA = ff.create_table(PercentChange_webtabCCA)
figureCCA.layout.width = 800

figure2CCA = ff.create_table(Change_webtabCCA)
figure2CCA.layout.width = 800


# Create the app
VALID_USERNAME_PASSWORD_PAIRS = {
    'ryan.wendling@selectquote.com': password, 
    'david.cable@selectquote.com': password, 
    'terresha.dinkel@selectquote.com' : password
}


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# Populate the layout with HTML and graph components
app.layout = html.Div(children = [
    dcc.Tabs([
        dcc.Tab(label='CCA', children=[
    html.H2("CCA Performance Metrics", style={'font-size': '28pt'}),
   # generate_table(PercentChange_webtab),
    html.Br(),
                    # adding a plot
    html.H4("Time Series"),
    dcc.Graph(id = 'plotCCA', figure = figCCA),
    # dropdown
    html.P([
        html.Label("Choose a Metric"),
        dcc.Dropdown(id = 'optCCA', options = optsCCA,
                    value = optsCCA[0])
            ], style = {'width': '400px',
                        'fontSize' : '18px',
                        'padding-left' : '100px',
                        'display': 'inline-block'}),
    # range slider
    html.P([
        html.Label("Time Period"),
        dcc.RangeSlider(id = 'sliderCCA',
                        marks = {i : datesCCA[i] for i in range(0, len(datesCCA))},
                        min = 0,
                        max = len(datesCCA)-.5,
                        value = [1, len(datesCCA)])
            ], style = {'width' : '90%',
                        'fontSize' : '18px',
                        'padding-left' : '100px'}),
    html.Br(), html.Br(),
    html.H4("Daily Averages"),
    dcc.DatePickerRange(
        id='my-date-picker-rangeCCA',
        min_date_allowed=min(stCCA['Date']),
        max_date_allowed=max(stCCA['Date']),
        start_date=min(stCCA['Date']),
        end_date=max(stCCA['Date'])
    ),
    dcc.Graph(id='tableCCA', figure=figure3CCA),
    html.Br(), html.Br(),
    html.H4("Percent Change Relative to "+yesterday),
    html.Div(
        [
            dcc.Dropdown(
                id="METRICSCCA",
                options=[{
                    'label': i,
                    'value': i
                } for i in metrics],
                value='Calls'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    html.Div(children=[
        dcc.Graph(id='funnel-graphCCA', style={'display': 'inline-block'}),
        dcc.Graph(id='my-tableCCA', figure=figureCCA, style={'display': 'inline-block'})
    ])
    ,
    html.Br(), html.Br(),
    html.H4("Change Relative to "+yesterday),
    html.Div(
        [
            dcc.Dropdown(
                id="METRICS2CCA",
                options=[{
                    'label': i,
                    'value': i
                } for i in metrics],
                value='Calls'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    html.Div(children=[
        dcc.Graph(id='funnel-graph2CCA', style={'display': 'inline-block'}),
        dcc.Graph(id='my-table2CCA', figure=figure2CCA, style={'display': 'inline-block'})
    ])
    ,
                    ]),
        dcc.Tab(label='AEPCCA', children=[
    html.H2("AEPCCA Performance Metrics", style={'font-size': '28pt'}),
   # generate_table(PercentChange_webtab),
    html.Br(),
                    # adding a plot
    html.H4("Time Series"),
    dcc.Graph(id = 'plotAEPCCA', figure = figAEPCCA),
    # dropdown
    html.P([
        html.Label("Choose a Metric"),
        dcc.Dropdown(id = 'optAEPCCA', options = optsAEPCCA,
                    value = optsAEPCCA[0])
            ], style = {'width': '400px',
                        'fontSize' : '18px',
                        'padding-left' : '100px',
                        'display': 'inline-block'}),
    # range slider
    html.P([
        html.Label("Time Period"),
        dcc.RangeSlider(id = 'sliderAEPCCA',
                        marks = {i : datesAEPCCA[i] for i in range(0, len(datesAEPCCA))},
                        min = 0,
                        max = len(datesAEPCCA)-.5,
                        value = [1, len(datesAEPCCA)-1])
            ], style = {'width' : '90%',
                        'fontSize' : '18px',
                        'padding-left' : '100px'}),
    html.Br(), html.Br(),
    html.H4("Daily Averages"),
    dcc.DatePickerRange(
        id='my-date-picker-rangeAEPCCA',
        min_date_allowed=min(stAEPCCA['Date']),
        max_date_allowed=max(stAEPCCA['Date']),
        start_date=min(stAEPCCA['Date']),
        end_date=max(stAEPCCA['Date'])
    ),
    dcc.Graph(id='tableAEPCCA', figure=figure3AEPCCA),
    html.Br(), html.Br(),
    html.H4("Percent Change Relative to "+yesterday),
    html.Div(
        [
            dcc.Dropdown(
                id="METRICSAEPCCA",
                options=[{
                    'label': i,
                    'value': i
                } for i in metrics],
                value='Calls'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    html.Div(children=[
        dcc.Graph(id='funnel-graphAEPCCA', style={'display': 'inline-block'}),
        dcc.Graph(id='my-tableAEPCCA', figure=figureAEPCCA, style={'display': 'inline-block'})
    ])
    ,
    html.Br(), html.Br(),
    html.H4("Change Relative to "+yesterday),
    html.Div(
        [
            dcc.Dropdown(
                id="METRICS2AEPCCA",
                options=[{
                    'label': i,
                    'value': i
                } for i in metrics],
                value='Calls'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    html.Div(children=[
        dcc.Graph(id='funnel-graph2AEPCCA', style={'display': 'inline-block'}),
        dcc.Graph(id='my-table2AEPCCA', figure=figure2AEPCCA, style={'display': 'inline-block'})
    ])
    ,
                    ]),
            dcc.Tab(label='IBCCA', children=[
    html.H2("IBCCA Performance Metrics", style={'font-size': '28pt'}),
   # generate_table(PercentChange_webtab),
    html.Br(),
                    # adding a plot
    html.H4("Time Series"),
    dcc.Graph(id = 'plotIBCCA', figure = figIBCCA),
    # dropdown
    html.P([
        html.Label("Choose a Metric"),
        dcc.Dropdown(id = 'optIBCCA', options = optsIBCCA,
                    value = optsIBCCA[0])
            ], style = {'width': '400px',
                        'fontSize' : '18px',
                        'padding-left' : '100px',
                        'display': 'inline-block'}),
    # range slider
    html.P([
        html.Label("Time Period"),
        dcc.RangeSlider(id = 'sliderIBCCA',
                        marks = {i : datesIBCCA[i] for i in range(0, len(datesIBCCA))},
                        min = 0,
                        max = len(datesIBCCA)-.5,
                        value = [1, len(datesIBCCA)])
            ], style = {'width' : '90%',
                        'fontSize' : '18px',
                        'padding-left' : '100px'}),
    html.Br(), html.Br(),
    html.H4("Daily Averages"),
    dcc.DatePickerRange(
        id='my-date-picker-rangeIBCCA',
        min_date_allowed=min(stIBCCA['Date']),
        max_date_allowed=max(stIBCCA['Date']),
        start_date=min(stIBCCA['Date']),
        end_date=max(stIBCCA['Date'])
    ),
    dcc.Graph(id='tableIBCCA', figure=figure3IBCCA),
    html.Br(), html.Br(),
    html.H4("Percent Change Relative to "+yesterday),
    html.Div(
        [
            dcc.Dropdown(
                id="METRICSIBCCA",
                options=[{
                    'label': i,
                    'value': i
                } for i in metrics],
                value='Calls'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    html.Div(children=[
        dcc.Graph(id='funnel-graphIBCCA', style={'display': 'inline-block'}),
        dcc.Graph(id='my-tableIBCCA', figure=figureIBCCA, style={'display': 'inline-block'})
    ])
    ,
    html.Br(), html.Br(),
    html.H4("Change Relative to "+yesterday),
    html.Div(
        [
            dcc.Dropdown(
                id="METRICS2IBCCA",
                options=[{
                    'label': i,
                    'value': i
                } for i in metrics],
                value='Calls'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    html.Div(children=[
        dcc.Graph(id='funnel-graph2IBCCA', style={'display': 'inline-block'}),
        dcc.Graph(id='my-table2IBCCA', figure=figure2IBCCA, style={'display': 'inline-block'})
    ])
    ,
                    ]),

      ])
])


# ## Figure 1: Yesterday Compare to n

# In[ ]:


@app.callback(
    dash.dependencies.Output('funnel-graphCCA', 'figure'),
    [dash.dependencies.Input('METRICSCCA', 'value')])
def update_graph(Metrics):
    if Metrics == "Calls":
        trace = go.Bar(x=PercentChangeCCA ['index'], y=PercentChangeCCA [('Calls')], name='Calls')
    elif Metrics == "Contacts":
        trace = go.Bar(x=PercentChangeCCA ['index'], y=PercentChangeCCA [('Contacts')], name='Contacts')
    elif Metrics == "Contact Rate":
        trace = go.Bar(x=PercentChangeCCA ['index'], y=PercentChangeCCA [('Contact Rate')], name='Contact Rate')
    elif Metrics == "Unique Accounts Called":
        trace = go.Bar(x=PercentChangeCCA ['index'], y=PercentChangeCCA [('Unique Accounts Called')], name='Unique Accounts Called')
    elif Metrics == "Unique Accounts Contacted":   
        trace = go.Bar(x=PercentChangeCCA ['index'], y=PercentChangeCCA [('Unique Accounts Contacted')], name='Unique Accounts Contacted')
    elif Metrics == "Account Contact Rate":   
        trace = go.Bar(x=PercentChangeCCA ['index'], y=PercentChangeCCA [('Account Contact Rate')], name='Account Contact Rate')
    elif Metrics == "Transfers":  
        trace = go.Bar(x=PercentChangeCCA ['index'], y=PercentChangeCCA [('Transfers')], name='Transfers')
    elif Metrics == "Call Transfer Rate":  
        trace = go.Bar(x=PercentChangeCCA ['index'], y=PercentChangeCCA [('Call Transfer Rate')], name='Call Transfer Rate')
    elif Metrics == "Account Transfer Rate":
        trace = go.Bar(x=PercentChangeCCA ['index'], y=PercentChangeCCA [('Account Transfer Rate')], name='Account Transfer Rate')
    elif Metrics == "Enrollments":
        trace = go.Bar(x=PercentChangeCCA ['index'], y=PercentChangeCCA [('Enrollments')], name='Enrollments')
    elif Metrics == "Calls per 8 Hours":
        trace = go.Bar(x=PercentChangeCCA ['index'], y=PercentChangeCCA [('Calls per 8 Hours')], name='Calls per 8 Hours')
    elif Metrics == "Not Ready Time %":
        trace = go.Bar(x=PercentChangeCCA ['index'], y=PercentChangeCCA [('Not Ready Time %')], name='Not Ready Time %')


    return {
        'data': [trace],
        'layout':
        go.Layout(
            title='Percent Change in {}'.format(Metrics),
            xaxis = dict(title = yesterday+' Relative to:'),
            yaxis = dict(tickformat=".0%"),
          #  font_family="Times New Roman",
          #  paper_bgcolor='#000000',
            barmode='group')
    }



@app.callback(
    dash.dependencies.Output('funnel-graph2CCA', 'figure'),
    [dash.dependencies.Input('METRICS2CCA', 'value')])
def update_graph(Metrics):
    if Metrics == "Calls":
        trace2 = go.Bar(x=ChangeCCA ['index'], y=ChangeCCA [('Calls')], name='Calls')
    elif Metrics == "Contacts":
        trace2 = go.Bar(x=ChangeCCA ['index'], y=ChangeCCA [('Contacts')], name='Contacts')
    elif Metrics == "Contact Rate":
        trace2 = go.Bar(x=ChangeCCA ['index'], y=ChangeCCA [('Contact Rate')], name='Contact Rate')
    elif Metrics == "Unique Accounts Called":
        trace2 = go.Bar(x=ChangeCCA ['index'], y=ChangeCCA [('Unique Accounts Called')], name='Unique Accounts Called')
    elif Metrics == "Unique Accounts Contacted":   
        trace2 = go.Bar(x=ChangeCCA ['index'], y=ChangeCCA [('Unique Accounts Contacted')], name='Unique Accounts Contacted')
    elif Metrics == "Account Contact Rate":   
        trace2 = go.Bar(x=ChangeCCA ['index'], y=ChangeCCA [('Account Contact Rate')], name='Account Contact Rate')
    elif Metrics == "Transfers":  
        trace2 = go.Bar(x=ChangeCCA ['index'], y=ChangeCCA [('Transfers')], name='Transfers')
    elif Metrics == "Call Transfer Rate":  
        trace2 = go.Bar(x=ChangeCCA ['index'], y=ChangeCCA [('Call Transfer Rate')], name='Call Transfer Rate')
    elif Metrics == "Account Transfer Rate":
        trace2 = go.Bar(x=ChangeCCA ['index'], y=ChangeCCA [('Account Transfer Rate')], name='Account Transfer Rate')
    elif Metrics == "Enrollments":
        trace = go.Bar(x=ChangeCCA ['index'], y=ChangeCCA [('Enrollments')], name='Enrollments')
    elif Metrics == "Calls per 8 Hours":
        trace2 = go.Bar(x=ChangeCCA ['index'], y=ChangeCCA [('Calls per 8 Hours')], name='Calls per 8 Hours')
    elif Metrics == "Not Ready Time %":
        trace2 = go.Bar(x=ChangeCCA ['index'], y=ChangeCCA [('Not Ready Time %')], name='Not Ready Time %')


    return {
        'data': [trace2],
        'layout':
        go.Layout(
            title='Change in {}'.format(Metrics),
            xaxis = dict(title = yesterday+' Relative to:'),
            #yaxis = dict(tickformat=".0%"),
          #  font_family="Times New Roman",
          #  paper_bgcolor='#000000',
            barmode='group')
    }



#Add callback functions
@app.callback(Output('plotCCA', 'figure'),
             [Input('optCCA', 'value'),
             Input('sliderCCA', 'value')])
def update_figure(input1, input2):
    # filtering the data
    st2 = stCCA[(stCCA.Date > datesCCA[input2[0]]) & (stCCA.Date <= datesCCA[input2[1]])]
    # updating the plot
    trace_1 = go.Scatter(x = st2.Date, y = st2['Calls'],
                        name = 'Calls',
                        line = dict(width = 2,
                                    color = 'rgb(229, 151, 50)'))
    trace_2 = go.Scatter(x = st2.Date, y = st2[input1],
                        name = input1,
                        line = dict(width = 2,
                                    color = 'rgb(106, 181, 135)'))
    figCCA = go.Figure(data = [trace_2], layout = layoutCCA)
    return figCCA
  

@app.callback(
    dash.dependencies.Output('tableCCA', 'figure'),
    [dash.dependencies.Input('my-date-picker-rangeCCA', 'start_date'),
     dash.dependencies.Input('my-date-picker-rangeCCA', 'end_date')])
def update_table(start_date, end_date):
    df = stCCA[(stCCA.Date >= start_date) & (stCCA.Date <= end_date)]
    df.reset_index(drop = True, inplace = True)
    fig3_df = df.copy()
    rows = len(fig3_df.index)
    fig3_df['Average Daily Calls'] = fig3_df['Calls'].sum() / rowsCCA
    fig3_df['Average Daily Contacts'] = fig3_df['Contacts'].sum() / rowsCCA
    fig3_df['Average Daily Contact Rate'] = fig3_df['Average Daily Contacts'] / fig3_df['Average Daily Calls']
    fig3_df['Average Daily Unique Accounts Called'] = fig3_df['Unique Accounts Called'].sum() / rowsCCA
    fig3_df['Average Daily Unique Accounts Contacted'] = fig3_df['Unique Accounts Contacted'].sum() / rowsCCA
    fig3_df['Average Daily Account Contact Rate'] = fig3_df['Average Daily Unique Accounts Contacted'] / fig3_df['Average Daily Unique Accounts Called']
    fig3_df['Average Daily Transfers'] = fig3_df['Transfers'].sum() / rowsCCA
    fig3_df['Average Daily Call Transfer Rate'] = fig3_df['Average Daily Transfers'] / fig3_df['Average Daily Calls']
    fig3_df['Average Daily Account Transfer Rate'] = fig3_df['Average Daily Transfers'] / fig3_df['Average Daily Unique Accounts Called']
    fig3_df['Average Daily Enrollments'] = fig3_df['Enrollments'].sum() / rowsCCA
    fig3_df.drop(fig3_df.columns[0:13], axis=1, inplace = True) 
    fig3_df = fig3_df[:1]
    fig3_df = fig3_df.round(decimals = 2)
    fig3_df = fig3_df.T
    fig3_df = fig3_df.rename(columns = {0: 'Over Selected Date Range'})
    fig3_df.reset_index(drop = False, inplace = True)
    fig3_df = fig3_df.rename(columns = {'index': ''})
    figure3CCA = ff.create_table(fig3_df)
    return figure3CCA
    
    
@app.callback(
    dash.dependencies.Output('funnel-graphAEPCCA', 'figure'),
    [dash.dependencies.Input('METRICSAEPCCA', 'value')])
def update_graph(Metrics):
    if Metrics == "Calls":
        trace = go.Bar(x=PercentChangeAEPCCA ['index'], y=PercentChangeAEPCCA [('Calls')], name='Calls')
    elif Metrics == "Contacts":
        trace = go.Bar(x=PercentChangeAEPCCA ['index'], y=PercentChangeAEPCCA [('Contacts')], name='Contacts')
    elif Metrics == "Contact Rate":
        trace = go.Bar(x=PercentChangeAEPCCA ['index'], y=PercentChangeAEPCCA [('Contact Rate')], name='Contact Rate')
    elif Metrics == "Unique Accounts Called":
        trace = go.Bar(x=PercentChangeAEPCCA ['index'], y=PercentChangeAEPCCA [('Unique Accounts Called')], name='Unique Accounts Called')
    elif Metrics == "Unique Accounts Contacted":   
        trace = go.Bar(x=PercentChangeAEPCCA ['index'], y=PercentChangeAEPCCA [('Unique Accounts Contacted')], name='Unique Accounts Contacted')
    elif Metrics == "Account Contact Rate":   
        trace = go.Bar(x=PercentChangeAEPCCA ['index'], y=PercentChangeAEPCCA [('Account Contact Rate')], name='Account Contact Rate')
    elif Metrics == "Transfers":  
        trace = go.Bar(x=PercentChangeAEPCCA ['index'], y=PercentChangeAEPCCA [('Transfers')], name='Transfers')
    elif Metrics == "Call Transfer Rate":  
        trace = go.Bar(x=PercentChangeAEPCCA ['index'], y=PercentChangeAEPCCA [('Call Transfer Rate')], name='Call Transfer Rate')
    elif Metrics == "Account Transfer Rate":
        trace = go.Bar(x=PercentChangeAEPCCA ['index'], y=PercentChangeAEPCCA [('Account Transfer Rate')], name='Account Transfer Rate')
    elif Metrics == "Enrollments":
        trace = go.Bar(x=PercentChangeAEPCCA ['index'], y=PercentChangeAEPCCA [('Enrollments')], name='Enrollments')
    elif Metrics == "Calls per 8 Hours":
        trace = go.Bar(x=PercentChangeAEPCCA ['index'], y=PercentChangeAEPCCA [('Calls per 8 Hours')], name='Calls per 8 Hours')
    elif Metrics == "Not Ready Time %":
        trace = go.Bar(x=PercentChangeAEPCCA ['index'], y=PercentChangeAEPCCA [('Not Ready Time %')], name='Not Ready Time %')


    return {
        'data': [trace],
        'layout':
        go.Layout(
            title='Percent Change in {}'.format(Metrics),
            xaxis = dict(title = yesterday+' Relative to:'),
            yaxis = dict(tickformat=".0%"),
          #  font_family="Times New Roman",
          #  paper_bgcolor='#000000',
            barmode='group')
    }



@app.callback(
    dash.dependencies.Output('funnel-graph2AEPCCA', 'figure'),
    [dash.dependencies.Input('METRICS2AEPCCA', 'value')])
def update_graph(Metrics):
    if Metrics == "Calls":
        trace2 = go.Bar(x=ChangeAEPCCA ['index'], y=ChangeAEPCCA [('Calls')], name='Calls')
    elif Metrics == "Contacts":
        trace2 = go.Bar(x=ChangeAEPCCA ['index'], y=ChangeAEPCCA [('Contacts')], name='Contacts')
    elif Metrics == "Contact Rate":
        trace2 = go.Bar(x=ChangeAEPCCA ['index'], y=ChangeAEPCCA [('Contact Rate')], name='Contact Rate')
    elif Metrics == "Unique Accounts Called":
        trace2 = go.Bar(x=ChangeAEPCCA ['index'], y=ChangeAEPCCA [('Unique Accounts Called')], name='Unique Accounts Called')
    elif Metrics == "Unique Accounts Contacted":   
        trace2 = go.Bar(x=ChangeAEPCCA ['index'], y=ChangeAEPCCA [('Unique Accounts Contacted')], name='Unique Accounts Contacted')
    elif Metrics == "Account Contact Rate":   
        trace2 = go.Bar(x=ChangeAEPCCA ['index'], y=ChangeAEPCCA [('Account Contact Rate')], name='Account Contact Rate')
    elif Metrics == "Transfers":  
        trace2 = go.Bar(x=ChangeAEPCCA ['index'], y=ChangeAEPCCA [('Transfers')], name='Transfers')
    elif Metrics == "Call Transfer Rate":  
        trace2 = go.Bar(x=ChangeAEPCCA ['index'], y=ChangeAEPCCA [('Call Transfer Rate')], name='Call Transfer Rate')
    elif Metrics == "Account Transfer Rate":
        trace2 = go.Bar(x=ChangeAEPCCA ['index'], y=ChangeAEPCCA [('Account Transfer Rate')], name='Account Transfer Rate')
    elif Metrics == "Enrollments":
        trace = go.Bar(x=ChangeAEPCCA ['index'], y=ChangeAEPCCA [('Enrollments')], name='Enrollments')
    elif Metrics == "Calls per 8 Hours":
        trace2 = go.Bar(x=ChangeAEPCCA ['index'], y=ChangeAEPCCA [('Calls per 8 Hours')], name='Calls per 8 Hours')
    elif Metrics == "Not Ready Time %":
        trace2 = go.Bar(x=ChangeAEPCCA ['index'], y=ChangeAEPCCA [('Not Ready Time %')], name='Not Ready Time %')


    return {
        'data': [trace2],
        'layout':
        go.Layout(
            title='Change in {}'.format(Metrics),
            xaxis = dict(title = yesterday+' Relative to:'),
            #yaxis = dict(tickformat=".0%"),
          #  font_family="Times New Roman",
          #  paper_bgcolor='#000000',
            barmode='group')
    }



#Add callback functions
@app.callback(Output('plotAEPCCA', 'figure'),
             [Input('optAEPCCA', 'value'),
             Input('sliderAEPCCA', 'value')])
def update_figure(input1, input2):
    # filtering the data
    st2 = stAEPCCA[(stAEPCCA.Date > datesAEPCCA[input2[0]]) & (stAEPCCA.Date <= datesAEPCCA[input2[1]])]
    # updating the plot
    trace_1 = go.Scatter(x = st2.Date, y = st2['Calls'],
                        name = 'Calls',
                        line = dict(width = 2,
                                    color = 'rgb(229, 151, 50)'))
    trace_2 = go.Scatter(x = st2.Date, y = st2[input1],
                        name = input1,
                        line = dict(width = 2,
                                    color = 'rgb(106, 181, 135)'))
    figAEPCCA = go.Figure(data = [trace_2], layout = layoutAEPCCA)
    return figAEPCCA
  

@app.callback(
    dash.dependencies.Output('tableAEPCCA', 'figure'),
    [dash.dependencies.Input('my-date-picker-rangeAEPCCA', 'start_date'),
     dash.dependencies.Input('my-date-picker-rangeAEPCCA', 'end_date')])
def update_table(start_date, end_date):
    df = stAEPCCA[(stAEPCCA.Date >= start_date) & (stAEPCCA.Date <= end_date)]
    df.reset_index(drop = True, inplace = True)
    fig3_df = df.copy()
    rows = len(fig3_df.index)
    fig3_df['Average Daily Calls'] = fig3_df['Calls'].sum() / rowsAEPCCA
    fig3_df['Average Daily Contacts'] = fig3_df['Contacts'].sum() / rowsAEPCCA
    fig3_df['Average Daily Contact Rate'] = fig3_df['Average Daily Contacts'] / fig3_df['Average Daily Calls']
    fig3_df['Average Daily Unique Accounts Called'] = fig3_df['Unique Accounts Called'].sum() / rowsAEPCCA
    fig3_df['Average Daily Unique Accounts Contacted'] = fig3_df['Unique Accounts Contacted'].sum() / rowsAEPCCA
    fig3_df['Average Daily Account Contact Rate'] = fig3_df['Average Daily Unique Accounts Contacted'] / fig3_df['Average Daily Unique Accounts Called']
    fig3_df['Average Daily Transfers'] = fig3_df['Transfers'].sum() / rowsAEPCCA
    fig3_df['Average Daily Call Transfer Rate'] = fig3_df['Average Daily Transfers'] / fig3_df['Average Daily Calls']
    fig3_df['Average Daily Account Transfer Rate'] = fig3_df['Average Daily Transfers'] / fig3_df['Average Daily Unique Accounts Called']
    fig3_df['Average Daily Enrollments'] = fig3_df['Enrollments'].sum() / rowsAEPCCA
    fig3_df.drop(fig3_df.columns[0:13], axis=1, inplace = True) 
    fig3_df = fig3_df[:1]
    fig3_df = fig3_df.round(decimals = 2)
    fig3_df = fig3_df.T
    fig3_df = fig3_df.rename(columns = {0: 'Over Selected Date Range'})
    fig3_df.reset_index(drop = False, inplace = True)
    fig3_df = fig3_df.rename(columns = {'index': ''})
    figure3AEPCCA = ff.create_table(fig3_df)
    return figure3AEPCCA

@app.callback(
    dash.dependencies.Output('funnel-graphIBCCA', 'figure'),
    [dash.dependencies.Input('METRICSIBCCA', 'value')])
def update_graph(Metrics):
    if Metrics == "Calls":
        trace = go.Bar(x=PercentChangeIBCCA ['index'], y=PercentChangeIBCCA [('Calls')], name='Calls')
    elif Metrics == "Contacts":
        trace = go.Bar(x=PercentChangeIBCCA ['index'], y=PercentChangeIBCCA [('Contacts')], name='Contacts')
    elif Metrics == "Contact Rate":
        trace = go.Bar(x=PercentChangeIBCCA ['index'], y=PercentChangeIBCCA [('Contact Rate')], name='Contact Rate')
    elif Metrics == "Unique Accounts Called":
        trace = go.Bar(x=PercentChangeIBCCA ['index'], y=PercentChangeIBCCA [('Unique Accounts Called')], name='Unique Accounts Called')
    elif Metrics == "Unique Accounts Contacted":   
        trace = go.Bar(x=PercentChangeIBCCA ['index'], y=PercentChangeIBCCA [('Unique Accounts Contacted')], name='Unique Accounts Contacted')
    elif Metrics == "Account Contact Rate":   
        trace = go.Bar(x=PercentChangeIBCCA ['index'], y=PercentChangeIBCCA [('Account Contact Rate')], name='Account Contact Rate')
    elif Metrics == "Transfers":  
        trace = go.Bar(x=PercentChangeIBCCA ['index'], y=PercentChangeIBCCA [('Transfers')], name='Transfers')
    elif Metrics == "Call Transfer Rate":  
        trace = go.Bar(x=PercentChangeIBCCA ['index'], y=PercentChangeIBCCA [('Call Transfer Rate')], name='Call Transfer Rate')
    elif Metrics == "Account Transfer Rate":
        trace = go.Bar(x=PercentChangeIBCCA ['index'], y=PercentChangeIBCCA [('Account Transfer Rate')], name='Account Transfer Rate')
    elif Metrics == "Enrollments":
        trace = go.Bar(x=PercentChangeIBCCA ['index'], y=PercentChangeIBCCA [('Enrollments')], name='Enrollments')
    elif Metrics == "Calls per 8 Hours":
        trace = go.Bar(x=PercentChangeIBCCA ['index'], y=PercentChangeIBCCA [('Calls per 8 Hours')], name='Calls per 8 Hours')
    elif Metrics == "Not Ready Time %":
        trace = go.Bar(x=PercentChangeIBCCA ['index'], y=PercentChangeIBCCA [('Not Ready Time %')], name='Not Ready Time %')


    return {
        'data': [trace],
        'layout':
        go.Layout(
            title='Percent Change in {}'.format(Metrics),
            xaxis = dict(title = yesterday+' Relative to:'),
            yaxis = dict(tickformat=".0%"),
          #  font_family="Times New Roman",
          #  paper_bgcolor='#000000',
            barmode='group')
    }



@app.callback(
    dash.dependencies.Output('funnel-graph2IBCCA', 'figure'),
    [dash.dependencies.Input('METRICS2IBCCA', 'value')])
def update_graph(Metrics):
    if Metrics == "Calls":
        trace2 = go.Bar(x=ChangeIBCCA ['index'], y=ChangeIBCCA [('Calls')], name='Calls')
    elif Metrics == "Contacts":
        trace2 = go.Bar(x=ChangeIBCCA ['index'], y=ChangeIBCCA [('Contacts')], name='Contacts')
    elif Metrics == "Contact Rate":
        trace2 = go.Bar(x=ChangeIBCCA ['index'], y=ChangeIBCCA [('Contact Rate')], name='Contact Rate')
    elif Metrics == "Unique Accounts Called":
        trace2 = go.Bar(x=ChangeIBCCA ['index'], y=ChangeIBCCA [('Unique Accounts Called')], name='Unique Accounts Called')
    elif Metrics == "Unique Accounts Contacted":   
        trace2 = go.Bar(x=ChangeIBCCA ['index'], y=ChangeIBCCA [('Unique Accounts Contacted')], name='Unique Accounts Contacted')
    elif Metrics == "Account Contact Rate":   
        trace2 = go.Bar(x=ChangeIBCCA ['index'], y=ChangeIBCCA [('Account Contact Rate')], name='Account Contact Rate')
    elif Metrics == "Transfers":  
        trace2 = go.Bar(x=ChangeIBCCA ['index'], y=ChangeIBCCA [('Transfers')], name='Transfers')
    elif Metrics == "Call Transfer Rate":  
        trace2 = go.Bar(x=ChangeIBCCA ['index'], y=ChangeIBCCA [('Call Transfer Rate')], name='Call Transfer Rate')
    elif Metrics == "Account Transfer Rate":
        trace2 = go.Bar(x=ChangeIBCCA ['index'], y=ChangeIBCCA [('Account Transfer Rate')], name='Account Transfer Rate')
    elif Metrics == "Enrollments":
        trace = go.Bar(x=ChangeIBCCA ['index'], y=ChangeIBCCA [('Enrollments')], name='Enrollments')
    elif Metrics == "Calls per 8 Hours":
        trace2 = go.Bar(x=ChangeIBCCA ['index'], y=ChangeIBCCA [('Calls per 8 Hours')], name='Calls per 8 Hours')
    elif Metrics == "Not Ready Time %":
        trace2 = go.Bar(x=ChangeIBCCA ['index'], y=ChangeIBCCA [('Not Ready Time %')], name='Not Ready Time %')


    return {
        'data': [trace2],
        'layout':
        go.Layout(
            title='Change in {}'.format(Metrics),
            xaxis = dict(title = yesterday+' Relative to:'),
            #yaxis = dict(tickformat=".0%"),
          #  font_family="Times New Roman",
          #  paper_bgcolor='#000000',
            barmode='group')
    }



#Add callback functions
@app.callback(Output('plotIBCCA', 'figure'),
             [Input('optIBCCA', 'value'),
             Input('sliderIBCCA', 'value')])
def update_figure(input1, input2):
    # filtering the data
    st2 = stIBCCA[(stIBCCA.Date > datesIBCCA[input2[0]]) & (stIBCCA.Date <= datesIBCCA[input2[1]])]
    # updating the plot
    trace_1 = go.Scatter(x = st2.Date, y = st2['Calls'],
                        name = 'Calls',
                        line = dict(width = 2,
                                    color = 'rgb(229, 151, 50)'))
    trace_2 = go.Scatter(x = st2.Date, y = st2[input1],
                        name = input1,
                        line = dict(width = 2,
                                    color = 'rgb(106, 181, 135)'))
    figIBCCA = go.Figure(data = [trace_2], layout = layoutIBCCA)
    return figIBCCA
  

@app.callback(
    dash.dependencies.Output('tableIBCCA', 'figure'),
    [dash.dependencies.Input('my-date-picker-rangeIBCCA', 'start_date'),
     dash.dependencies.Input('my-date-picker-rangeIBCCA', 'end_date')])
def update_table(start_date, end_date):
    df = stIBCCA[(stIBCCA.Date >= start_date) & (stIBCCA.Date <= end_date)]
    df.reset_index(drop = True, inplace = True)
    fig3_df = df.copy()
    rows = len(fig3_df.index)
    fig3_df['Average Daily Calls'] = fig3_df['Calls'].sum() / rowsIBCCA
    fig3_df['Average Daily Contacts'] = fig3_df['Contacts'].sum() / rowsIBCCA
    fig3_df['Average Daily Contact Rate'] = fig3_df['Average Daily Contacts'] / fig3_df['Average Daily Calls']
    fig3_df['Average Daily Unique Accounts Called'] = fig3_df['Unique Accounts Called'].sum() / rowsIBCCA
    fig3_df['Average Daily Unique Accounts Contacted'] = fig3_df['Unique Accounts Contacted'].sum() / rowsIBCCA
    fig3_df['Average Daily Account Contact Rate'] = fig3_df['Average Daily Unique Accounts Contacted'] / fig3_df['Average Daily Unique Accounts Called']
    fig3_df['Average Daily Transfers'] = fig3_df['Transfers'].sum() / rowsIBCCA
    fig3_df['Average Daily Call Transfer Rate'] = fig3_df['Average Daily Transfers'] / fig3_df['Average Daily Calls']
    fig3_df['Average Daily Account Transfer Rate'] = fig3_df['Average Daily Transfers'] / fig3_df['Average Daily Unique Accounts Called']
    fig3_df['Average Daily Enrollments'] = fig3_df['Enrollments'].sum() / rowsIBCCA
    fig3_df.drop(fig3_df.columns[0:13], axis=1, inplace = True) 
    fig3_df = fig3_df[:1]
    fig3_df = fig3_df.round(decimals = 2)
    fig3_df = fig3_df.T
    fig3_df = fig3_df.rename(columns = {0: 'Over Selected Date Range'})
    fig3_df.reset_index(drop = False, inplace = True)
    fig3_df = fig3_df.rename(columns = {'index': ''})
    figure3IBCCA = ff.create_table(fig3_df)
    return figure3IBCCA

    
if __name__ == '__main__':
    app.run_server(debug=False)
