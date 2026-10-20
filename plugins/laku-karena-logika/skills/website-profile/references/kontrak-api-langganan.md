# Kontrak API langganan (modal Harga → QRIS → akun aktif)

Website Timebase adalah situs statis. Modal langganan di `/harga` memanggil API backend berikut.
**Webhook payment gateway diterima backend**, bukan oleh website.

Isi `site.json` → `"langganan": {"api": "https://<domain-backend>/langganan"}` lalu build ulang.
Selama `api` kosong, modal memakai mode sementara (pesanan dikirim lewat WhatsApp).

## Alur

```
Pengunjung pilih paket → isi data → [POST /orders] → QRIS tampil + hitung mundur
      ↓ modal cek status tiap 3 detik [GET /orders/{order_id}]
Pengunjung bayar → gateway kirim webhook ke backend → backend: status "paid" + aktifkan akun
      ↓
Modal: "Pembayaran diterima" + tombol "Masuk ke Timebase" (login_url / site.json signin_url)
```

## 1. Buat pesanan: `POST {api}/orders`

Request body (JSON):

| Field | Tipe | Contoh | Catatan |
|---|---|---|---|
| `paket` | number | `2` | id paket di `data/pricing.json` (1 Aktivitas, 2 Bukti Visual, 3 Waktu Per Tugas) |
| `periode` | string | `"bulanan"` / `"tahunan"` | tahunan = harga bulanan × 10, untuk 12 bulan |
| `karyawan` | number | `25` | 1–999 |
| `addon` | string[] | `["Presensi & lokasi"]` | nama add-on, boleh kosong |
| `nama` | string | `"Budi"` | |
| `perusahaan` | string | `"PT Contoh"` | |
| `whatsapp` | string | `"081234567890"` | angka saja, boleh diawali `+`, 9–15 digit |

Response `201` (JSON):

```json
{
  "order_id": "TB-20261004-0001",
  "amount": 350000,
  "expires_at": "2026-10-04T15:30:00+07:00",
  "qris_image": "https://…/qris.png"
}
```

- Isi **salah satu** dari `qris_image` (URL atau data URI gambar) atau `qris_string` (payload QRIS mentah). Bila `qris_string`, modal membuat gambar QR sendiri.
- **`amount` wajib dihitung ulang di server** dari harga resmi. Angka di modal hanya perkiraan, dan modal menampilkan `amount` dari server.
- Status selain 2xx, atau tanpa `order_id`/QRIS, membuat modal menampilkan "QRIS belum bisa dibuat" + tombol coba lagi.

## 2. Cek status: `GET {api}/orders/{order_id}`

Response (JSON):

```json
{ "status": "pending", "login_url": "https://app.timebase.id/login" }
```

| `status` | Tampilan di modal |
|---|---|
| `pending` | tetap menunggu, cek lagi 3 detik kemudian |
| `paid` | langkah sukses: "Pembayaran diterima" + tombol masuk ke `login_url` (atau `site.json signin_url`) |
| `expired` | QR diredupkan, "Waktu pembayaran habis" + tombol "Buat QRIS baru" |
| `failed` | "Pembayaran gagal" + tombol "Buat QRIS baru" |

## Kebutuhan backend

- **CORS:** izinkan origin website (mis. `https://timebase.id`) untuk `POST /orders` dan `GET /orders/*`.
- **Webhook gateway:** verifikasi tanda tangan/secret dari gateway, cocokkan `order_id` + nominal, lalu set `paid` dan aktifkan akun (tenant, user admin dari `nama`/`whatsapp`).
- **Idempoten:** webhook bisa terkirim lebih dari sekali, jadi jangan membuat akun ganda.
- **Kedaluwarsa:** QRIS sebaiknya berlaku ±15 menit (`expires_at`), lalu status menjadi `expired`.
- Kirim info login ke WhatsApp pelanggan dari backend bila diperlukan. Modal tidak menjanjikan hal ini.
