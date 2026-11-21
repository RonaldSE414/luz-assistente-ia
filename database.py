import os
from functools import lru_cache
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

@lru_cache(maxsize=1)
def cliente_supabase():
    url = os.getenv("SUPABASE_URL")
    chave = os.getenv("SUPABASE_KEY")
    if not url or not chave:
        raise ValueError("Configure SUPABASE_URL e SUPABASE_KEY no arquivo .env.")
    return create_client(url, chave)
