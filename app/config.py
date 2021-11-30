from pydantic import BaseSettings
from urllib.parse import quote


class Settings(BaseSettings):
    database_type: str
    database_driver: str
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

    def get_alembic_url(self):
        return f"{self.database_type}+{self.database_driver}://{quote(self.database_username)}:{quote(self.database_password)}@{self.database_hostname}:{self.database_port}/{self.database_name}".replace(
            "%", "%%"
        )

    def get_url(self):
        return f"{self.database_type}://{quote(self.database_username)}:{quote(self.database_password)}@{self.database_hostname}:{self.database_port}/{self.database_name}".replace(
            "%", "%%"
        )

    def get_test_url(self):
        return f"{self.database_type}://{quote(self.database_username)}:{quote(self.database_password)}@{self.database_hostname}:{self.database_port}/{self.database_name}_test".replace(
            "%", "%%"
        )


settings = Settings()

if __name__ == "__main__":
    print(settings.get_url())
