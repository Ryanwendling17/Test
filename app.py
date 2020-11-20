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



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Populate the layout with HTML and graph components
app.layout = html.Div(children = [
    
    html.H2("Department of Economics", style={'font-size': '28pt'}),
    html.H3("Undergraduate Resources", style={'font-size': '18pt'}),
    html.Br(), html.Br(),
    dcc.Tabs([
    dcc.Tab(label='Job Opportunities', children=[
    html.H4("Undergraduate Resources1", style={'font-size': '16pt'}),
    ]),
    dcc.Tab(label='Academic Opportunities', children=[
    html.H4("Undergraduate Resources2", style={'font-size': '16pt'}),
    ]),
    dcc.Tab(label='Student Resources', children=[
        html.Br(),
    html.H4("Professor Slusky’s Office Hours", style={'font-size': '16pt'}),
        html.P('Professor Slusky is the director of undergraduate studies in the economics department. Feel free to drop by his office hours this semester via Zoom if you have any questions about the economics program. You can access his office hours via this link on Tuesdays from 2-4 pm and on Thursdays from 9-11 am. (Password: 1115)'),
    html.H4("Ryan Wendling’s Office Hours", style={'font-size': '16pt'}),
        html.P('Ryan is a senior economics student who works for Professor Slusky. He is also available via Zoom this semester to answer any questions you may have about the economics department. You can access his office hours via this link on Mondays and Fridays from 3-5 pm.  (Password: 102891)'),
    html.H4("Stata Webinar: Creating customized reports in Word, Excel, and PDF", style={'font-size': '16pt'}),
        html.P('Join Gabriela Ortiz, Applied Statistician, as she demonstrates how to create Word documents with Stata summary statistics, regression tables, and graphs. Find out how to interact Stata\'s features with Word\'s features and how to automate your work when you want to regularly update reports. You will also see how easy it is to use putpdf and putexcel to similarly create reproducible reports in PDF and Excel formats. Register for this free event here.'),
    ]),
    dcc.Tab(label='Departmental Events', children=[
    html.H4("Undergraduate Resources4", style={'font-size': '16pt'}),
    ]),
    dcc.Tab(label='What an Economist Looks Like', children=[
    html.H4("Undergraduate Resources5", style={'font-size': '16pt'}),
    ]),]),
    
    
      ])



    
if __name__ == '__main__':
    app.run_server(debug=False)
