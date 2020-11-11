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
url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/Change_CCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

Change = pd.read_csv(io.StringIO(download.decode('utf-8')))


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/Change_webtab_CCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

Change_webtab = pd.read_csv(io.StringIO(download.decode('utf-8')))
Change_webtab = Change_webtab.rename(columns = {'Unnamed: 0': ''})


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/PercentChange_CCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

PercentChange = pd.read_csv(io.StringIO(download.decode('utf-8')))


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/PercentChange_webtab_CCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

PercentChange_webtab = pd.read_csv(io.StringIO(download.decode('utf-8')))
PercentChange_webtab = PercentChange_webtab.rename(columns = {'Unnamed: 0': ''})


# Downloading the csv file from your GitHub

url = "https://raw.githubusercontent.com/Ryanwendling17/CCA_WebApp/main/Data/TS_CCA.csv" # Make sure the url is the raw version of the file on GitHub
download = github_session.get(url).content

# Reading the downloaded content and making it a pandas dataframe

st = pd.read_csv(io.StringIO(download.decode('utf-8')))
del st['Position']






# dropdown options
features = st.columns[1:-1]
opts = [{'label' : i, 'value' : i} for i in features]

st['Date'] = pd.to_datetime(st.Date)


dates = pd.DataFrame()
dates["Dates"] = st['Date']
dates["DOW"] = dates["Dates"] - dates["Dates"].dt.weekday * np.timedelta64(1, 'D')
dates2 = pd.DataFrame()
dates2['DOW'] = dates["DOW"]
dates2 = dates2.drop_duplicates()
dates2['DOW'] = dates2['DOW'].astype(str)
dates = dates2['DOW'].tolist()


fig3_df = st.copy()
rows = len(fig3_df.index)
fig3_df['Average Daily Calls'] = fig3_df['Calls'].sum() / rows
fig3_df['Average Daily Contacts'] = fig3_df['Contacts'].sum() / rows
fig3_df['Average Daily Contact Rate'] = fig3_df['Average Daily Contacts'] / fig3_df['Average Daily Calls']
fig3_df['Average Daily Unique Accounts Called'] = fig3_df['Unique Accounts Called'].sum() / rows
fig3_df['Average Daily Unique Accounts Contacted'] = fig3_df['Unique Accounts Contacted'].sum() / rows
fig3_df['Average Daily Account Contact Rate'] = fig3_df['Average Daily Unique Accounts Contacted'] / fig3_df['Average Daily Unique Accounts Called']
fig3_df['Average Daily Transfers'] = fig3_df['Transfers'].sum() / rows
fig3_df['Average Daily Call Transfer Rate'] = fig3_df['Average Daily Transfers'] / fig3_df['Average Daily Calls']
fig3_df['Average Daily Account Transfer Rate'] = fig3_df['Average Daily Transfers'] / fig3_df['Average Daily Unique Accounts Called']
fig3_df['Average Daily Enrollments'] = fig3_df['Enrollments'].sum() / rows
fig3_df.drop(fig3_df.columns[0:13], axis=1, inplace = True) 
fig3_df = fig3_df[:1]
fig3_df = fig3_df.round(decimals = 2)
fig3_df = fig3_df.T
fig3_df = fig3_df.rename(columns = {0: 'Over Selected Date Range'})
fig3_df.reset_index(drop = False, inplace = True)
fig3_df = fig3_df.rename(columns = {'index': ''})
figure3 = ff.create_table(fig3_df)


# Create a plotly figure
trace_1 = go.Scatter(x = st.Date, y = st['Calls'],
                    name = 'Calls',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))
layout = go.Layout(hovermode = 'closest', margin=dict(l=50, r=50, t=20, b=50))
fig = go.Figure(data = [trace_1], layout = layout)



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
metrics = PercentChange_webtab[""].unique()



figure = ff.create_table(PercentChange_webtab)
figure.layout.width = 800

