"""Configure the PostgreSQL connection and Tortoise ORM models."""
from db_config import settings

DATABASE_URL=f"postgresql://{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.name}"

TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL
    },
    "apps": {
        "models": {
            "models": [
                "app.models",
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}
