import os
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from typing import Any
from pydantic import SecretStr

# 1. Konfigurasi Database Vektor
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")

print("Memuat Model Embedding dan Vector Database untuk RAG...")
# Memuat model embedding yang sama dengan saat ingestion
embeddings = HuggingFaceEmbeddings(model="all-MiniLM-L6-v2")

# Menghubungkan ke ChromaDB yang sudah kita buat sebelumnya
vector_store = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)

# Mengatur retriever untuk mengambil 3 potongan dokumen paling relevan (Top-K = 3)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})


# 2. Logika RAG & LLM
def get_ai_response(user_message: str, chat_history: list, kpi_context: dict) -> str:
    """Memproses pertanyaan pengguna menggunakan metrik real-time dan dokumen RAG."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Sistem Error: GROQ_API_KEY tidak ditemukan di file .env."

    # Inisialisasi LLM
    llm = ChatGroq(
        api_key=SecretStr(api_key), 
        model="openai/gpt-oss-120b", 
        temperature=0.1,
        stop_sequences=None
    )

    # Langkah A: Melakukan pencarian dokumen berdasarkan pertanyaan pengguna
    docs = retriever.invoke(user_message)

    # Merangkai dokumen yang ditemukan menjadi sebuah teks
    if docs:
        retrieved_context = "\n\n".join(
            [
                f"[Sumber: {os.path.basename(d.metadata.get('source', 'Unknown'))}]\n{d.page_content}"
                for d in docs
            ]
        )
    else:
        retrieved_context = (
            "Tidak ada referensi dokumen yang relevan ditemukan di Knowledge Base."
        )

    # Langkah B: Mempersiapkan Metrik Operasional
    kpi_summary = f"""
    - Total Transaksi: {kpi_context['total_trx']:,}
    - Total Nilai Diproses (TPV): ${kpi_context['total_value']:,.2f}
    - Net Savings (ROI): ${kpi_context['net_savings']:,.2f}
    - Customer Friction Rate (FPR): {kpi_context['friction_rate']:.2f}%
    - Loss Prevented (Kerugian Dicegah): ${kpi_context['loss_prevented']:,.2f}
    - Volume Antrean Tinjauan Manual: {kpi_context['fp_volume']}
    """

    # Langkah C: Membangun Prompt LangChain
    system_prompt = """Anda adalah "RiskCommand Copilot", seorang Senior Fraud Analyst dan Compliance Officer AI.
    Tugas Anda adalah memberikan jawaban strategis dan taktis kepada eksekutif bisnis.
    
    Anda memiliki akses ke dua sumber kebenaran mutlak:
    
    1. METRIK OPERASIONAL SAAT INI (Live Data):
    {kpi_summary}
    
    2. DOKUMEN REFERENSI KEPATUHAN & SOP (RAG):
    {retrieved_context}
    
    INSTRUKSI KETAT:
    - Jawablah menggunakan bahasa Indonesia yang profesional, padat, dan analitis.
    - Jika pertanyaan terkait angka, performa, atau ROI, gunakan [METRIK OPERASIONAL SAAT INI].
    - Jika pertanyaan terkait aturan, SOP, atau cara menangani insiden, gunakan [DOKUMEN REFERENSI KEPATUHAN].
    - Selalu kutip nama file sumbernya (contoh: "Menurut POJK 12 Tahun 2024...") jika Anda mengambil informasi dari dokumen RAG.
    - Jika jawaban tidak ada di kedua sumber tersebut, katakan secara jujur bahwa informasi tidak tersedia di sistem. JANGAN mengarang (hallucination).
    """

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )

    # Langkah D: Memformat riwayat percakapan untuk LangChain
    formatted_history: list[Any] = []
    for msg in chat_history:
        if msg["role"] == "user":
            formatted_history.append(HumanMessage(content=msg["content"]))
        else:
            formatted_history.append(AIMessage(content=msg["content"]))

    # Langkah E: Eksekusi Chain LCEL (LangChain Expression Language)
    chain = prompt_template | llm

    try:
        response = chain.invoke(
            {
                "kpi_summary": kpi_summary,
                "retrieved_context": retrieved_context,
                "history": formatted_history,
                "question": user_message,
            }
        )
        return str(response.content)
    except Exception as e:
        return f"Terjadi kesalahan saat menghubungi layanan AI: {str(e)}"
