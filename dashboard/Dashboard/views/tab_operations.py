from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


def render(df: pd.DataFrame, meta: dict):
    # Peta dan Grafik Tren
    fig_map = px.scatter_map(
        df[df["predicted_fraud"] == 1],
        lat="lat",
        lon="long",
        color="is_fraud",
        size="amt",
        hover_name="merchant",
        hover_data=["category", "amt"],
        color_continuous_scale=[(0, "#F59E0B"), (1, "#D13438")],
        zoom=3.5,
        height=400,
    )
    fig_map.update_layout(
        map_style="carto-positron",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_showscale=False,
    )

    fraud_df = (
        df[df["predicted_fraud"] == 1].groupby("hour").size().reset_index(name="count")
    )
    fig_trend = px.bar(
        fraud_df,
        x="hour",
        y="count",
        labels={"hour": "Hour of Day", "count": "System Alerts"},
        color_discrete_sequence=["#D13438"],
        height=250,
    )
    fig_trend.update_layout(
        margin={"r": 10, "t": 10, "l": 10, "b": 10},
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    # Persiapan Data Antrean Investigasi (Top 10 High Value Alerts)
    alert_df = df[df["predicted_fraud"] == 1][
        ["trans_date_trans_time", "merchant", "category", "amt", "city_pop"]
    ]
    alert_df = alert_df.sort_values("amt", ascending=False).head(10)
    alert_df["amt"] = alert_df["amt"].apply(lambda x: f"${x:,.2f}")
    alert_df["category"] = alert_df["category"].str.replace("_", " ").str.title()
    alert_df.rename(
        columns={
            "trans_date_trans_time": "Timestamp",
            "merchant": "Merchant Name",
            "category": "Category",
            "amt": "Amount",
            "city_pop": "City Population",
        },
        inplace=True,
    )

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "Spatial Anomaly Alerts",
                                    className="fw-bold bg-white",
                                ),
                                dbc.CardBody(
                                    dcc.Graph(figure=fig_map), className="p-0"
                                ),
                            ],
                            className="shadow-sm border-0",
                        ),
                        width=8,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        "Alert Volume by Hour",
                                        className="fw-bold bg-white",
                                    ),
                                    dbc.CardBody(
                                        dcc.Graph(figure=fig_trend), className="p-2"
                                    ),
                                ],
                                className="shadow-sm border-0 mb-3",
                            ),
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        "Active Engine Profile",
                                        className="fw-bold bg-white",
                                    ),
                                    dbc.CardBody(
                                        [
                                            html.Table(
                                                [
                                                    html.Tr(
                                                        [
                                                            html.Th(
                                                                "Engine:",
                                                                className="text-secondary w-50",
                                                            ),
                                                            html.Td(
                                                                f"{meta['model_name']} {meta['version']}",
                                                                className="fw-bold text-dark",
                                                            ),
                                                        ]
                                                    ),
                                                    html.Tr(
                                                        [
                                                            html.Th(
                                                                "Threshold:",
                                                                className="text-secondary",
                                                            ),
                                                            html.Td(
                                                                f"{meta['threshold']}",
                                                                className="fw-bold text-dark",
                                                            ),
                                                        ]
                                                    ),
                                                ],
                                                className="table table-borderless table-sm mb-0 text-small",
                                            )
                                        ]
                                    ),
                                ],
                                className="shadow-sm border-0",
                            ),
                        ],
                        width=4,
                    ),
                ],
                className="mt-4",
            ),
            # TABEL INVESTIGASI
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "Fraud Investigation Queue (High Priority)",
                                    className="fw-bold bg-white text-danger",
                                ),
                                dbc.CardBody(
                                    [
                                        dash_table.DataTable(  # type: ignore
                                            data=alert_df.to_dict("records"),
                                            columns=[
                                                {"name": i, "id": i}
                                                for i in alert_df.columns
                                            ],
                                            style_header={
                                                "backgroundColor": "#f8f9fa",
                                                "fontWeight": "bold",
                                                "border": "none",
                                            },
                                            style_cell={
                                                "textAlign": "left",
                                                "padding": "10px",
                                                "fontFamily": "Inter, sans-serif",
                                                "borderBottom": "1px solid #e2e8f0",
                                            },
                                            style_data={"border": "none"},
                                            style_as_list_view=True,
                                        )
                                    ]
                                ),
                            ],
                            className="shadow-sm border-0",
                        ),
                        width=12,
                    )
                ],
                className="mt-4 mb-4",
            ),
        ]
    )
