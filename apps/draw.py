import os
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd

from datetime import datetime as dt, timedelta, date
import time
import numpy as np
import random

import plotly.graph_objs as go
from app import app
from utils import write_csv, assign_term
from style_html import header_style, section_dropdown_style

DATE_TIME =(time.strftime("%d-%m-%Y"))
PATH_DATA_CIR = './data/circulation_data_23-07-2019.csv'

def read_circulation_data():
    if os.path.isfile(PATH_DATA_CIR) == True:
        df = pd.read_csv(PATH_DATA_CIR, sep=';')
    else:
        print('file not found')
    return df

def process_df(df):
    df['TERM_DEP'] = df.CODLIGNE.apply(lambda x: assign_term(x[:3]))
    df = df.drop_duplicates(subset='NUMMISDEP')
    df = df.dropna(subset=['NUMMISDEP'])

    df['CODSEG'] = df.CODSEG.apply(lambda x : x[-5:])
    df_g = df[['CODSEG', 'DEP', 'ARR', 'SENS', 'CODLIGNE', 'CODSILLON', 'TERM_DEP', 'DSTFIN']]
    df_g.columns = ['Train', 'Debut', 'Fin', 'Sens', 'Couleur', 'Sillon', 'TermDep', 'TermFin']
    df_g['Couleur'] = str(1)
    df_g['TermDep'] = str(0)
    df_g['TermFin'] = str(1)
    df_g['Closing'] = int(2)
    df_g['Mad'] = int(2)
    df_g['Debut'] = df_g.Debut.apply(lambda x:((dt.strptime(str(x), "%d-%m-%Y %H:%M:%S")) if pd.notnull(x)  else x))
    df_g['Fin'] = df_g.Fin.apply(lambda x:((dt.strptime(str(x), "%d-%m-%Y %H:%M:%S")) if pd.notnull(x)  else x))
    df_g = df_g[['Train', 'Debut', 'Fin', 'Couleur', 'TermDep','TermFin', 'Closing', 'Mad']]
    return df_g.tail(2)

def init_term():
    d = {'TERM': ['LE BOULOU', 'BETTEMBOURG']}
    df = pd.DataFrame(data = d)
    return df

def draw_marey(df1, df2):
    list_term = df2['TERM'].values.tolist()
    list_y = []
    for t in list_term:
        ind = list_term.index(t)
        list_y.append(ind)
    list_trace = []

    colors = {'1': 'blue',
            '2': 'lightblue',
            '3': 'lightgreen',
            '4': 'darkgreen',
            '5': 'purple',
            '6': 'mediumpurple',
            '7' : 'salmon',
            '8': 'lightsalmon',
            '9': 'chocolate',
            '10': 'beige',
            '11': 'darkturquoise',
            '12': 'turquoise',
            '13': 'purple',
            '14': 'mediumpurple',
            '15': 'lightgoldenrodyellow',
            '16': 'gold'}

    for i in df1.columns:

        date_clos = dt.strptime(df1[i][1], '%Y-%m-%d %H:%M:%S') + timedelta(hours= -int(df1[i][6]))
        date_mad =  dt.strptime(df1[i][2], '%Y-%m-%d %H:%M:%S') + timedelta(hours= +int(df1[i][7]))
        
        trace = go.Scatter(
                x=[str(date_clos), 
                df1[i][1], df1[i][2], str(date_mad)],
                y=[ df1[i][4], df1[i][4], df1[i][5], df1[i][5] ],
                name= str([df1[i][0]]),
                mode = 'lines+markers',
                connectgaps=True,
                marker=dict(
                    color=colors[df1[i][3]],
                    line=dict(
                        color=colors[df1[i][3]],
                        width=2),
                    ),
                opacity=0.7)
        list_trace.append(trace)
    data = list_trace

    layout = go.Layout(
        autosize=True,
        xaxis=dict(
            showgrid=True, 
            tickfont=dict(
        size=8,
        color='grey')
        ),
        barmode='group',
        yaxis=dict(showgrid=True, 
                showticklabels=True,
                tickmode = 'array',
                tickvals = list_y,
                ticktext = list_term,
                tickfont = dict(size = 9)
                    )
                )
    return go.Figure(data = data, layout=layout)   

def graph_html():
    return html.Div([dcc.Graph(id='my_marey',
    style={"height": "60vh", "width": "100%", 'border': 'thin lightgrey dashed', 'display': 'inline-block'})
    ], className="seven columns")

