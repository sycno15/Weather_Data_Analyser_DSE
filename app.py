import dash
from dash import dcc, html, dash_table, Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from weather import WeatherDataAnalyzer
from datetime import datetime
import base64
import io

# Initialize the app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Weather Data Analyzer"

# Initialize analyzer
analyzer = WeatherDataAnalyzer()

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🌤️ Weather Data Analyzer", 
                style={'textAlign': 'center', 'color': '#667eea', 'marginBottom': '10px'}),
        html.Hr()
    ]),
    
    # Main container
    html.Div([
        # Sidebar
        html.Div([
            html.H3("📊 Data Source", style={'color': '#667eea'}),
            
            dcc.RadioItems(
                id='data-source',
                options=[
                    {'label': 'Upload CSV File', 'value': 'upload'},
                    {'label': 'Get Real Data', 'value': 'fetch'}
                ],
                value='upload',
                style={'marginBottom': '20px'}
            ),
            
            # Upload section
            html.Div(id='upload-section', children=[
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        '📁 Drag and Drop or ',
                        html.A('Select CSV File')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '2px',
                        'borderStyle': 'dashed',
                        'borderRadius': '10px',
                        'textAlign': 'center',
                        'margin': '10px 0',
                        'backgroundColor': '#f8f9ff',
                        'cursor': 'pointer'
                    }
                ),
            ]),
            
            # Fetch section
            html.Div(id='fetch-section', style={'display': 'none'}, children=[
                html.Label("Number of days:"),
                dcc.Slider(
                    id='days-slider',
                    min=30,
                    max=365,
                    value=365,
                    marks={30: '30', 90: '90', 180: '180', 365: '365'},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.Br(),
                html.Label("Select a city:"),
                dcc.Dropdown(
                    id='city-dropdown',
                    options=[
                        {'label': city, 'value': city} 
                        for city in ["Nagpur", "New Delhi", "Mumbai", "Chennai", 
                                   "Bengaluru", "Kolkata", "Hyderabad"]
                    ],
                    value='Nagpur'
                ),
                html.Br(),
                html.Button('Get Data', id='fetch-btn', n_clicks=0,
                           style={'width': '100%', 'padding': '10px', 'backgroundColor': '#667eea',
                                 'color': 'white', 'border': 'none', 'borderRadius': '8px',
                                 'cursor': 'pointer', 'fontSize': '16px', 'fontWeight': 'bold'})
            ]),
            
            html.Hr(),
            
            # Quick Info
            html.Div(id='quick-info', children=[
                html.H4("📋 Quick Info", style={'color': '#667eea'}),
                html.Div(id='info-content')
            ])
            
        ], style={'width': '25%', 'padding': '20px', 'backgroundColor': '#f9f9f9', 
                 'borderRadius': '10px', 'marginRight': '20px'}),
        
        # Main content
        html.Div([
            dcc.Store(id='stored-data'),
            html.Div(id='status-message'),
            
            dcc.Tabs(id='tabs', value='statistics', children=[
                dcc.Tab(label='📊 Statistics', value='statistics'),
                dcc.Tab(label='📈 Visualizations', value='visualizations'),
                dcc.Tab(label='🌡️ Extremes', value='extremes'),
                dcc.Tab(label='📋 Data View', value='dataview'),
                dcc.Tab(label='🔍 Insights', value='insights'),
            ]),
            
            html.Div(id='tab-content', style={'padding': '20px'})
            
        ], style={'width': '75%'})
        
    ], style={'display': 'flex', 'padding': '20px'}),
    
    # Footer
    html.Hr(),
    html.P("Weather Data Analyzer | Built with Dash 🌤️",
           style={'textAlign': 'center', 'color': '#666'})
])


# Callbacks
@app.callback(
    [Output('upload-section', 'style'),
     Output('fetch-section', 'style')],
    Input('data-source', 'value')
)
def toggle_data_source(value):
    if value == 'upload':
        return {'display': 'block'}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'display': 'block'}


@app.callback(
    [Output('stored-data', 'data'),
     Output('status-message', 'children')],
    [Input('upload-data', 'contents'),
     Input('fetch-btn', 'n_clicks')],
    [State('upload-data', 'filename'),
     State('city-dropdown', 'value'),
     State('days-slider', 'value')]
)
def load_data(contents, n_clicks, filename, city, days):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return None, html.Div()
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    try:
        if trigger_id == 'upload-data' and contents:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            df['date'] = pd.to_datetime(df['date'])
            
            message = html.Div(f"✅ File loaded! {len(df)} rows", 
                             style={'padding': '10px', 'backgroundColor': '#d4edda', 
                                   'color': '#155724', 'borderRadius': '5px', 'margin': '10px 0'})
            return df.to_json(date_format='iso', orient='split'), message
            
        elif trigger_id == 'fetch-btn' and n_clicks > 0:
            analyzer.fetch_real_data(city=city, days=days)
            df = analyzer.df
            
            message = html.Div(f"✅ Data fetched for {days} days in {city}!", 
                             style={'padding': '10px', 'backgroundColor': '#d4edda', 
                                   'color': '#155724', 'borderRadius': '5px', 'margin': '10px 0'})
            return df.to_json(date_format='iso', orient='split'), message
            
    except Exception as e:
        message = html.Div(f"❌ Error: {str(e)}", 
                         style={'padding': '10px', 'backgroundColor': '#f8d7da', 
                               'color': '#721c24', 'borderRadius': '5px', 'margin': '10px 0'})
        return None, message
    
    return None, html.Div()


