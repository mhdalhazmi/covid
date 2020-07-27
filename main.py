import dash
import dash_core_components as dcc
import dash_html_components as html
from htexpr import compile
import unicodedata
from flask import Flask
import requests
import pandas as pd
import time
import chart_studio.plotly as py
import plotly.express as px
import dash_bootstrap_components as dbc
from toolz import curry
from htexpr.mappings import dbc_and_default
import dash_table

compile = curry(compile)(map_tag=dbc_and_default)


server = Flask(__name__)

df_final = pd.read_csv("df_final.csv")
df_total_stats = pd.read_csv("df_total_stats.csv")
df_news = pd.read_csv("df_news.csv")

mapbox_access_token = 'pk.eyJ1IjoiaGFzdHlsZSIsImEiOiJja2QwM2dtdHgwcHVhMzBwZ3F0azlpMDZtIn0.mCN0EYyBKElCkJPOO1xA7A'

color_scale = [
        "#fadc8f",
        "#f9d67a",
        "#f8d066",
        "#f8c952",
        "#f7c33d",
        "#f6bd29",
        "#f5b614",
        "#F4B000",
        "#eaa900",
        "#e0a200",
        "#dc9e00",
        ]


px.set_mapbox_access_token(mapbox_access_token)
df_final['Size'] = df_final['Confirmed Cases']**0.77

fig = px.scatter_mapbox(df_final,
                        lat="Latitude", lon="Longitude",
                        color="Confirmed Cases", size="Size",
                        hover_name="Country",
                        hover_data=["Confirmed Cases", "Recovered Cases","Critical Cases","Deaths"],
                        title= 'World-wide Covid-19 status',
                        color_continuous_scale=color_scale,
                        zoom=15)
fig.layout.update(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        # This takes away the colorbar on the right hand side of the plot
        coloraxis_showscale=False,
        mapbox_style='mapbox://styles/hastyle/ckd04vx3w0orf1irxdgxzotia',
        mapbox=dict(center=dict(lat=40.721319,lon=-73.987130), zoom=1),
        )
fig.data[0].update(hovertemplate= '<b>%{hovertext}</b><br>Confirmed Cases= %{marker.color}<br>Recovered Cases= %{customdata[1]}<br>Critical Cases= %{customdata[2]}<br>Deaths= %{customdata[3]}')

#app.layout = html.Div([
#    dcc.Graph(
#        id='confirmed-map',
#        figure=fig
#    )
#])



app = dash.Dash(__name__, server = server,external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css',
                                                '//use.fontawesome.com/releases/v5.0.7/css/all.css',
                                                '/assets/style.css'])

nav = compile("""
    <div class="main-nav col-md">
      <div class="nav-container">
      <div class="icon">
      <img src="./assets/Icon.png" alt=""></img></div>
      <div class="icon">
      <img src="./assets/Mail.png" alt=""></img></div>
      <div class="icon">
      <img src="./assets/stats.png" alt=""></img></div>
      </div>
    </div>
""")

content = compile("""
        <div class="main-map col-md">
          <div class="worldwide-stats">
            <div class="worldwide-title">
            <h1>الإحصاءات الإجمالية في العالم</h1>
            </div>
            <div class="worldwide-icon-container">
              <div class="worldwide-icon">
                <div class="left-icon-block">
                  <img src="./assets/spread.png" alt=""></img>
                </div>
                <div class="right-text-block">
                  <p>المصابون</p>
                  <p>{f"{df_total_stats['confirmed'][0]:,}"}</p>
                </div>
              </div>
              <div class="worldwide-icon">
                <div class="left-icon-block">
                  <img src="./assets/halloween.png" alt=""></img>
                </div>
                <div class="right-text-block">
                  <p>الوفيات</p>
                  <p>{f"{df_total_stats['deaths'][0]:,}"}</p>
                </div>
              </div>
              <div class="worldwide-icon">
                <div class="left-icon-block">
                  <img src="./assets/person.png" alt=""></img>
                </div>
                <div class="right-text-block">
                  <p>الحالات الخطرة</p>
                  <p>{f"{df_total_stats['critical'][0]:,}"}</p>
                </div>
              </div>
              <div class="worldwide-icon">
                <div class="left-icon-block">
                  <img src="./assets/spread.png" alt=""></img>
                </div>
                <div class="right-text-block">
                  <p>المتعافون</p>
                  <p>{f"{df_total_stats['recovered'][0]:,}"}</p>
                </div>
              </div>

            </div>
          </div>
          <div class="map">
          <Graph id="map" figure={fig} config={'displayModeBar': False} /> </div>
          <div class="footer">
            <span class="footer">
                Made with <i class="fa fa-heart pulse"></i> in <a target="_blank">KSA</a>
            </span>
            </div>
        </div>
""")

