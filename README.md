# InkBook API – Backend MVP

  ## Python Version
  This project requires Python 3.11.x. Use pyenv or your preferred environment manager to install and activate this version.

This is the backend for **InkBook**, a SaaS platform for tattoo artists and studios. It powers client booking, image uploads, and reminder logic. The frontend is built in **Next.js**, using **Supabase** for authentication and storage, and deployed via **Vercel**.

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

## 🔐 Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Optional: Development Settings
DEBUG=True
ENVIRONMENT=development  # development, staging, production

# Optional: CORS Settings (for production)
# ALLOWED_ORIGINS=http://localhost:5173,https://your-domain.com
```

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/inkbook-api.git
cd inkbook-api
```

2. Set up Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create and configure `.env` file:
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

5. Run the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000` with Swagger documentation at `http://localhost:8000/docs`.

## 📂 Project Structure

```
inkbook-api/
├── main.py              # FastAPI application setup
├── requirements.txt     # Dependencies
├── routes/
│   ├── appointments.py  # Appointment booking logic
│   └── portfolio.py     # Portfolio upload stub
├── db/
│   └── supabase_client.py  # Supabase configuration
└── .env.example         # Environment variables template
```

## 📤 API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication
Currently, the API uses Supabase for authentication. All endpoints (except health check) require a valid JWT token in the Authorization header:
```http
Authorization: Bearer <your-supabase-jwt-token>
```

### Endpoints

#### Health Check
```http
GET /
```
Response:
```json
{
  "status": "ok",
  "message": "InkBook API is running"
}
```

#### Create Appointment
```http
POST /appointments
Content-Type: application/json
Authorization: Bearer <token>

{
  "client_name": "John Doe",
  "email": "john@example.com",
  "date": "2024-03-20T14:30:00",
  "notes": "First tattoo session"
}
```
Response (200 OK):
```json
{
  "status": "success",
  "message": "Appointment created successfully",
  "data": {
    "id": "uuid",
    "client_name": "John Doe",
    "email": "john@example.com",
    "date": "2024-03-20T14:30:00",
    "notes": "First tattoo session",
    "status": "pending",
    "created_at": "2024-03-19T10:00:00Z"
  }
}
```

#### Portfolio Upload (Stub)
```http
POST /portfolio
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Geometric Wolf",
  "description": "Blackwork geometric design",
  "style": "blackwork"
}
```
Response (501 Not Implemented):
```json
{
  "detail": "Portfolio upload functionality is not implemented yet"
}
```

### Error Responses

#### 400 Bad Request
```json
{
  "detail": "Failed to create appointment"
}
```

#### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Error message"
}
```

## 📊 Database Schema

### Appointments Table
```sql
create table appointments (
    id uuid default uuid_generate_v4() primary key,
    client_name text not null,
    email text not null,
    date timestamp with time zone not null,
    notes text,
    status text not null default 'pending',
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Add indexes
create index appointments_date_idx on appointments(date);
create index appointments_status_idx on appointments(status);
```

### Portfolio Table (Future Implementation)
```sql
create table portfolio (
    id uuid default uuid_generate_v4() primary key,
    title text not null,
    description text,
    style text not null,
    image_url text not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null,
    user_id uuid references auth.users not null
);

-- Add indexes
create index portfolio_style_idx on portfolio(style);
create index portfolio_user_id_idx on portfolio(user_id);
```

### RLS Policies

#### Appointments
```sql
-- Allow users to view their own appointments
create policy "Users can view their own appointments"
on appointments for select
to authenticated
using (auth.uid() = user_id);

-- Allow users to create appointments
create policy "Users can create appointments"
on appointments for insert
to authenticated
with check (auth.uid() = user_id);
```

#### Portfolio
```sql
-- Allow public to view portfolio items
create policy "Anyone can view portfolio items"
on portfolio for select
to public
using (true);

-- Allow authenticated users to upload portfolio items
create policy "Authenticated users can upload portfolio items"
on portfolio for insert
to authenticated
with check (auth.uid() = user_id);
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=./

# Run specific test file
pytest tests/test_appointments.py
```

### Test Coverage
The CI pipeline will automatically run tests and generate coverage reports. You can view the coverage report locally by running:
```bash
pytest --cov=./ --cov-report=html
```
Then open `htmlcov/index.html` in your browser.

## 🧭 What's Next

### Immediate Tasks
* Add `GET /appointments` to view bookings
* Implement auth headers and token parsing
* Add image upload handling
* Set up proper CORS for production

### Future Enhancements
* Add portfolio image processing
* Implement reminder system
* Add analytics and reporting
* Set up monitoring and logging
* Extract services into microservices

## 🔄 Future Microservice Extraction

This `inkbook-api` repo is currently a monolith, but its structure is designed for future splitting. Services like `appointments`, `auth`, `portfolio`, and `notifications` can be extracted into separate microservices later and deployed independently.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@inkbook.com or join our Discord community.

# Inkbook API - Dockerized Development

## Prerequisites
- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/)
- (Optional) [Supabase CLI](https://supabase.com/docs/guides/cli) if you want to run Supabase locally

## Environment Variables
Create a `.env.docker` file in this directory with the following structure:

```
# Supabase connection (use your real project values or local Supabase if running)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Postgres connection (if your app uses direct DB access)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=inkbook
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Add any other environment variables your app needs
```

**Never commit secrets!**

## Build and Run

```sh
docker compose up --build
```
- The API will be available at [http://localhost:8000](http://localhost:8000)
- Code changes will hot-reload automatically.

## Stopping
```sh
docker compose down
```

## Connecting to Supabase
- For cloud Supabase, use your project URL and keys in `.env.docker`.
- For local Supabase, run the Supabase CLI on your host and point the API to the local endpoints.

## Database
- A local Postgres container is included for development.
- Data is persisted in a Docker volume (`pgdata`).

## Running Tests
You can run tests inside the container:
```sh
docker compose exec api pytest
```

---

**For production, use a separate Dockerfile without --reload and with stricter dependency pinning.**




