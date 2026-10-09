from dash import dcc, html
import dash_bootstrap_components as dbc


def render():
    return dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            [
                                html.I(className="bi bi-robot me-2"),
                                "Fraud Analytics Copilot",
                            ],
                            className="fw-bold bg-white text-dark",
                        ),
                        dbc.CardBody(
                            [
                                # Area tampilan chat
                                html.Div(
                                    id="chat-display",
                                    style={
                                        "height": "400px",
                                        "overflowY": "auto",
                                        "padding": "15px",
                                        "backgroundColor": "#f8f9fa",
                                        "borderRadius": "8px",
                                        "border": "1px solid #e2e8f0",
                                        "marginBottom": "15px",
                                    },
                                ),
                                # Area input
                                dbc.InputGroup(
                                    [
                                        dbc.Input(
                                            id="chat-input",
                                            placeholder="Tanyakan analisis tentang ROI, fraud rate, atau tren saat ini...",
                                            type="text",
                                            n_submit=0,  # Memungkinkan tekan 'Enter' untuk kirim
                                        ),
                                        dbc.Button(
                                            "Kirim",
                                            id="chat-submit",
                                            color="primary",
                                            className="fw-bold px-4",
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    className="shadow-sm border-0 mt-4",
                ),
                width=8,
                className="mx-auto",
            )  # Memusatkan tampilan chat
        ]
    )
