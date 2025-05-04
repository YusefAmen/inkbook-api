from supabase import create_clien
import os

# Initialize Supabase clien
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)
