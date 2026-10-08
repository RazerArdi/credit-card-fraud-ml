import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Note: Run dulu yak..... python build_vector_db.py , in-case bisa pake cd dulu Xd;

# 1. Konfigurasi Path (Mundur 4 tingkat dari /core/build_vector_db.py ke root project)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, 'knowledge_base')
CHROMA_DB_DIR = os.path.join(BASE_DIR, 'chroma_db')

def build_database():
    print(f"Mencari dokumen di: {KNOWLEDGE_BASE_DIR}")
    
    # 2. Load semua PDF dari folder knowledge_base
    loader = PyPDFDirectoryLoader(KNOWLEDGE_BASE_DIR)
    documents = loader.load()
    print(f"Berhasil memuat {len(documents)} halaman dari PDF.")

    if len(documents) == 0:
        print("Error: Tidak ada dokumen PDF yang ditemukan.")
        return

    # 3. Text Splitter (Membagi teks menjadi potongan 1000 karakter agar konteksnya fokus)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Dokumen dipecah menjadi {len(chunks)} chunks.")

    # 4. Inisialisasi Model Embedding Lokal (Ringan dan cepat)
    print("Mengunduh/Memuat model embedding (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 5. Membangun dan Menyimpan Vector Database (Chroma)
    print("Menyimpan ke Vector Database Chroma...")
    vector_store = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=CHROMA_DB_DIR
    )
    
    print(f"Done! Vector Database disimpan di: {CHROMA_DB_DIR}")

if __name__ == "__main__":
    build_database()