figure2 = ff.create_table(Change_webtab)
figure2.layout.width = 800


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
    html.H2("CCA Performance Metrics", style={'font-size': '28pt'}),
   # generate_table(PercentChange_webtab),
    html.Br(),
                    # adding a plot
    html.H4("Time Series"),
    dcc.Graph(id = 'plot', figure = fig),
    # dropdown
    html.P([
        html.Label("Choose a Metric"),
        dcc.Dropdown(id = 'opt', options = opts,
                    value = opts[0])
            ], style = {'width': '400px',
                        'fontSize' : '18px',
                        'padding-left' : '100px',
                        'display': 'inline-block'}),
    # range slider
    html.P([
        html.Label("Time Period"),
        dcc.RangeSlider(id = 'slider',
                        marks = {i : dates[i] for i in range(0, 10)},
                        min = 0,
                        max = 9.5,
                        value = [1, 10])
            ], style = {'width' : '90%',
                        'fontSize' : '18px',
                        'padding-left' : '100px'}),
    html.Br(), html.Br(),
    html.H4("Daily Averages"),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=min(st['Date']),
        max_date_allowed=max(st['Date']),
        start_date=min(st['Date']),
        end_date=max(st['Date'])
    ),
    dcc.Graph(id='table', figure=figure3),
    html.Br(), html.Br(),
    html.H4("Percent Change Relative to Yesterday"),
    html.Div(
        [
            dcc.Dropdown(
                id="METRICS",
                options=[{
                    'label': i,
                    'value': i
                } for i in metrics],
                value='Calls'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    html.Div(children=[
        dcc.Graph(id='funnel-graph', style={'display': 'inline-block'}),
        dcc.Graph(id='my-table', figure=figure, style={'display': 'inline-block'})
    ])
    ,
    html.Br(), html.Br(),
    html.H4("Change Relative to Yesterday"),
    html.Div(
        [
            dcc.Dropdown(
                id="METRICS2",
                options=[{
                    'label': i,
                    'value': i
                } for i in metrics],
                value='Calls'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    html.Div(children=[
        dcc.Graph(id='funnel-graph2', style={'display': 'inline-block'}),
        dcc.Graph(id='my-table2', figure=figure2, style={'display': 'inline-block'})
    ])
    ,
])


# ## Figure 1: Yesterday Compare to n

# In[ ]:


@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('METRICS', 'value')])
def update_graph(Metrics):
    if Metrics == "Calls":
        trace = go.Bar(x=PercentChange ['index'], y=PercentChange [('Calls')], name='Calls')
    elif Metrics == "Contacts":
        trace = go.Bar(x=PercentChange ['index'], y=PercentChange [('Contacts')], name='Contacts')
    elif Metrics == "Contact Rate":
        trace = go.Bar(x=PercentChange ['index'], y=PercentChange [('Contact Rate')], name='Contact Rate')
    elif Metrics == "Unique Accounts Called":
        trace = go.Bar(x=PercentChange ['index'], y=PercentChange [('Unique Accounts Called')], name='Unique Accounts Called')
    elif Metrics == "Unique Accounts Contacted":   
        trace = go.Bar(x=PercentChange ['index'], y=PercentChange [('Unique Accounts Contacted')], name='Unique Accounts Contacted')
    elif Metrics == "Account Contact Rate":   
        trace = go.Bar(x=PercentChange ['index'], y=PercentChange [('Account Contact Rate')], name='Account Contact Rate')
    elif Metrics == "Transfers":  
        trace = go.Bar(x=PercentChange ['index'], y=PercentChange [('Transfers')], name='Transfers')
    elif Metrics == "Call Transfer Rate":  
        trace = go.Bar(x=PercentChange ['index'], y=PercentChange [('Call Transfer Rate')], name='Call Transfer Rate')
    elif Metrics == "Account Transfer Rate":
        trace = go.Bar(x=PercentChange ['index'], y=PercentChange [('Account Transfer Rate')], name='Account Transfer Rate')
    elif Metrics == "Enrollments":
        trace = go.Bar(x=PercentChange ['index'], y=PercentChange [('Enrollments')], name='Enrollments')
    elif Metrics == "Calls per 8 Hours":
        trace = go.Bar(x=PercentChange ['index'], y=PercentChange [('Calls per 8 Hours')], name='Calls per 8 Hours')
    elif Metrics == "Not Ready Time %":
        trace = go.Bar(x=PercentChange ['index'], y=PercentChange [('Not Ready Time %')], name='Not Ready Time %')


    return {
        'data': [trace],
        'layout':
        go.Layout(
            title='Percent Change in {}'.format(Metrics),
            xaxis = dict(title = 'Yesterday Relative to:'),
            yaxis = dict(tickformat=".0%"),
          #  font_family="Times New Roman",
          #  paper_bgcolor='#000000',
            barmode='group')
    }



@app.callback(
    dash.dependencies.Output('funnel-graph2', 'figure'),
    [dash.dependencies.Input('METRICS2', 'value')])
def update_graph(Metrics):
    if Metrics == "Calls":
        trace2 = go.Bar(x=Change ['index'], y=Change [('Calls')], name='Calls')
    elif Metrics == "Contacts":
        trace2 = go.Bar(x=Change ['index'], y=Change [('Contacts')], name='Contacts')
    elif Metrics == "Contact Rate":
        trace2 = go.Bar(x=Change ['index'], y=Change [('Contact Rate')], name='Contact Rate')
    elif Metrics == "Unique Accounts Called":
        trace2 = go.Bar(x=Change ['index'], y=Change [('Unique Accounts Called')], name='Unique Accounts Called')
    elif Metrics == "Unique Accounts Contacted":   
        trace2 = go.Bar(x=Change ['index'], y=Change [('Unique Accounts Contacted')], name='Unique Accounts Contacted')
    elif Metrics == "Account Contact Rate":   
        trace2 = go.Bar(x=Change ['index'], y=Change [('Account Contact Rate')], name='Account Contact Rate')
    elif Metrics == "Transfers":  
        trace2 = go.Bar(x=Change ['index'], y=Change [('Transfers')], name='Transfers')
    elif Metrics == "Call Transfer Rate":  
        trace2 = go.Bar(x=Change ['index'], y=Change [('Call Transfer Rate')], name='Call Transfer Rate')
    elif Metrics == "Account Transfer Rate":
        trace2 = go.Bar(x=Change ['index'], y=Change [('Account Transfer Rate')], name='Account Transfer Rate')
    elif Metrics == "Enrollments":
        trace = go.Bar(x=Change ['index'], y=Change [('Enrollments')], name='Enrollments')
    elif Metrics == "Calls per 8 Hours":
        trace2 = go.Bar(x=Change ['index'], y=Change [('Calls per 8 Hours')], name='Calls per 8 Hours')
    elif Metrics == "Not Ready Time %":
        trace2 = go.Bar(x=Change ['index'], y=Change [('Not Ready Time %')], name='Not Ready Time %')


    return {
        'data': [trace2],
        'layout':
        go.Layout(
            title='Change in {}'.format(Metrics),
            xaxis = dict(title = 'Yesterday Relative to:'),
            #yaxis = dict(tickformat=".0%"),
          #  font_family="Times New Roman",
          #  paper_bgcolor='#000000',
            barmode='group')
    }



#Add callback functions
@app.callback(Output('plot', 'figure'),
             [Input('opt', 'value'),
             Input('slider', 'value')])
def update_figure(input1, input2):
    # filtering the data
    st2 = st[(st.Date > dates[input2[0]]) & (st.Date <= dates[input2[1]])]
    # updating the plot
    trace_1 = go.Scatter(x = st2.Date, y = st2['Calls'],
                        name = 'Calls',
                        line = dict(width = 2,
                                    color = 'rgb(229, 151, 50)'))
    trace_2 = go.Scatter(x = st2.Date, y = st2[input1],
                        name = input1,
                        line = dict(width = 2,
                                    color = 'rgb(106, 181, 135)'))
    fig = go.Figure(data = [trace_2], layout = layout)
    return fig
  

@app.callback(
    dash.dependencies.Output('table', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_table(start_date, end_date):
    df = st[(st.Date >= start_date) & (st.Date <= end_date)]
    df.reset_index(drop = True, inplace = True)
    fig3_df = df.copy()
    rows = len(fig3_df.index)
    fig3_df['Average Daily Calls'] = fig3_df['Calls'].sum() / rows
    fig3_df['Average Daily Contacts'] = fig3_df['Contacts'].sum() / rows
    fig3_df['Average Daily Contact Rate'] = fig3_df['Average Daily Contacts'] / fig3_df['Average Daily Calls']
    fig3_df['Average Daily Unique Accounts Called'] = fig3_df['Unique Accounts Called'].sum() / rows
    fig3_df['Average Daily Unique Accounts Contacted'] = fig3_df['Unique Accounts Contacted'].sum() / rows
    fig3_df['Average Daily Account Contact Rate'] = fig3_df['Average Daily Unique Accounts Contacted'] / fig3_df['Average Daily Unique Accounts Called']
    fig3_df['Average Daily Transfers'] = fig3_df['Transfers'].sum() / rows
    fig3_df['Average Daily Call Transfer Rate'] = fig3_df['Average Daily Transfers'] / fig3_df['Average Daily Calls']
    fig3_df['Average Daily Account Transfer Rate'] = fig3_df['Average Daily Transfers'] / fig3_df['Average Daily Unique Accounts Called']
    fig3_df['Average Daily Enrollments'] = fig3_df['Enrollments'].sum() / rows
    fig3_df.drop(fig3_df.columns[0:13], axis=1, inplace = True) 
    fig3_df = fig3_df[:1]
    fig3_df = fig3_df.round(decimals = 2)
    fig3_df = fig3_df.T
    fig3_df = fig3_df.rename(columns = {0: 'Over Selected Date Range'})
    fig3_df.reset_index(drop = False, inplace = True)
    fig3_df = fig3_df.rename(columns = {'index': ''})
    figure3 = ff.create_table(fig3_df)
    return figure3
    
    
if __name__ == '__main__':
    app.run_server(debug=False)
