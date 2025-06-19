from dash import Dash, html, dcc, dash_table, callback, Output, Input
import pandas as pd
import plotly.express as px

# Charger les données
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Liste des pays pour le filtre dropdown (triée)
countries = sorted(df['country'].unique())

# CSS externe - Bootstrap + Font Awesome + Google Fonts
external_stylesheets = [
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap'
]

app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server – app.server

# Styles CSS personnalisés
custom_css = {
    'container': {
        'padding': '20px',
        'fontFamily': 'Roboto, sans-serif',
        'maxWidth': '1400px',
        'margin': '0 auto'
    },
    'header': {
        'background': 'linear-gradient(135deg, #2c3e50 0%, #3498db 100%)',
        'color': 'white',
        'padding': '25px',
        'borderRadius': '8px',
        'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
        'marginBottom': '30px'
    },
    'title': {
        'fontWeight': '700',
        'fontSize': '2.5rem',
        'textAlign': 'center',
        'marginBottom': '0'
    },
    'subtitle': {
        'textAlign': 'center',
        'fontSize': '1.1rem',
        'opacity': '0.9',
        'marginTop': '10px'
    },
    'tabs': {
        'marginBottom': '30px'
    },
    'tab': {
        'border': 'none',
        'padding': '12px 24px',
        'fontWeight': '600',
        'color': '#7f8c8d',
        'borderBottom': '3px solid transparent'
    },
    'tab--selected': {
        'color': '#3498db',
        'borderBottom': '3px solid #3498db',
        'backgroundColor': 'transparent'
    },
    'dropdown': {
        'width': '100%',
        'borderRadius': '8px',
        'border': '1px solid #dfe6e9'
    },
    'card': {
        'borderRadius': '10px',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
        'border': 'none',
        'marginBottom': '20px'
    },
    'graph-container': {
        'borderRadius': '10px',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
        'padding': '15px',
        'backgroundColor': 'white'
    },
    'data-table': {
        'borderRadius': '10px',
        'overflow': 'hidden',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.05)'
    },
    'radio-items': {
        'padding': '15px',
        'borderRadius': '8px',
        'backgroundColor': '#f8f9fa',
        'marginBottom': '20px'
    },
    'radio-label': {
        'display': 'flex',
        'alignItems': 'center',
        'marginRight': '20px',
        'cursor': 'pointer'
    },
    'radio-input': {
        'marginRight': '8px'
    }
}

# Définir le layout initial
app.layout = html.Div([
    html.Div([
        # En-tête amélioré avec icône et sous-titre
        html.Div([
            html.Div([
                html.H1(
                    [
                        html.I(className="fas fa-chart-line me-3"),
                        'Tableau de bord analytique'
                    ],
                    style=custom_css['title'],
                    className='mb-2'
                ),
                html.P(
                    "Visualisation interactive des données socio-économiques mondiales",
                    style=custom_css['subtitle']
                )
            ], style=custom_css['header'])
        ], className='row'),

        # Contenu principal
        html.Div([
            dcc.Tabs(
                id='tabs-example',
                value='tab-1',
                children=[
                    dcc.Tab(
                        label='Données & Analyses',
                        value='tab-1',
                        style=custom_css['tab'],
                        selected_style=custom_css['tab--selected']
                    ),
                    dcc.Tab(
                        label='Carte mondiale',
                        value='tab-2',
                        style=custom_css['tab'],
                        selected_style=custom_css['tab--selected']
                    )
                ],
                style=custom_css['tabs']
            ),

            # Contenu des onglets
            html.Div(id='tabs-content')
        ], style=custom_css['container'])
    ])
])