logo = compile("""
          <div class="logo">
          <img src="./assets/logo2.png" alt=""/></div>

""")



df_stat = df_final.copy()
df_stat = df_stat(['Country', 'Confirmed Cases', 'Deaths'])
stats = html.Div([html.Div([html.H1("احصائيات الدول")], className="worldwide-title"),
        html.Div(dash_table.DataTable(
                                    id='table',
                                    columns=[{"name": i, "id": i} for i in df_stat.columns],
                                    data=df_stat.to_dict('records'),
                                    editable=False,
                                    sort_action="native",
                                    sort_mode="multi",
                                    column_selectable="single",
                                    style_as_list_view=True,
                                    fixed_rows={"headers": True},
                                    fill_width=True,
                                    style_table={'height': '350px',"width": "100%", },
                                    #style_table={
                                    #    "width": "100%",
                                    #    "height": "100vh",
                                    #},
                                    style_header={
                                        "backgroundColor": "#262A2F",
                                        "border": "#2b2b2b",
                                        "fontWeight": "bold",
                                        "font": "Lato, sans-serif",
                                        "height": "2vw",
                                    },
                                    style_cell={
                                        'textAlign': 'center',
                                        "font-size": "14px",
                                        "font-family": "Lato, sans-serif",
                                        "border-bottom": "0.01rem solid #313841",
                                        "backgroundColor": "#262A2F",
                                        "color": "#FEFEFE",
                                        "height": "2.75vw",
                                        'whiteSpace': 'normal',
                                        'height': 'auto',

                                    },
                                    style_cell_conditional=[
                                        {
                                            "if": {"column_id": "Country",},
                                            "minWidth": "3vw",
                                            "width": "3vw",
                                            "maxWidth": "3vw",
                                            "textAlign": "left"
                                        },
                                        {
                                            "if": {"column_id": "Confirmed Cases",},
                                            "color": "#F4B000",
                                            "minWidth": "3vw",
                                            "width": "3vw",
                                            "maxWidth": "3vw",
                                        },
                                        {
                                            "if": {"column_id": "Deaths",},
                                            "color": "#E55465",
                                            "minWidth": "3vw",
                                            "width": "3vw",
                                            "maxWidth": "3vw",
                                        },
                                    ],
                                    ), className="stats_table")
])
news =  html.Div([html.Div([html.H1("اخر الأخبار")], className="worldwide-title"),
        dbc.ListGroup([
                        dbc.ListGroupItem([
                            html.Div([
                                html.H6(
                                        f"{df_news.iloc[i]['title']}",
                                        className="news-txt-headline",
                                ),
                                html.P(
                                        f"source: {df_news.iloc[i]['clean_url']}.",
                                        className = "news-txt-source",
                                ),
                            ], className = "news-item-container")
                        ],  className="news-item", href=df_news.iloc[i]["link"])
                        for i in range(len(df_news))
        ], className = "news-container", flush=True, )
])

app.layout = html.Div(
                        html.Div([
                        nav.run(), content.run(),
                        html.Div([logo.run(),stats, news],className="main-stats col-md")
                        ], className='row')
                        , className="container-fluid")



# Run the server
if __name__ == '__main__':
    app.run_server()
