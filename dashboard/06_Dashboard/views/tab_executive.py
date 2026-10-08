from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def render(df: pd.DataFrame, kpi: dict):
    # Kalkulasi Tren Bulanan
    monthly_impact = df[df['is_fraud'] == 1].groupby('month').apply(
        lambda x: pd.Series({'Prevented': x[x['predicted_fraud'] == 1]['amt'].sum(), 'Escaped': x[x['predicted_fraud'] == 0]['amt'].sum()})
    ).reset_index()
    
    fig_finance = px.bar(
        monthly_impact, x='month', y=['Prevented', 'Escaped'], title="Monthly Financial Impact",
        color_discrete_map={'Prevented': '#10B981', 'Escaped': '#EF4444'},
        labels={'value': 'USD ($)', 'month': 'Month', 'variable': 'Status'}, height=320, barmode="group"
    )
    fig_finance.update_layout(margin={"r":10,"t":40,"l":10,"b":10}, plot_bgcolor="white", paper_bgcolor="white", legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    # Kalkulasi Profil Risiko (Kategori Teratas)
    fraud_category = df[df['is_fraud'] == 1].groupby('category')['amt'].sum().reset_index().sort_values('amt', ascending=True).tail(5)
    fraud_category['category'] = fraud_category['category'].str.replace('_', ' ').str.title()
    fig_cat = px.bar(
        fraud_category, x='amt', y='category', orientation='h', title="Top Fraud Loss by Category",
        labels={'amt': 'Total Loss ($)', 'category': ''}, color_discrete_sequence=['#F59E0B'], height=320
    )
    fig_cat.update_layout(margin={"r":10,"t":40,"l":10,"b":10}, plot_bgcolor="white", paper_bgcolor="white")

    card_style = {"border-radius": "8px", "box-shadow": "0 2px 4px rgba(0,0,0,0.05)", "height": "100%"}
    
    return html.Div([
        # SEGMEN 1: FINANCIAL OVERVIEW
        html.H5("Financial Overview", className="fw-bold text-dark mt-4 mb-3"),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([html.P("Total Processed Value (TPV)", className="text-secondary mb-1 fw-bold"), html.H3(f"${kpi['total_value']:,.0f}", className="text-dark mb-0")]), style=card_style), width=3),
            dbc.Col(dbc.Card(dbc.CardBody([html.P("Net Business Value (ROI)", className="text-secondary mb-1 fw-bold"), html.H3(f"${kpi['net_savings']:,.0f}", className="text-success mb-0")]), style=card_style), width=3),
            dbc.Col(dbc.Card(dbc.CardBody([html.P("Gross Loss Prevented", className="text-secondary mb-1 fw-bold"), html.H3(f"${kpi['loss_prevented']:,.0f}", className="text-primary mb-0")]), style=card_style), width=3),
            dbc.Col(dbc.Card(dbc.CardBody([html.P("Loss Escaped", className="text-secondary mb-1 fw-bold"), html.H3(f"${kpi['loss_escaped']:,.0f}", className="text-danger mb-0")]), style=card_style), width=3),
        ], className="mb-4"),
        
        # SEGMEN 2: OPERATIONAL EFFICIENCY
        html.H5("Operational Efficiency", className="fw-bold text-dark mb-3"),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([html.P("System Approval Rate", className="text-secondary mb-1 fw-bold"), html.H3(f"{kpi['approval_rate']:.2f}%", className="text-success mb-0")]), style=card_style), width=3),
            dbc.Col(dbc.Card(dbc.CardBody([html.P("Customer Friction Rate", className="text-secondary mb-1 fw-bold"), html.H3(f"{kpi['friction_rate']:.2f}%", className="text-warning mb-0")]), style=card_style), width=3),
            dbc.Col(dbc.Card(dbc.CardBody([html.P("Manual Review Volume", className="text-secondary mb-1 fw-bold"), html.H3(f"{kpi['fp_volume']:,}", className="text-dark mb-0")]), style=card_style), width=3),
            dbc.Col(dbc.Card(dbc.CardBody([html.P("Review OpEx (Estimated)", className="text-secondary mb-1 fw-bold"), html.H3(f"${kpi['review_cost']:,.0f}", className="text-danger mb-0")]), style=card_style), width=3),
        ], className="mb-4"),

        # SEGMEN 3: TRENDS & RISK PROFILING
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(figure=fig_finance)), className="shadow-sm border-0", style={"border-radius": "8px"}), width=7),
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(figure=fig_cat)), className="shadow-sm border-0", style={"border-radius": "8px"}), width=5),
        ], className="mb-4")
    ])