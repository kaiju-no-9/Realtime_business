from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_LOGS_TOPIC: str = os.getenv("KAFKA_LOGS_TOPIC")
    KAFKA_ALERTS_TOPIC: str = os.getenv("KAFKA_ALERTS_TOPIC")
    KAFKA_GROUP_ID: str = os.getenv("KAFKA_GROUP_ID")   

    class Config:
        env_file = ".env"


settings = Settings()