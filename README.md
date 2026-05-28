# AI-Smart-Documents-Finder
Smart Documents Finder is a smart solution to solve file management problems on the computer. Many users often save documents carelessly, either using file names that do not match the contents or putting them in random folders.

This application makes it easier to search for documents by:
1. Users simply enter a description or keywords related to the content of the document they are looking for.
2. The AI Agent will analyze all documents stored in the our local data.
3. The AI looks for matches based on the context and meaning of the file's content, not just the title.
4. The system will display the file name, storage location (path), along with the reason why that specific file was selected.


-------- CARA KERJA ---------
(language: Bahasa Indonesia)

[MASALAH YANG DISELESAIKAN]

User ingin mencari dokumen di PC-nya hanya dengan mendeskripsikan isinya,
tanpa perlu ingat nama file atau lokasi folder.


[PHASE 1 — INDEXING]
Jalankan sekali via terminal (untuk indexingDATA.py)
! setelah masukkan path storage & database API

Folder Lokal (recursive)
    │  Membaca semua file PDF, DOCX, TXT, XLSX
    ↓
Chunking
    │  Memotong dokumen panjang menjadi potongan 500 kata
    │  agar pencarian lebih presisi
    ↓
Embedding
    │  Mengubah setiap potongan teks menjadi vector angka
    │  menggunakan Gemini text-embedding-004
    ↓
AstraDB
    │  Menyimpan vector + metadata (file_name, path)
    │  secara permanen di cloud


[PHASE 2 — QUERY]
Berjalan di Langflow setiap ada input user

User mengetik prompt
    │  "Carikan dokumen yang membahas future personal plan saya"
    ↓
AstraDB (Similarity Search)
    │  Mengubah prompt menjadi vector
    │  lalu mencari vector paling mirip di database
    ↓
Parser
    │  Mengekstrak teks dan metadata
    │  dari dokumen yang ditemukan
    ↓
Prompt Template
    │  Menggabungkan hasil pencarian (context)
    │  dengan prompt asli user (query)
    ↓
Agent — Gemini 2.5 Flash
    │  Menganalisis dan menentukan
    │  dokumen mana yang paling relevan
    ↓
Chat Output
    │  Mengembalikan file_name, path, dan alasan
    │  mengapa dokumen tersebut relevan


[HASIL AKHIR]
User mendapat jawaban:
- File Name : future_plan_nicky.docx
- File Path : C:/Users/future_plan_nicky.docx
- Alasan    : Dokumen ini membahas rencana pribadi jangka panjang Nicky
