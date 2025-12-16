# Bancakan 2025 - API Billing Demo

API billing demo menggunakan FastAPI dan Lago untuk manajemen billing berbasis usage-based pricing.

## 🚀 Fitur

- **Authentication System**: Register dan login dengan API key
- **Usage-Based Billing**: Integrasi dengan Lago untuk tracking penggunaan
- **Credit System**: Wallet-based credit management
- **WhatsApp Messaging API**: Endpoint untuk mengirim pesan (dummy implementation)
- **Credit Checking**: Endpoint untuk mengecek saldo kredit

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.11+ (untuk development lokal)

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite
- **Billing**: Lago (self-hosted)
- **Authentication**: API Key based
- **ORM**: SQLAlchemy

## 📦 Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd bancakan2025
```

### 2. Setup Environment Variables

Copy file `.env.example` menjadi `.env` dan sesuaikan konfigurasi sesuai kebutuhan:

```bash
cp .env.example .env
```

**Catatan Penting:**
- File `.env.example` sudah berisi konfigurasi default untuk development
- Pastikan untuk mengubah nilai-nilai sensitif seperti:
  - `POSTGRES_PASSWORD`: Password database PostgreSQL
  - `SECRET_KEY_BASE`: Secret key untuk enkripsi (generate dengan `openssl rand -hex 64`)
  - `LAGO_RSA_PRIVATE_KEY`: (generate dengan `openssl genrsa 2048 | base64 | tr -d '\n'`)
  - `LAGO_ENCRYPTION_PRIMARY_KEY`: (generate dengan `openssl rand -hex 32`)
  - `LAGO_ENCRYPTION_DETERMINISTIC_KEY`: (generate dengan `openssl rand -hex 32`)
  - `LAGO_ENCRYPTION_KEY_DERIVATION_SALT`: (generate dengan `openssl rand -hex 32`)
  - `LAGO_ORG_API_KEY`: API key dari Lago organization
  - `LAGO_ORG_USER_EMAIL` dan `LAGO_ORG_USER_PASSWORD`: Kredensial admin Lago

### 3. Run dengan Docker Compose

```bash
docker-compose up -d
```

Ini akan menjalankan:
- **backend-api**: FastAPI application (port 8000)
- **lago-api**: Lago API server (port 3000)
- **lago-front**: Lago Frontend UI (port 80)
- **lago-db**: PostgreSQL database
- **lago-redis**: Redis cache
- **lago-worker**: Background worker
- **lago-clock**: Scheduled tasks

### 4. Akses Aplikasi

- **API Documentation**: http://localhost:8000/docs
- **Lago Frontend**: http://localhost:8001 (sesuai `FRONT_PORT` di `.env`)
- **Lago API**: http://localhost:3000

## 🔧 Development Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Locally

```bash
uvicorn app.main:app --reload
```

## 📚 API Endpoints

### Authentication

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "message": "logged in",
  "api_key": "your_api_key_here"
}
```

### Messaging

#### Send WhatsApp Message
```http
POST /v1/message
x-api-key: your_api_key_here
Content-Type: application/json

{
  "phone_number": "+6281234567890",
  "message": "Hello World"
}
```

**Note**: Saat ini implementasi WhatsApp masih dummy. Setiap pengiriman pesan akan:
1. Mengecek saldo kredit (minimal 100 credits)
2. Mengirim pesan (dummy)
3. Mengirim event ke Lago untuk mengurangi credit

#### Check Credits
```http
GET /v1/check-credits
x-api-key: your_api_key_here
```

Response:
```json
{
  "message": "credits checked",
  "credits": 1000.0
}
```

## 🏗️ Project Structure

```
bancakan2025/
├── app/
│   ├── api/
│   │   ├── auth.py          # Authentication endpoints
│   │   └── message.py       # Messaging endpoints
│   ├── core/
│   │   ├── database.py      # Database configuration
│   │   ├── deps.py          # Dependency injection
│   │   └── init_db.py       # Database initialization
│   ├── models/
│   │   └── user.py          # User model
│   ├── services/
│   │   ├── auth.py          # Authentication service
│   │   ├── lago.py          # Lago integration
│   │   └── whatsapp.py      # WhatsApp service (dummy)
│   └── main.py              # FastAPI application
├── data/
│   └── app.db               # SQLite database
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile               # Docker image configuration
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🔐 Authentication Flow

1. User register dengan email dan password
2. System membuat:
   - User di database lokal
   - Customer di Lago
   - Wallet di Lago
   - Subscription di Lago
3. User login untuk mendapatkan API key
4. API key digunakan untuk autentikasi di semua endpoint

## 💳 Billing Flow

1. User mengirim request ke API (contoh: send message)
2. System mengecek saldo kredit di wallet
3. Jika cukup, request diproses
4. Event dikirim ke Lago untuk mengurangi credit
5. Lago mencatat usage dan mengurangi balance

## 🧪 Testing

### Test Register
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123"}'
```

### Test Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123"}'
```

### Test Send Message
```bash
curl -X POST http://localhost:8000/v1/message \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{"phone_number": "+6281234567890", "message": "Hello"}'
```

### Test Check Credits
```bash
curl -X GET http://localhost:8000/v1/check-credits \
  -H "x-api-key: YOUR_API_KEY"
```

## 🐛 Troubleshooting

### Environment Variables Tidak Terbaca

Pastikan:
1. File `.env` ada di root project
2. `env_file: - .env` sudah ditambahkan di `docker-compose.yml` untuk service `backend-api`
3. Restart container setelah perubahan

### Lago API Error

1. Pastikan semua service Lago sudah running:
   ```bash
   docker-compose ps
   ```
2. Cek logs:
   ```bash
   docker-compose logs lago-api
   ```
3. Pastikan environment variables di `.env` sudah benar

### Database Error

Database SQLite akan dibuat otomatis di `data/app.db`. Pastikan folder `data` memiliki permission yang tepat.

## 📝 Notes

- WhatsApp service saat ini masih dummy implementation
- Credit minimum untuk send message adalah 100 credits
- Database SQLite digunakan untuk development, pertimbangkan PostgreSQL untuk production
- Lago frontend tersedia di http://localhost:8001 untuk manajemen billing (sesuai `FRONT_PORT` di `.env`)
- File `.env.example` berisi template konfigurasi yang bisa digunakan sebagai starting point


## 👥 Contributors

[Rizqon Sadoda/Nevacloud]
