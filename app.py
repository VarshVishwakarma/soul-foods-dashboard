from dash import Dash, html, dcc, Input, Output, callback, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. DATA PREPARATION & ENRICHMENT ---
df = pd.read_csv("pink_morsels_sales.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by="date")

# Define business events for annotations
BUSINESS_EVENTS = [
    {'date': '2024-03-15', 'label': 'Spring Campaign', 'text': 'Q1 Marketing Push'},
    {'date': '2024-07-04', 'label': 'Summer Festival', 'text': 'Increased regional foot traffic'},
    {'date': '2024-11-28', 'label': 'Holiday Launch', 'text': 'New packaging introduced'}
]

app = Dash(__name__)

# --- 2. LAYOUT DESIGN ---
app.layout = html.Div(id="app-container", children=[
    
    # Header Section
    html.Div(id="header-section", children=[
        html.H1("Pink Morsels Executive Performance Suite", id="header"),
        html.P("Soul Foods Strategic Analytics - Confidential", className="sub-header"),
    ]),

    # 1. Product Framing Panel (Collapsible)
    html.Details([
        html.Summary("How to Read This Dashboard & Strategic Intent"),
        html.Div(className="framing-content", children=[
            html.P("Purpose: This dashboard monitors regional elasticity and sales velocity for Pink Morsels."),
            html.Ul([
                html.Li("KPIs: Use 'Volatility' to identify supply chain or demand instability."),
                html.Li("Decisions: Supports inventory allocation and marketing spend ROI analysis.")
            ])
        ])
    ], className="info-panel"),

    # 2. Executive KPI Command Bar
    html.Div(id="kpi-container", className="grid-4-col"),

    # 3. Auto-Generated Insight Summary
    html.Div(id="insight-summary", className="insight-box"),

    # 4. Global Controls
    html.Div(id="control-panel", className="flex-row", children=[
        html.Div([
            html.Label("Regional Perimeter:"),
            dcc.RadioItems(
                id="region-filter",
                options=[{"label": r.capitalize(), "value": r} for r in ['north', 'east', 'south', 'west']] + [{"label": "All Regions", "value": "all"}],
                value="all", inline=True
            ),
        ], className="control-group"),
        
        html.Div([
            html.Label("Analysis Period:"),
            dcc.DatePickerRange(
                id='date-picker',
                min_date_allowed=df['date'].min(),
                max_date_allowed=df['date'].max(),
                start_date=df['date'].min(),
                end_date=df['date'].max()
            ),
        ], className="control-group"),

        html.Div([
            html.Label("Smoothing:"),
            dcc.Checklist(id='smoothing-toggle', options=[{'label': '30D Rolling Average', 'value': 'roll'}], value=[])
        ], className="control-group")
    ]),

    # 5. Visual Intelligence Primary Chart
    dcc.Graph(id="main-timeseries-chart"),

    # 6. Comparative Intelligence (Multi-Region)
    html.Div([
        html.H3("Cross-Regional Velocity Comparison"),
        dcc.Graph(id="comparative-chart")
    ], className="chart-card")
])

# --- 3. BUSINESS LOGIC CALLBACKS ---

@callback(
    [Output("kpi-container", "children"),
     Output("insight-summary", "children"),
     Output("main-timeseries-chart", "figure"),
     Output("comparative-chart", "figure")],
    [Input("region-filter", "value"),
     Input("date-picker", "start_date"),
     Input("date-picker", "end_date"),
     Input("smoothing-toggle", "value")]
)
def update_dashboard(region, start, end, smoothing):
    # Filter base data
    mask = (df['date'] >= start) & (df['date'] <= end)
    filtered_df = df.loc[mask]
    
    # 1. KPI Calculations
    region_df = filtered_df if region == 'all' else filtered_df[filtered_df['region'] == region]
    total_rev = region_df['sales'].sum()
    volatility = region_df['sales'].std()
    
    best_region = filtered_df.groupby('region')['sales'].sum().idxmax()
    
    # Mock growth calc (Current vs Previous half of selected range)
    midpoint = len(region_df) // 2
    growth = ((region_df['sales'].tail(midpoint).mean() / region_df['sales'].head(midpoint).mean()) - 1) * 100

    kpi_cards = [
        html.Div([html.Small("Total Revenue"), html.H2(f"${total_rev:,.0f}")], className="kpi-card"),
        html.Div([html.Small("Growth (Range Split)"), html.H2(f"{growth:+.1f}%", style={'color': 'green' if growth > 0 else 'red'})], className="kpi-card"),
        html.Div([html.Small("Market Leader"), html.H2(best_region.capitalize())], className="kpi-card"),
        html.Div([html.Small("Sales Volatility"), html.H2(f"{volatility:.1f}")], className="kpi-card"),
    ]

    # 2. Insight Generation
    avg_sales = filtered_df['sales'].mean()
    perf_status = "outperforming" if region_df['sales'].mean() > avg_sales else "underperforming"
    insight_text = f"Strategic Summary: The {region if region != 'all' else 'Global'} portfolio is currently {perf_status} the historical baseline. "
    if volatility > 150:
        insight_text += "High volatility detected; recommend reviewing supply chain buffer stocks."

    # 3. Main Chart with Smoothing & Annotations
    fig_main = go.Figure()
    fig_main.add_trace(go.Scatter(x=region_df['date'], y=region_df['sales'], name="Raw Sales", line=dict(color='#cbd5e1', width=1)))
    
    if 'roll' in smoothing:
        fig_main.add_trace(go.Scatter(x=region_df['date'], y=region_df['sales'].rolling(30).mean(), name="30D Trend", line=dict(color='#0f172a', width=3)))

    # Add Event Annotations
    for ev in BUSINESS_EVENTS:
        fig_main.add_vline(x=ev['date'], line_dash="dash", line_color="gray")
        fig_main.add_annotation(x=ev['date'], y=1, text=ev['label'], showarrow=False, yref="paper")

    fig_main.update_layout(title="Sales Signal Analysis", template="simple_white", hovermode="x unified")

    # 4. Comparative Intelligence Chart
    comp_df = filtered_df.groupby(['date', 'region'])['sales'].sum().reset_index()
    fig_comp = px.line(comp_df, x='date', y='sales', color='region', 
                       color_discrete_map={'north': '#1e40af', 'east': '#9333ea', 'south': '#059669', 'west': '#dc2626'})
    fig_comp.update_layout(template="simple_white", showlegend=True)

    return kpi_cards, insight_text, fig_main, fig_comp

if __name__ == "__main__":
    app.run(debug=True)