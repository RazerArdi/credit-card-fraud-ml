from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


def render(df: pd.DataFrame, kpi: dict, meta: dict):
    # 1. Confusion Matrix
    cm_data = pd.DataFrame(
        {
            "Category": ["Caught Fraud (TP)", "False Alarms (FP)", "Missed Fraud (FN)"],
            "Volume": [kpi["tp_volume"], kpi["fp_volume"], kpi["fn_volume"]],
        }
    )
    fig_cm = px.bar(
        cm_data,
        x="Volume",
        y="Category",
        orientation="h",
        title="Operational Classification Breakdown",
        color="Category",
        color_discrete_map={
            "Caught Fraud (TP)": "#10B981",
            "False Alarms (FP)": "#F59E0B",
            "Missed Fraud (FN)": "#EF4444",
        },
        height=280,
    )
    fig_cm.update_layout(
        showlegend=False,
        margin={"r": 10, "t": 40, "l": 10, "b": 10},
        plot_bgcolor="white",
    )

    # 2. XAI / Feature Importance (Simulasi nilai SHAP dari eksperimen LightGBM Anda)
    shap_mock = pd.DataFrame(
        {
            "Feature": [
                "Transaction Amount (amt)",
                "Distance to Merchant (distance_km)",
                "Merchant Category",
                "Customer Age",
                "Hour of Day",
            ],
            "Importance": [0.45, 0.28, 0.15, 0.08, 0.04],
        }
    ).sort_values("Importance", ascending=True)

    fig_shap = px.bar(
        shap_mock,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Global Feature Importance (SHAP Values)",
        labels={"Importance": "Mean |SHAP| Value (Impact on Model Output)"},
        color_discrete_sequence=["#3B82F6"],
        height=280,
    )
    fig_shap.update_layout(
        margin={"r": 10, "t": 40, "l": 10, "b": 10}, plot_bgcolor="white"
    )

    return html.Div(
        [
            dbc.Row(
                [
                    # Metrik Teknis
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "Core Metrics",
                                    className="fw-bold bg-white text-dark",
                                ),
                                dbc.CardBody(
                                    [
                                        html.H6(
                                            "Training PR-AUC",
                                            className="text-secondary mb-1",
                                        ),
                                        html.H4(
                                            meta["pr_auc"],
                                            className="text-primary mb-3",
                                        ),
                                        html.H6(
                                            "Operational Precision",
                                            className="text-secondary mb-1",
                                        ),
                                        html.H4(
                                            "91.00%", className="text-primary mb-3"
                                        ),
                                        html.H6(
                                            "Operational Recall",
                                            className="text-secondary mb-1",
                                        ),
                                        html.H4("77.00%", className="text-primary"),
                                    ]
                                ),
                            ],
                            className="shadow-sm border-0 h-100",
                        ),
                        width=3,
                    ),
                    # Confusion Matrix
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(dcc.Graph(figure=fig_cm)),
                            className="shadow-sm border-0 h-100",
                        ),
                        width=4,
                    ),
                    # Explainable AI (SHAP)
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(dcc.Graph(figure=fig_shap)),
                            className="shadow-sm border-0 h-100",
                        ),
                        width=5,
                    ),
                ],
                className="mt-4 mb-4",
            )
        ]
    )
