import os
from typing import Generator

from supabase import create_client, Client

def get_supabase_client() -> Generator[Client, None, None]:
    """
    Dependency for getting a Supabase client instance.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        raise ValueError("Missing Supabase credentials")
        
    client = create_client(url, key)
    yield client