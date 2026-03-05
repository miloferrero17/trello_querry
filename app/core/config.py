from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "sql-vector-search-api"
    app_env: str = "dev"
    log_level: str = "INFO"

    pinecone_api_key: str
    pinecone_index: str
    pinecone_namespace: str = "__default__"

    # Pagination/safety for "all matches"
    max_results: int = 5000
    page_size: int = 200

    # Optional semantic mode
    openai_api_key: str | None = None
    openai_embed_model: str = "text-embedding-3-small"
    default_query_top_k: int = 50


settings = Settings()