def table_term(df2):
    return html.Div([
    html.H4('Modify Line'),
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df2.columns],
        data=df2.to_dict('rows'),
        editable=True,
        row_deletable=True,
        id='editable-table-term',
    ) ,
    html.Div(className="row", style={"margin": "1% 0.2%"}),
    html.Button('Add Stop', id='editing-rows-button-term', n_clicks=0)
], className='four columns')

def upload_html():
    return html.Div([
    html.H4('Upload File'),
    html.Div([
        dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
            ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
            },
        # Allow multiple files to be uploaded
        multiple=False
        ),
        html.Div(id='output-data-upload'),
        ])
    ], className='four columns')

def table_html(df):
    return html.Div([
    html.H4('Modify TimeTable'),
    html.H5('Keep date format like 2019-07-01 19:23:00 ; Colors are between 1-16'),
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('rows'),
        # optional - sets the order of columns
        editable=True,
        row_deletable=True,
        id='editable-table'
    ),
    html.Div(className="row", style={"margin": "1% 0.2%"}),
    html.Button('+ Void Circ', id='editing-rows-button', n_clicks=0,  n_clicks_timestamp='0'),
    html.Button('+ 1 day Circ', id='repeat-button', n_clicks=0,  n_clicks_timestamp='0'),
], className='four columns')


df = process_df(read_circulation_data())
df2 = init_term()

layout = [
        html.Div([
            graph_html(),
            table_term(df2),
            table_html(df)
            ], className="row"),
        html.Div([
            upload_html()
        ], className="row"),

]

# hide/show modal
@app.callback(dash.dependencies.Output('modal', 'style'),
              [dash.dependencies.Input('button-draw', 'n_clicks'),
              dash.dependencies.Input('modal-close-button', 'n_clicks')])

def show_modal(n, n2):
    if isinstance(n, int)  == True:
        if n > 0:
            return {"display": "block"}
        else :
            return {"display": "none"}
    elif n2 is not None and n2 > 0:
        return {"display": "none"}
# Close modal by resetting info_button click to 0
@app.callback(dash.dependencies.Output('button-draw', 'n_clicks'),
              [dash.dependencies.Input('modal-close-button', 'n_clicks')])
def close_modal(n):
    return 0

#TABLE TIME
@app.callback(
    dash.dependencies.Output('editable-table', 'data'),
    [dash.dependencies.Input('editing-rows-button', 'n_clicks_timestamp'),
    dash.dependencies.Input('repeat-button', 'n_clicks_timestamp')],
    [dash.dependencies.State('editable-table', 'data'),
     dash.dependencies.State('editable-table', 'columns')])

def add_row(n, n2,  rows, columns):
    if int(n) > int(n2) :
        rows.append({c['id']: '' for c in columns})
    elif int(n2) > int(n):
        last_line = dict()
        train = rows[-1].get('Train')
        date_deb = rows[-1].get('Debut')
        date_fin = rows[-1].get('Fin')
        color = rows[-1].get('Couleur')
        term_dep1 = rows[-1].get('TermDep')
        term_fin1 = rows[-1].get('TermFin')
        hour_clos = rows[-1].get('Closing')
        hour_mad = rows[-1].get('Mad')
        date_deb1 = dt.strptime(date_deb, '%Y-%m-%d %H:%M:%S') + timedelta(days=1)
        date_fin1 = dt.strptime(date_fin, '%Y-%m-%d %H:%M:%S') + timedelta(days=1)
        last_line = {'Train': train, 'Debut': date_deb1, 'Fin': date_fin1, 'Couleur': color, 'TermDep' : term_dep1, 'TermFin': term_fin1, 'Closing': hour_clos, 'Mad': hour_mad}
        rows.append(last_line)
    return rows   

#TABLE TERM
@app.callback(
    dash.dependencies.Output('editable-table-term', 'data'),
    [dash.dependencies.Input('editing-rows-button-term', 'n_clicks')],
    [dash.dependencies.State('editable-table-term', 'data'),
     dash.dependencies.State('editable-table-term', 'columns')])

def add_row_term(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

@app.callback(
    dash.dependencies.Output('my_marey', 'figure'),
    [dash.dependencies.Input('editable-table', 'data'),
    dash.dependencies.Input('editable-table', 'columns'),
    dash.dependencies.Input('editable-table-term', 'data'),
    dash.dependencies.Input('editable-table-term', 'columns')])

def display_output(rows, columns, rows2, columns2):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    df2 = df.T
    dft = pd.DataFrame(rows2, columns=[c2['name'] for c2 in columns2])
    return draw_marey(df2, dft)