@app.callback(
    Output('info-content', 'children'),
    Input('stored-data', 'data')
)
def update_quick_info(data):
    if data is None:
        return html.Div()
    
    df = pd.read_json(data, orient='split')
    df['date'] = pd.to_datetime(df['date'])
    
    return html.Div([
        html.P(f"Total Records: {len(df)}", style={'fontSize': '14px', 'fontWeight': 'bold'}),
        html.P(f"Columns: {len(df.columns)}", style={'fontSize': '14px', 'fontWeight': 'bold'}),
        html.P(f"Date Range: {df['date'].min().date()} to {df['date'].max().date()}", 
               style={'fontSize': '12px'})
    ])


@app.callback(
    Output('tab-content', 'children'),
    [Input('tabs', 'value'),
     Input('stored-data', 'data')]
)
def render_tab_content(active_tab, data):
    if data is None:
        return html.Div([
            html.P("👈 Please upload a CSV file or fetch data from the sidebar to begin analysis",
                   style={'padding': '20px', 'backgroundColor': '#d1ecf1', 'borderRadius': '5px'}),
            html.H4("Expected CSV Format:"),
            dash_table.DataTable(
                data=[
                    {'date': '2024-01-01', 'temperature': 25.5, 'precipitation': 0, 'wind_speed': 15, 'pressure': 1013},
                    {'date': '2024-01-02', 'temperature': 26.3, 'precipitation': 2.5, 'wind_speed': 18, 'pressure': 1015},
                    {'date': '2024-01-03', 'temperature': 24.8, 'precipitation': 1.2, 'wind_speed': 12, 'pressure': 1012}
                ],
                columns=[{'name': i, 'id': i} for i in ['date', 'temperature', 'precipitation', 'wind_speed', 'pressure']],
                style_table={'overflowX': 'auto'}
            )
        ])
    
    df = pd.read_json(data, orient='split')
    df['date'] = pd.to_datetime(df['date'])
    
    if active_tab == 'statistics':
        return render_statistics(df)
    elif active_tab == 'visualizations':
        return render_visualizations(df)
    elif active_tab == 'extremes':
        return render_extremes(df)
    elif active_tab == 'dataview':
        return render_dataview(df)
    elif active_tab == 'insights':
        return render_insights(df)


