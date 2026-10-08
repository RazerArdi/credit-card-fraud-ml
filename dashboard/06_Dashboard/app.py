import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from dotenv import load_dotenv

# Memuat konfigurasi dari file .env
load_dotenv()

# Mengimpor modul MVC
from core import data_pipeline, ai_assistant
from views import tab_executive, tab_operations, tab_performance, tab_ai

# 1. Inisialisasi Aplikasi
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN, dbc.icons.BOOTSTRAP])
app.title = "Fraud Analytics Dashboard"

# 2. Pemuatan Data Global
SYSTEM_META = data_pipeline.fetch_system_metadata()
df_operational = data_pipeline.load_and_prep_data()
KPI_DATA = data_pipeline.get_kpis(df_operational)

# 3. Tata Letak Utama
app.layout = dbc.Container([
    # Store untuk menyimpan riwayat percakapan AI di browser pengguna
    dcc.Store(id="chat-history-store", data=[]),
    
    # Header
    dbc.Row([
        dbc.Col([
            html.H3("Fraud Analytics Dashboard", className="fw-bold text-primary mb-0 mt-4"),
            html.P("Enterprise Risk Management", className="text-secondary")
        ], width=8),
        dbc.Col([
            html.Div([
                html.I(className="bi bi-circle-fill text-success me-2"),
                html.Span(f"System Status: Online", className="text-muted fw-bold")
            ], className="text-end mt-4 pt-2")
        ], width=4)
    ], className="mb-3 border-bottom pb-2"),

    # Tabs
    dbc.Tabs([
        dbc.Tab(tab_executive.render(df_operational, KPI_DATA), label="Executive Summary", tab_id="tab-executive", tab_class_name="fw-bold text-secondary", active_tab_class_name="text-primary"),
        dbc.Tab(tab_operations.render(df_operational, SYSTEM_META), label="Operations Monitor", tab_id="tab-operations", tab_class_name="fw-bold text-secondary", active_tab_class_name="text-primary"),
        dbc.Tab(tab_performance.render(df_operational, KPI_DATA, SYSTEM_META), label="Model Performance", tab_id="tab-performance", tab_class_name="fw-bold text-secondary", active_tab_class_name="text-primary"),
        dbc.Tab(tab_ai.render(), label="AI Copilot", tab_id="tab-ai", tab_class_name="fw-bold text-secondary", active_tab_class_name="text-primary")
    ], active_tab="tab-executive")
], fluid=True, style={"background-color": "#f8f9fa", "min-height": "100vh", "padding": "2rem"})

# 4. Callback untuk AI Chat
@app.callback(
    [Output("chat-display", "children"), Output("chat-history-store", "data"), Output("chat-input", "value")],
    [Input("chat-submit", "n_clicks"), Input("chat-input", "n_submit")],
    [State("chat-input", "value"), State("chat-history-store", "data")]
)
def update_chat(n_clicks, n_submit, user_message, chat_history):
    # Jika tidak ada trigger (baru dimuat)
    if not user_message or (n_clicks is None and n_submit is None):
        return [html.Div("Halo! Saya adalah AI Copilot Anda. Ada yang bisa saya bantu terkait analisis performa model atau ROI saat ini?", className="text-muted text-center mt-3")], chat_history, ""
    
    # Render chat pengguna
    new_history = chat_history + [{"role": "user", "content": user_message}]
    
    # Ambil respons dari Groq dengan memberikan konteks KPI dari data_pipeline
    ai_response_text = ai_assistant.get_ai_response(user_message, chat_history, KPI_DATA)
    new_history.append({"role": "assistant", "content": ai_response_text})
    
    # Bangun elemen UI untuk riwayat percakapan
    chat_ui_elements = []
    for msg in new_history:
        if msg["role"] == "user":
            # Tampilan chat pengguna (tetap menggunakan Span biasa karena teks biasa)
            chat_ui_elements.append(html.Div([
                html.Span(msg["content"], style={
                    "backgroundColor": "#0d6efd", "color": "white", 
                    "padding": "8px 15px", "borderRadius": "15px", 
                    "display": "inline-block", "maxWidth": "80%"
                })
            ], className="text-end mb-3"))
        else:
            # Tampilan chat AI (Menggunakan dcc.Markdown agar tabel & bold terbaca)
            chat_ui_elements.append(html.Div([
                html.Div(dcc.Markdown(msg["content"], style={"margin": "0"}), style={
                    "backgroundColor": "#e9ecef", "color": "#212529", 
                    "padding": "12px 15px", "borderRadius": "15px", 
                    "display": "inline-block", "maxWidth": "85%",
                    "overflowX": "auto", # Agar tabel yang panjang bisa di-scroll ke samping
                    "fontSize": "0.95rem"
                })
            ], className="text-start mb-3"))
            
    return chat_ui_elements, new_history, ""

if __name__ == '__main__':
    app.run(debug=True, port=8050)