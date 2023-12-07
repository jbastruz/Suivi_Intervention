import dash
from dash import html, dcc, Input, Output, callback, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import mysql.connector
import dash_auth
import os
import base64
#import time

load_figure_template("morph")

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

UPLOAD_DIRECTORY = os.path.abspath("/opt/lampp/htdocs/dolibarr/documents/ficheinter/")

VALID_USERNAME_PASSWORD_PAIRS = {
    'USER': 'PASSWORD'
}

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Incorporate data
global df

def Update_data():

    config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',

    'port': 3306,
    'database': 'dolibarr'
    }
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    #Base FicheInter
    cursor.execute("SELECT * FROM llx_fichinter")
    res = cursor.fetchall()
    df_inter = pd.DataFrame(res)

    #Base Société
    cursor.execute("SELECT rowid, nom FROM llx_societe")
    res = cursor.fetchall()
    df_soc = pd.DataFrame(res)
    df_soc
    df_inter = pd.merge(df_inter, df_soc, left_on = "fk_soc", right_on = "rowid", how = "left").drop("rowid_y" ,axis=1).rename(columns={"rowid_x": "rowid", "nom":"client"})

    #Base Intervenant
    cursor.execute("SELECT element_id, fk_c_type_contact, fk_socpeople FROM llx_element_contact")
    res = cursor.fetchall()
    df_Intervenant = pd.DataFrame(res)
    df_Intervenant.rename(columns={'element_id':'rowid', 'fk_c_type_contact':'TypeInter', 'fk_socpeople':'Inter'}, inplace=True)
    df_Intervenant = df_Intervenant[df_Intervenant["TypeInter"]==27].drop('TypeInter', axis = 1)
    df_Intervenant

    #base Key Intervenant
    cursor.execute("SELECT rowid, lastname FROM llx_user")
    res = cursor.fetchall()
    df_user = pd.DataFrame(res)
    df_user

    # #Merge des tables dans la Table df mise en variable globale
    df = pd.DataFrame()
    df_inter = pd.merge(df_inter, df_Intervenant, on = "rowid", how = "left")
    df = pd.merge(df_inter, df_user, left_on='Inter', right_on='rowid', how="left").drop('Inter', axis=1).drop('rowid_y', axis=1).rename(columns={'lastname':'Inter'})
    df["KEY"] = df["client"]+" : "+df["description"]

    return df

df = Update_data()

dcc.Location(id='url', refresh=False)

# Initialize the app
app = dash.Dash(__name__, suppress_callback_exceptions=True, title="Suivi d'interventions", external_stylesheets=[dbc.themes.MORPH, dbc.icons.FONT_AWESOME, dbc_css])
server = app.server
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

