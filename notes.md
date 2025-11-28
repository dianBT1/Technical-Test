## Design Decisions dan Trade-offs
### Keputusan Desain Utama
Refactoring ini memisahkan kode menjadi beberapa kelas dengan tanggung jawab yang jelas. Pada folder `Services` saya menyimpan semua proses logic utama:
- `QdrantClientService` untuk abstraksi interaksi dengan Qdrant (inisialisasi client, memastikan collection siap, dan operasi upsert/query).
- `DocumentStore` untuk manajemen dokumen dan fallback ke in-memory ketika Qdrant tidak bisa digunakan.
- `EmbeddingServices` untuk mengubah teks menjadi vektor .
- `RagService`  untuk orchestration proses retrieve dan answer menggunakan LangGraph.

Setelah itu, business logic dikumpulkan di `WorkflowController` (folder `Controller`) yang berfungsi sebagai facade: controller ini yang dipanggil oleh `main.py`. Layer API di `main.py` hanya menerima request HTTP dan meneruskannya ke `WorkflowController`, sehingga web layer tetap tipis dan lebih mudah dibaca.

### Trade-offs yang Dipertimbangkan
**1. Singleton Pattern vs Dependency Injection**
**Pilihan yang dipakai (Singleton):**
- Instance `workflowcontroller` dibuat sekali di level module (`Controller/WorkflowController.py`)
- Langsung di-import dan dipakai di `main.py` tanpa setup tambahan
- ✅ **Keuntungan:** Kode lebih sederhana, mudah ditulis, tidak perlu setup dependency injection

**Alternatif (Dependency Injection via FastAPI Depends):**
- Setiap endpoint inject dependencies melalui `Depends()`
- ✅ **Keuntungan:** Lebih mudah untuk testing, bisa ganti dengan mock, lebih fleksibel

**2. Auto-Recovery dengan Fallback ke Memory**
**Pilihan yang dipakai (Optimistic Approach dengan Fallback):**
- Utamakan untuk memakai database qdrant
- Jika gagal, otomatis fallback ke in-memory storage
- Auto-reconnect jika Qdrant down lalu hidup lagi
- ✅ **Keuntungan:** Aplikasi tetap jalan meski Qdrant down, user experience lebih baik, resilient
- ❌ **Kekurangan:** Load time cukup lama karena harus mengecek qdrantnya aktif atau tidak terlebih dahulu

### Peningkatan Maintainability
Versi refactored ini meningkatkan maintainability melalui beberapa cara:
1. **Separation of Concerns** – setiap kelas punya tanggung jawab yang jelas (Qdrant service, embedding service, document store, RAG Servoces, controller), sehingga perubahan di satu area tidak memaksa kita menyentuh seluruh kode.
2. **Encapsulation** – data dan behavior dikelompokkan bersama (contoh: `DocumentStore` mengelola `_docs_memory` dan operasi terkait), sehingga akses ke state lebih terkontrol.
3. **Explicit Dependencies** – dependency utama (Qdrant client, embedding service, document store, RAG workflow) di-pass melalui constructor, sehingga hubungan antar komponen jelas dan bisa di‑mock saat testing.
4. **Readability** – struktur file yang terorganisir dan penamaan yang konsisten membuat kode lebih mudah dipahami oleh developer lain 

