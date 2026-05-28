# index_docs.py
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_astradb import AstraDBVectorStore

from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredExcelLoader 
)
import time

# ── Konfigurasi ──────────────────────────────────────────
FOLDER_PATH    = ""
ASTRA_TOKEN    = ""
ASTRA_ENDPOINT = ""
COLLECTION     = "my_docs"
GOOGLE_API_KEY = ""

# ── Load semua file secara recursive ─────────────────────
extensions = {
    "pdf"  : PyPDFLoader,
    "docx" : Docx2txtLoader,
    "txt"  : TextLoader,
    "xlsx" : UnstructuredExcelLoader,  
}

docs = []
for ext, loader_cls in extensions.items():
    loader = DirectoryLoader(
        FOLDER_PATH,
        glob=f"**/*.{ext}",
        loader_cls=loader_cls,          
        recursive=True,
        show_progress=True,
        silent_errors=True
    )
    loaded = loader.load()
    docs.extend(loaded)
    print(f"  {ext.upper()}: {len(loaded)} dokumen")  

print(f"\nTotal dokumen dimuat: {len(docs)}")
# ── Chunking ──────────────────────────────────────────────

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(docs)  
print(f"Total chunks: {len(chunks)}")

embedding = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY
)

vectorstore = AstraDBVectorStore(
    embedding=embedding,
    collection_name=COLLECTION,
    token=ASTRA_TOKEN,
    api_endpoint=ASTRA_ENDPOINT,
)

# ── Upload chunks ─────────────
BATCH_SIZE = 50  
DELAY_SECONDS = 20  

total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE

for i in range(0, len(chunks), BATCH_SIZE):
    batch = chunks[i:i + BATCH_SIZE]
    batch_num = (i // BATCH_SIZE) + 1
    
    try:
        vectorstore.add_documents(batch)
        print(f"✅ Batch {batch_num}/{total_batches} selesai ({len(batch)} chunks)")
    except Exception as e:
        print(f"❌ Batch {batch_num} error: {e}")
        print(f"   Menunggu 30 detik lalu retry...")
        time.sleep(30)
        vectorstore.add_documents(batch)  # retry sekali
        print(f"✅ Batch {batch_num} retry berhasil")
    
    # Jeda antar batch kecuali batch terakhir
    if i + BATCH_SIZE < len(chunks):
        print(f"   Menunggu {DELAY_SECONDS} detik...")
        time.sleep(DELAY_SECONDS)

print(f"\n✅ Indexing selesai! Total {len(chunks)} chunks tersimpan di AstraDB.")