def render_statistics(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    children = [html.H3("Summary Statistics")]
    
    for col in numeric_cols:
        stats = html.Div([
            html.H4(col.upper(), style={'color': '#667eea'}),
            html.Div([
                html.Div([
                    html.P("Mean", style={'fontWeight': 'bold'}),
                    html.P(f"{df[col].mean():.2f}")
                ], style={'display': 'inline-block', 'margin': '10px', 'padding': '10px', 
                         'backgroundColor': '#f0f2f6', 'borderRadius': '5px'}),
                
                html.Div([
                    html.P("Median", style={'fontWeight': 'bold'}),
                    html.P(f"{df[col].median():.2f}")
                ], style={'display': 'inline-block', 'margin': '10px', 'padding': '10px', 
                         'backgroundColor': '#f0f2f6', 'borderRadius': '5px'}),
                
                html.Div([
                    html.P("Std Dev", style={'fontWeight': 'bold'}),
                    html.P(f"{df[col].std():.2f}")
                ], style={'display': 'inline-block', 'margin': '10px', 'padding': '10px', 
                         'backgroundColor': '#f0f2f6', 'borderRadius': '5px'}),
                
                html.Div([
                    html.P("Min", style={'fontWeight': 'bold'}),
                    html.P(f"{df[col].min():.2f}")
                ], style={'display': 'inline-block', 'margin': '10px', 'padding': '10px', 
                         'backgroundColor': '#f0f2f6', 'borderRadius': '5px'}),
                
                html.Div([
                    html.P("Max", style={'fontWeight': 'bold'}),
                    html.P(f"{df[col].max():.2f}")
                ], style={'display': 'inline-block', 'margin': '10px', 'padding': '10px', 
                         'backgroundColor': '#f0f2f6', 'borderRadius': '5px'}),
            ])
        ], style={'marginBottom': '30px'})
        
        children.append(stats)
    
    return html.Div(children)


def render_visualizations(df):
    return html.Div([
        html.H3("Data Visualizations"),
        
        dcc.Dropdown(
            id='viz-selector',
            options=[
                {'label': 'Temperature Trend', 'value': 'temp_trend'},
                {'label': 'Monthly Averages', 'value': 'monthly'},
                {'label': 'All Variables', 'value': 'all_vars'},
                {'label': 'Distribution Plots', 'value': 'distribution'}
            ],
            value='temp_trend',
            style={'width': '50%', 'marginBottom': '20px'}
        ),
        
        html.Div(id='viz-content')
    ])


@app.callback(
    Output('viz-content', 'children'),
    [Input('viz-selector', 'value'),
     Input('stored-data', 'data')]
)
def update_visualization(viz_type, data):
    if data is None:
        return html.Div()
    
    df = pd.read_json(data, orient='split')
    df['date'] = pd.to_datetime(df['date'])
    
    if viz_type == 'temp_trend' and 'temperature' in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['date'], y=df['temperature'], 
                                mode='lines', name='Temperature',
                                line=dict(color='#e74c3c', width=2)))
        fig.update_layout(title='Temperature Trend Over Time',
                         xaxis_title='Date', yaxis_title='Temperature (°C)',
                         height=500)
        return dcc.Graph(figure=fig)
    
    elif viz_type == 'monthly' and 'temperature' in df.columns:
        df_copy = df.copy()
        df_copy['month'] = pd.to_datetime(df_copy['date']).dt.month
        monthly_avg = df_copy.groupby('month')['temperature'].mean().reset_index()
        
        month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_avg['month_name'] = monthly_avg['month'].apply(lambda x: month_labels[x-1])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=monthly_avg['month_name'], y=monthly_avg['temperature'],
                            marker_color='skyblue'))
        fig.update_layout(title='Monthly Average Temperature',
                         xaxis_title='Month', yaxis_title='Average Temperature (°C)',
                         height=500)
        return dcc.Graph(figure=fig)
    
    elif viz_type == 'all_vars':
        numeric_cols = [col for col in df.columns if col != 'date' and pd.api.types.is_numeric_dtype(df[col])]
        
        if not numeric_cols:
            return html.P("No numeric columns found")
        
        fig = go.Figure()
        for col in numeric_cols:
            fig.add_trace(go.Scatter(x=df['date'], y=df[col], 
                                    mode='lines', name=col.title()))
        
        fig.update_layout(title='All Weather Variables',
                         xaxis_title='Date', yaxis_title='Value',
                         height=600)
        return dcc.Graph(figure=fig)
    
    elif viz_type == 'distribution':
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        return html.Div([
            dcc.Dropdown(
                id='dist-var-selector',
                options=[{'label': col, 'value': col} for col in numeric_cols],
                value=numeric_cols[0] if numeric_cols else None,
                style={'width': '50%', 'marginBottom': '20px'}
            ),
            html.Div(id='dist-plots')
        ])
    
    return html.Div()


@app.callback(
    Output('dist-plots', 'children'),
    [Input('dist-var-selector', 'value'),
     Input('stored-data', 'data')]
)
def update_distribution(selected_var, data):
    if data is None or selected_var is None:
        return html.Div()
    
    df = pd.read_json(data, orient='split')
    
    fig1 = go.Figure()
    fig1.add_trace(go.Histogram(x=df[selected_var], nbinsx=30,
                               marker_color='skyblue'))
    fig1.update_layout(title=f'Distribution of {selected_var.title()}',
                      xaxis_title=selected_var.title(), yaxis_title='Frequency',
                      height=400)
    
    fig2 = go.Figure()
    fig2.add_trace(go.Box(y=df[selected_var], name=selected_var.title()))
    fig2.update_layout(title=f'Box Plot of {selected_var.title()}',
                      yaxis_title=selected_var.title(),
                      height=400)
    
    return html.Div([
        html.Div(dcc.Graph(figure=fig1), style={'display': 'inline-block', 'width': '48%'}),
        html.Div(dcc.Graph(figure=fig2), style={'display': 'inline-block', 'width': '48%', 'marginLeft': '4%'})
    ])


