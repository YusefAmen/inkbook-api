# inkbook-api


# InkBook API – Backend MVP

This is the backend for **InkBook**, a SaaS platform for tattoo artists and studios. It powers client booking, image uploads, and reminder logic. The frontend is built in **Next.js**, using **Supabase** for authentication and storage, and deployed via **Vercel**. This backend contains all business logic, database connectivity, and future observability hooks.

## 🤖 Cursor Agent Instruction

> Use this README to generate the starter FastAPI backend for InkBook. Scaffold the project minimally:
>
> * Core route: `POST /appointments`
> * Health check: `GET /`
> * Stub only for `POST /portfolio` (no full image upload logic)
> * Include `.env` support for Supabase
> * Do not complete the full project – just enough to reach an MVP where booking appointments works end-to-end.
> * The developer will manually build out other features like portfolio uploads, reminders, and observability hooks later.

## 🤖 Tempo/Cursor Prompt

```tempo
Build a FastAPI backend for InkBook, a SaaS platform for tattoo artists.

Requirements:
- Implement `POST /appointments`: accepts name, email, date and stores in Supabase
- Implement health check: `GET /` returning 200 OK
- Add a stub route for `POST /portfolio` that the user will complete manually later
- Support .env values: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
- Do NOT build full CRUD or extra features
- Output Swagger docs via FastAPI automatically
- The developer will wire in observability and auth themselves

Frontend is handled separately in Next.js. This repo is only for the backend logic.
```

## 🧱 Stack

* **FastAPI** (lightweight, async-ready Python web framework)
* **Supabase PostgreSQL** (hosted DB)
* Optional: **S3 or Supabase Storage** for future image uploads
* Optional: Logging hooks to Reflex Observability suite (TODO)

## 🔧 Features to Include Now

### 1. Appointment Booking ✅

* `POST /appointments`: Accepts name, date, and email
* Writes to Supabase `appointments` table
* Will later emit events/logs for observability

### 2. Portfolio Upload (stub only) 🛠

* `POST /portfolio`: Accepts image + notes (TODO: build later)

### 3. Health Check ✅

* `GET /`: Simple `200 OK` to verify deployment

## 🔐 Secrets (.env)

```env
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## 🚀 Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/inkbook-api.git
cd inkbook-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 📂 Suggested Directory Structure

```
inkbook-api/
├── main.py
├── routes/
│   ├── appointments.py
│   └── portfolio.py  # stub
├── services/
│   ├── bookings.py
│   └── storage.py  # optional later
├── db/
│   └── supabase_client.py
├── tests/
├── .env.example
└── requirements.txt
```

* **routes/**: Defines the public-facing API endpoints
* **services/**: Handles business logic per concern (booking, auth, etc.)
* **db/**: Contains Supabase client or ORM logic

## 📤 Example Request

```http
POST /appointments
Content-Type: application/json
{
  "client_name": "John Doe",
  "email": "john@example.com",
  "date": "2025-05-10"
}
```

Returns `201 Created` on success.

## 🧪 Testing Plan (for developer)

* Test `POST /appointments` manually and verify data reaches Supabase
* Use mock clients in `main.py` if Supabase not connected yet
* Confirm observability hooks in `/appointments` are triggered (TODO: Reflex integration)
* Leave `portfolio` endpoint with a `TODO` so it can be manually implemented

## 🧭 What's Next

* Add `GET /appointments` to view bookings (optional MVP+)
* Implement auth headers and token parsing
* Add image upload handling
* Plug this API into Reflex Observability using counter for successful bookings and failed attempts
* Monitor request latency via Prometheus-compatible metrics

## 🔄 Future Microservice Extraction

This `inkbook-api` repo is currently a monolith, but its structure is designed for future splitting. Services like `appointments`, `auth`, `portfolio`, and `notifications` can be extracted into separate microservices later and deployed independently.




InkBook API – Backend MVP
This is the backend for InkBook, a SaaS platform for tattoo artists and studios. It powers client booking, image uploads, and reminder logic. The frontend is built in Next.js, using Supabase for authentication and storage, and deployed via Vercel. This backend contains all business logic, database connectivity, and future observability hooks.
🤖 Cursor Agent Instruction
Use this README to generate the starter FastAPI backend for InkBook. Scaffold the project minimally:
* Core route: POST /appointments
* Health check: GET /
* Stub only for POST /portfolio (no full image upload logic)
* Include .env support for Supabase
* Do not complete the full project – just enough to reach an MVP where booking appointments works end-to-end.
* The developer will manually build out other features like portfolio uploads, reminders, and observability hooks later.
🤖 Tempo/Cursor Prompt
Build a FastAPI backend for InkBook, a SaaS platform for tattoo artists.

Requirements:
- Implement `POST /appointments`: accepts name, email, date and stores in Supabase
- Implement health check: `GET /` returning 200 OK
- Add a stub route for `POST /portfolio` that the user will complete manually later
- Support .env values: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
- Do NOT build full CRUD or extra features
- Output Swagger docs via FastAPI automatically
- The developer will wire in observability and auth themselves

Frontend is handled separately in Next.js. This repo is only for the backend logic.
🧱 Stack
* FastAPI (lightweight, async-ready Python web framework)
* Supabase PostgreSQL (hosted DB)
* Optional: S3 or Supabase Storage for future image uploads
* Optional: Logging hooks to Reflex Observability suite (TODO)
🔧 Features to Include Now
1. Appointment Booking ✅
* POST /appointments: Accepts name, date, and email
* Writes to Supabase appointments table
* Will later emit events/logs for observability
2. Portfolio Upload (stub only) 🛠
* POST /portfolio: Accepts image + notes (TODO: build later)
3. Health Check ✅
* GET /: Simple 200 OK to verify deployment
🔐 Secrets (.env)
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
🚀 Getting Started
git clone https://github.com/YOUR_USERNAME/inkbook-backend.git
cd inkbook-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
📤 Example Request
POST /appointments
Content-Type: application/json
{
  "client_name": "John Doe",
  "email": "john@example.com",
  "date": "2025-05-10"
}
Returns 201 Created on success.
🧪 Testing Plan (for developer)
* Test POST /appointments manually and verify data reaches Supabase
* Use mock clients in main.py if Supabase not connected yet
* Confirm observability hooks in /appointments are triggered (TODO: Reflex integration)
* Leave portfolio endpoint with a TODO so it can be manually implemented
🧭 What's Next
* Add GET /appointments to view bookings (optional MVP+)
* Implement auth headers and token parsing
* Add image upload handling
* Plug this API into Reflex Observability using counter for successful bookings and failed attempts
* Monitor request latency via Prometheus-compatible metrics




