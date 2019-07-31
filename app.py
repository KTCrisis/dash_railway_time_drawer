# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import flask

#app = dash.Dash(__name__)
#server = app.server

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
application = app.server

app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
