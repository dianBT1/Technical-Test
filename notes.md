## Design Decisions dan Trade-offs

### Keputusan Desain Utama
Refactoring ini memisahkan kode menjadi beberapa kelas dengan tanggung jawab yang jelas. Pada folder `Services` saya menyimpan semua proses logic utama:
- `QdrantClientService` untuk abstraksi interaksi dengan Qdrant (inisialisasi client, memastikan collection siap, dan operasi upsert/query).
- `DocumentStore` untuk manajemen dokumen dan fallback ke in-memory ketika Qdrant tidak bisa digunakan.
- `EmbeddingServices` untuk mengubah teks menjadi vektor .
- `RagService`  untuk orchestration proses retrieve dan answer menggunakan LangGraph.

Setelah itu, business logic dikumpulkan di `WorkflowController` (folder `Controller`) yang berfungsi sebagai facade: controller ini yang dipanggil oleh `main.py`. Layer API di `main.py` hanya menerima request HTTP dan meneruskannya ke `WorkflowController`, sehingga web layer tetap tipis dan lebih mudah dibaca.

### Salah satu operasi business logic
Ketika user menambah dokumen, business logic di `DocumentStore.add_document_store()` akan:
- Membuat embedding dari teks dengan `EmbeddingServices`.
- Membuat `doc_id` unik dengan UUID.
- Jika `QdrantClientService.is_available()` bernilai **True**, dokumen disimpan ke Qdrant melalui `upsert_document`.
- Jika Qdrant tidak tersedia, dokumen disimpan ke list in-memory sebagai fallback.

Dengan cara ini, aplikasi tetap bisa menerima dan menyimpan dokumen meskipun Qdrant sedang down, tanpa mengubah kontrak API yang dipakai client.

### Peningkatan Maintainability
Versi refactored ini meningkatkan maintainability melalui beberapa cara:
1. **Separation of Concerns** – setiap kelas punya tanggung jawab yang jelas (Qdrant service, embedding service, document store, RAG Servoces, controller), sehingga perubahan di satu area tidak memaksa kita menyentuh seluruh kode.
2. **Encapsulation** – data dan behavior dikelompokkan bersama (contoh: `DocumentStore` mengelola `_docs_memory` dan operasi terkait), sehingga akses ke state lebih terkontrol.
3. **Explicit Dependencies** – dependency utama (Qdrant client, embedding service, document store, RAG workflow) di-pass melalui constructor, sehingga hubungan antar komponen jelas dan bisa di‑mock saat testing.
4. **Readability** – struktur file yang terorganisir dan penamaan yang konsisten membuat kode lebih mudah dipahami oleh developer lain dan memudahkan penambahan unit test karena setiap komponen bisa diuji secara terpisah.