def layout_function():

    df = Update_data()
    dropdown_inter = html.Div(
            [
                dbc.Label("Intervenants"),
                dcc.Dropdown(
                    df['Inter'].unique(),
                    "None",
                    id="my-inter",
                    clearable=True,
                )
            ],
            #className="mb-4",
        )

    return dbc.Container(
        [
            dcc.Interval(
                id='interval-component',
                interval=3600 * 1000,  # en millisecondes, met à jour toutes les 3600 secondes
                n_intervals=0
            ),
            html.H1('Application de suivi d\'interventions v0.6', className="p-2 mb-2 text-center"),
            dbc.Row([
                # dbc.Col(
                #     dbc.Card([html.H4("Selections", className="card-title"),dropdown], body=True), width="3"
                # ),
                dbc.Col([
                    dbc.Container([
                        dbc.Card([html.H4("Selections", className="card-title"), dropdown_inter, html.Br(), html.Div(id = 'Techni')], body=True),
                        html.Br(),
                        dbc.Tabs([
                            dbc.Tab(label='Inputs', children=[
                                html.H4('Notes de l\'intervenant', className="border-bottom p-2 mb-2"),
                                dbc.Textarea(id = 'notes-textarea', className="mb-3", placeholder="Notez vos observations"),
                                html.H4('Photos', className="border-bottom p-2 mb-2"),
                                dbc.Row([
                                    dbc.Col([
                                        dcc.Upload(
                                            id='upload-image',
                                            children=html.Div([
                                                'Image 1'
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
                                            multiple=True
                                        ),
                                        html.Br(),
                                        html.Div(id='output-image-upload')
                                    ]),
                                    dbc.Col([
                                        dcc.Upload(
                                            id='upload-image2',
                                            children=html.Div([
                                                'Image 2'
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
                                            multiple=True
                                        ),
                                        html.Br(),
                                        html.Div(id='output-image-upload2')
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dcc.Upload(
                                            id='upload-image3',
                                            children=html.Div([
                                                'Image 3'
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
                                            multiple=True
                                        ),
                                        html.Br(),
                                        html.Div(id='output-image-upload3')
                                    ]),
                                    dbc.Col([
                                        dcc.Upload(
                                            id='upload-image4',
                                            children=html.Div([
                                                'Image 4'
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
                                            multiple=True
                                        ),
                                        html.Br(),
                                        html.Div(id='output-image-upload4')
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dcc.Upload(
                                            id='upload-image5',
                                            children=html.Div([
                                                'Image 5'
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
                                            multiple=True
                                        ),
                                        html.Br(),
                                        html.Div(id='output-image-upload5')
                                    ]),
                                ]),
                                html.Br(),
                                dbc.Row([
                                    dbc.Col([
                                            dbc.Button("Mettre à jour", id = "my-button", color="secondary", className="me-1")
                                        ],
                                        #width={"size": 5}
                                    ),
                                    dbc.Col(
                                        dbc.ModalBody(dbc.Spinner(html.Div(id="uploaded-images"), color = "primary")),
                                        width={"size": 3}
                                    )
                                ]),
                                dbc.Row([
                                    html.Br()
                                ])
                            ]),
                            # dbc.Tab(label='Output', children=[
                            #     html.Br(),
                            #     dbc.Row([
                            #         dbc.Card([
                            #             dbc.CardHeader("Notes de l'intervenant"),
                            #             dbc.CardBody(id = 'Displayed-Notes')
                            #         ])
                            #     ]),
                            #     html.Br(),
                            #     dbc.Row([
                            #         dbc.Card([
                            #             dbc.CardHeader("Images"),
                            #             dbc.CardBody([
                            #                 dbc.Row([
                                                
                            #                 ])
                            #             ])
                            #         ])
                            #     ])                        
                            # ])
                        ])
                    ]),
                ])
            ]),
        ],
        
        fluid=True,
        className="dbc dbc-ag-grid",
    )

# App layout
app.layout = layout_function

# Definition de Fonction

def parse_contents(contents):
    return html.Div([

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents, style={'width': '100%'})
    ])

def save_file(name, content, dossier):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(os.path.join(UPLOAD_DIRECTORY, dossier), name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

def display_Notes(name):
    if not(df[df['ref'] == name]['note_public'].empty):
        return html.P([
                df[df['ref'] == name]['note_public'].tolist()[0]
        ])

#Callbacks
@callback(Output('Displayed-Notes', 'children'),
              Input('my-input', 'value'),
              prevent_initial_call=True)
def update_output(Intervention):

    display_Notes(Intervention)
    nom_inter = df[df["KEY"] == Intervention]['ref'].to_string().split(" ")[-1]
    if not(df[df['ref'] == nom_inter]['note_public'].empty):
        res = display_Notes(nom_inter)
        return res
    
@callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c) for c, n in
            zip(list_of_contents, list_of_names)]
        return children

@callback(Output('output-image-upload2', 'children'),
              Input('upload-image2', 'contents'),
              State('upload-image2', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c) for c, n in
            zip(list_of_contents, list_of_names)]
        return children
    
@callback(Output('output-image-upload3', 'children'),
              Input('upload-image3', 'contents'),
              State('upload-image3', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c) for c, n in
            zip(list_of_contents, list_of_names)]
        return children
    
@callback(Output('output-image-upload4', 'children'),
              Input('upload-image4', 'contents'),
              State('upload-image4', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c) for c, n in
            zip(list_of_contents, list_of_names)]
        return children
    
@callback(Output('output-image-upload5', 'children'),
              Input('upload-image5', 'contents'),
              State('upload-image5', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c) for c, n in
            zip(list_of_contents, list_of_names)]
        return children

# définition des Callback()
@callback(
    Output('uploaded-images', 'children'),
    Input('my-button', 'n_clicks'),
    State('upload-image', 'contents'),
    State('upload-image', 'filename'),
    State('upload-image2', 'contents'),
    State('upload-image2', 'filename'),
    State('upload-image3', 'contents'),
    State('upload-image3', 'filename'),
    State('upload-image4', 'contents'),
    State('upload-image4', 'filename'),
    State('upload-image5', 'contents'),
    State('upload-image5', 'filename'),
    State('my-input', 'value'),
    State('notes-textarea', 'value'),
    prevent_initial_call=True,
)
def update_database(n_clicks, img1_contents, img1_filename, img2_contents, img2_filename, img3_contents, img3_filename, img4_contents, img4_filename, img5_contents, img5_filename,
                    selected_intervention, notes_value):
    config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',

    'port': 3306,
    'database': 'dolibarr'
    }
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    
    if selected_intervention == 'None':
        return dbc.Modal([
                        dbc.ModalHeader(dbc.ModalTitle("Mise à jour"), close_button=False),
                        dbc.ModalBody("Pensez à sélectionner une intervention"),
                    ],
                size="sm",
                is_open = True, 
                centered=True,
                )
    
    if n_clicks is not None:

        nom_inter = df[df["KEY"] == selected_intervention]['ref'].to_string().split(" ")[-1]
        images = [img1_contents, img2_contents, img3_contents, img4_contents, img5_contents]
        FileNames = [img1_filename, img2_filename, img3_filename, img4_filename, img5_filename]
        column_names = ['Image1', 'Image2', 'Image3', 'Image4', 'Image5']

        if notes_value:
            # Update the 'Notes' column
            query_notes = f"UPDATE llx_fichinter SET note_public = '{notes_value}' WHERE ref = '{nom_inter}'"
            cursor.execute(query_notes)
            cnx.commit()
        
        for i, uploaded_file_contents in enumerate(images, start=1):
            if uploaded_file_contents is not None:
                uploaded_filenames = FileNames[i-1]

                for name, data in zip(uploaded_filenames, uploaded_file_contents):
                    save_file(str(i)+" "+name, data, nom_inter)

        #time.sleep(10)
        return dbc.Modal([
                    dbc.ModalHeader(dbc.ModalTitle("Mise à jour"), close_button=False),
                    dbc.ModalBody("Modifications prises en compte !"),
                ],
                size = 'sm',
                is_open = True, 
                centered=True,
                )
    
@callback(Output('data-store', 'data'),
          Input('url', 'pathname'))
def update_data(url):
    df = Update_data()

    return df.to_json(date_format='iso', orient='split')

@callback(Output('Techni', 'children'),
          Input('my-inter', 'value'),
          prevent_initial_call=False)
def define_inter(Inter):

    df = Update_data()

    if Inter is None:
        return html.Div(
        [
            dbc.Label("Interventions"),
            dcc.Dropdown(
                df['KEY'].unique(),
                "None",
                id="my-input",
                clearable=True,
            )
        ])
    else:
        return html.Div(
        [
            dbc.Label("Interventions"),
            dcc.Dropdown(
                df[df["Inter"] == Inter]['KEY'].unique(),
                "None",
                id="my-input",
                clearable=True,
            )
        ])

options = {
    "bind": "0.0.0.0:8081",
    "workers": 3,
    "worker_class": "gevent",  # Use gevent workers for asynchronous requests
}

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8081, debug=False)
