# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc
from app import app
from apps import draw
from server import run

app.layout = html.Div(
    [
## HEADER
     html.Div([
            html.Span(" --- Tracks ---", className='app-title'),
            html.Div(
                html.Img(src='./assets/VIIA-VisionBrowser.png', height="60px" ), style={"float":"right"})
            ],
            className="row header"
            ),
## TABS
        html.Div([  
            dcc.Tabs(
                id="tabs",
                style={"height":"20","verticalAlign":"Left"},
                children=[
                    dcc.Tab(label="TrackGraph", value="draw_tab")],
                colors={
                        "border": "white",
                        "primary": "deeppink",
                        "background": "whitesmoke"
                            },
                value="browser_tab")
                 ],
            className="row tabs_div"
            ),

## TAB CONTENT
        html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),
        html.Link(href="https://fonts.googleapis.com/css?family=Shadows Into Light", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Cabin", rel="stylesheet")
    ],
    className="row",
    style={"margin": "0%"}
)

@app.callback(dash.dependencies.Output("tab_content", "children"), [dash.dependencies.Input("tabs", "value")])
def render_content(tab):
    if tab == "draw_tab":
        return draw.layout
    else:
        return draw.layout

if __name__ == '__main__':
    run()