# Layout pour l'onglet 1 (Données & Analyses)
tab1_layout = html.Div([
    # Filtres et contrôles
    html.Div([
        html.Div([
            html.Label("Filtrer par pays", className="form-label fw-bold"),
            dcc.Dropdown(
                options=[{'label': c, 'value': c} for c in countries],
                value=None,
                placeholder="Sélectionnez un ou plusieurs pays...",
                id='dropdown-country',
                clearable=True,
                multi=True,
                style=custom_css['dropdown']
            )
        ], className="mb-4"),

        html.Div([
            html.Label("Métrique à visualiser", className="form-label fw-bold"),
            html.Div([
                dcc.RadioItems(
                    id='controls-and-radio-item',
                    options=[
                        {'label': 'Population', 'value': 'pop'},
                        {'label': 'Espérance de vie', 'value': 'lifeExp'},
                        {'label': 'PIB par habitant', 'value': 'gdpPercap'}
                    ],
                    value='lifeExp',
                    labelStyle={'display': 'flex', 'alignItems': 'center', 'marginRight': '20px'},
                    inputStyle={'marginRight': '8px'}
                )
            ], style=custom_css['radio-items'])
        ])
    ], className="card p-4", style=custom_css['card']),

    # Tableau de données
    html.Div([
        html.H4([
            html.I(className="fas fa-table me-2"),
            "Données détaillées"
        ], className="mb-3"),
        html.Div(
            dash_table.DataTable(
                id='datatable',
                columns=[{"name": i, "id": i} for i in df.columns],
                page_size=8,
                style_table={
                    'overflowX': 'auto',
                    'borderRadius': '10px',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.05)'
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '12px',
                    'fontFamily': 'Roboto',
                    'fontSize': '14px',
                    'border': '1px solid #f1f1f1'
                },
                style_header={
                    'backgroundColor': '#3498db',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'textTransform': 'uppercase',
                    'fontSize': '13px'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f8f9fa'
                    },
                    {
                        'if': {'state': 'active'},
                        'backgroundColor': 'rgba(52, 152, 219, 0.2)',
                        'border': '1px solid #3498db'
                    }
                ],
                filter_action='native',
                sort_action='native',
                sort_mode='multi',
                page_action='native'
            ),
            style=custom_css['data-table']
        )
    ], className="card p-4 mb-4", style=custom_css['card']),

    # Graphique
    html.Div([
        html.H4([
            html.I(className="fas fa-chart-bar me-2"),
            "Visualisation"
        ], className="mb-3"),
        dcc.Graph(
            figure={},
            id='controls-and-graph',
            style={'height': '500px'}
        )
    ], className="card p-4", style=custom_css['card'])
])

# Layout pour l'onglet 2 (Carte mondiale)
tab2_layout = html.Div([
    html.Div([
        html.H4([
            html.I(className="fas fa-map me-2"),
            "Carte du PIB moyen par continent"
        ], className="mb-3"),
        dcc.Graph(
            id='map-gdp',
            style={'height': '700px'}
        )
    ], className="card p-4", style=custom_css['card'])
])

# Callback pour le contenu des onglets
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs-example', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return tab1_layout
    elif tab == 'tab-2':
        return tab2_layout

# Callback pour mettre à jour tableau et graphique selon pays (liste) et métrique choisie
@callback(
    Output('datatable', 'data'),
    Output('controls-and-graph', 'figure'),
    Input('dropdown-country', 'value'),
    Input('controls-and-radio-item', 'value')
)
def update_table_graph(countries_selected, col_chosen):
    # Si sélection multiple
    if countries_selected and len(countries_selected) > 0:
        dff = df[df['country'].isin(countries_selected)]
    else:
        dff = df.copy()

    # DataTable
    data = dff.to_dict('records')

    # Graphique : barre par pays sélectionnés ou moyenne par continent si aucun pays
    if countries_selected and len(countries_selected) > 0:
        fig = px.bar(
            dff, 
            x='country', 
            y=col_chosen,
            title=f"<b>{col_chosen}</b> pour les pays sélectionnés",
            labels={col_chosen: col_chosen.capitalize(), 'country': 'Pays'},
            color='continent',
            height=500
        )
    else:
        fig = px.histogram(
            df, 
            x='continent', 
            y=col_chosen, 
            histfunc='avg',
            title=f"<b>Moyenne de {col_chosen}</b> par continent",
            color='continent',
            height=500
        )
    
    # Style commun pour les graphiques
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Roboto', 'color': '#2c3e50'},
        hovermode='closest',
        margin={'l': 40, 'r': 40, 't': 80, 'b': 40},
        title_x=0.5,
        title_font_size=20
    )
    
    fig.update_traces(
        marker_line_width=1,
        marker_line_color='white'
    )

    return data, fig

# Callback carte
@callback(
    Output('map-gdp', 'figure'),
    Input('tabs-example', 'value')
)
def update_map(tab):
    if tab != 'tab-2':
        return {}
    
    gdp_by_continent = df.groupby('continent')['gdpPercap'].mean().reset_index()
    df_map = df.merge(gdp_by_continent, on='continent', suffixes=('', '_mean'))

    fig = px.choropleth(
        df_map,
        locations='country',
        locationmode='country names',
        color='gdpPercap_mean',
        hover_name='country',
        hover_data={'gdpPercap_mean': ':.2f', 'continent': True},
        color_continuous_scale='Viridis',
        labels={'gdpPercap_mean': 'PIB moyen par continent'},
        title='<b>PIB moyen par habitant par continent</b>'
    )
    
    fig.update_layout(
        width=1400,
        height=700,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        ),
        margin={"r":0,"t":80,"l":0,"b":0},
        coloraxis_colorbar={
            'title': 'PIB moyen',
            'thickness': 20,
            'len': 0.75
        },
        title_x=0.5,
        font={'family': 'Roboto'}
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)