def render_extremes(df):
    children = [html.H3("🌡️ Extreme Weather Days")]
    
    col1_children = []
    col2_children = []
    
    if 'temperature' in df.columns:
        hottest = df.loc[df['temperature'].idxmax()]
        coldest = df.loc[df['temperature'].idxmin()]
        
        col1_children.extend([
            html.Div([
                html.H4("🔥 Hottest Day", style={'color': 'white'}),
                html.P(f"Date: {hottest['date'].date()}"),
                html.P(f"Temperature: {hottest['temperature']:.2f}°C")
            ], style={'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                     'padding': '20px', 'borderRadius': '10px', 'color': 'white', 'margin': '10px'}),
            
            html.Div([
                html.H4("❄️ Coldest Day", style={'color': 'white'}),
                html.P(f"Date: {coldest['date'].date()}"),
                html.P(f"Temperature: {coldest['temperature']:.2f}°C")
            ], style={'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                     'padding': '20px', 'borderRadius': '10px', 'color': 'white', 'margin': '10px'})
        ])
    
    if 'precipitation' in df.columns:
        wettest = df.loc[df['precipitation'].idxmax()]
        
        col2_children.append(
            html.Div([
                html.H4("💧 Wettest Day", style={'color': 'white'}),
                html.P(f"Date: {wettest['date'].date()}"),
                html.P(f"Precipitation: {wettest['precipitation']:.2f} mm")
            ], style={'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                     'padding': '20px', 'borderRadius': '10px', 'color': 'white', 'margin': '10px'})
        )
    
    if 'wind_speed' in df.columns:
        windiest = df.loc[df['wind_speed'].idxmax()]
        
        col2_children.append(
            html.Div([
                html.H4("💨 Windiest Day", style={'color': 'white'}),
                html.P(f"Date: {windiest['date'].date()}"),
                html.P(f"Wind Speed: {windiest['wind_speed']:.2f} km/h")
            ], style={'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                     'padding': '20px', 'borderRadius': '10px', 'color': 'white', 'margin': '10px'})
        )
    
    children.append(
        html.Div([
            html.Div(col1_children, style={'display': 'inline-block', 'width': '48%', 'verticalAlign': 'top'}),
            html.Div(col2_children, style={'display': 'inline-block', 'width': '48%', 'marginLeft': '4%', 'verticalAlign': 'top'})
        ])
    )
    
    return html.Div(children)


def render_dataview(df):
    return html.Div([
        html.H3("📋 Raw Data View"),
        
        dash_table.DataTable(
            data=df.head(50).to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': '#667eea', 'color': 'white', 'fontWeight': 'bold'},
            page_size=20
        ),
        
        html.Br(),
        html.Button('📥 Download CSV', id='download-btn', n_clicks=0,
                   style={'padding': '10px 20px', 'backgroundColor': '#667eea',
                         'color': 'white', 'border': 'none', 'borderRadius': '5px',
                         'cursor': 'pointer'}),
        dcc.Download(id='download-data')
    ])


@app.callback(
    Output('download-data', 'data'),
    Input('download-btn', 'n_clicks'),
    State('stored-data', 'data'),
    prevent_initial_call=True
)
def download_csv(n_clicks, data):
    if data is None:
        return None
    
    df = pd.read_json(data, orient='split')
    return dcc.send_data_frame(df.to_csv, f"weather_data_{datetime.now().strftime('%Y%m%d')}.csv", index=False)


def render_insights(df):
    insights = [html.H3("🔍 Quick Insights")]
    
    if 'temperature' in df.columns:
        avg_temp = df['temperature'].mean()
        recent_avg = df['temperature'].iloc[-30:].mean() if len(df) >= 30 else df['temperature'].mean()
        temp_trend = "warming" if recent_avg > avg_temp else "cooling"
        
        insights.append(
            html.Div(
                f"📊 The average temperature is {avg_temp:.2f}°C and the recent trend shows {temp_trend}.",
                style={'padding': '15px', 'backgroundColor': '#d1ecf1', 'borderRadius': '5px', 'margin': '10px 0'}
            )
        )
    
    if 'date' in df.columns and 'temperature' in df.columns:
        insights.append(html.H4("🍂 Seasonal Temperature Analysis"))
        
        df_seasonal = df.copy()
        df_seasonal['month'] = pd.to_datetime(df_seasonal['date']).dt.month
        df_seasonal['season'] = df_seasonal['month'].apply(
            lambda x: 'Winter' if x in [12, 1, 2] else
                     'Spring' if x in [3, 4, 5] else
                     'Summer' if x in [6, 7, 8] else 'Fall'
        )
        
        seasonal_avg = df_seasonal.groupby('season')['temperature'].mean().sort_values(ascending=False)
        
        season_divs = []
        for season, temp in seasonal_avg.items():
            season_divs.append(
                html.Div([
                    html.H5(season),
                    html.P(f"{temp:.1f}°C", style={'fontSize': '24px', 'fontWeight': 'bold'})
                ], style={'display': 'inline-block', 'width': '23%', 'margin': '1%',
                         'padding': '15px', 'backgroundColor': '#f0f2f6', 'borderRadius': '5px',
                         'textAlign': 'center'})
            )
        
        insights.append(html.Div(season_divs))
    
    return html.Div(insights)


if __name__ == '__main__':
    app.run( host='0.0.0.0', port=8050)