import os

class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://wavesHub_user:WavesHub@localhost:5432/wavesHub_db"
    )

settings = Settings()

# Añade esta línea
print(f"DATABASE_URL: {settings.DATABASE_URL}")
