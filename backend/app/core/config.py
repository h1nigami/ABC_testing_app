from dataclasses import dataclass
import os

def load_env() -> None:
    try:
        with open(".env", "r") as f:
            for line in f:
               
                line = line.strip()

                
                if not line or line.startswith('#'):
                    continue

                
                key, value = line.split('=', 1)

                os.environ[key.strip()] = value.strip()

    except FileNotFoundError:
        print("Warning: .env file not found. Skipping loading of environment variables.")

@dataclass
class Settings:
    DSN = os.getenv("DSN")
    TEST_DSN = "sqlite+aiosqlite:///test_db.db"