from urllib.parse import urljoin

from pydantic import BaseSettings

from server.apps.pictures.intrastructure.services.placeholder import PicturesFetch


class Settings(BaseSettings):
    ### DJANGO
    DJANGO_PLACEHOLDER_API_URL: str
    DJANGO_PLACEHOLDER_API_TIMEOUT: int

    @property
    def DJANGO_PHOTOS_API_URL(self) -> str:
        return urljoin(self.DJANGO_PLACEHOLDER_API_URL, 'photos')

    @property
    def DJANGO_USERS_API_URL(self) -> str:
        return urljoin(self.DJANGO_PLACEHOLDER_API_URL, 'users')

    ### POSTGRES
    DJANGO_DATABASE_HOST: str
    DJANGO_DATABASE_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    ### JSON-SERVER
    JSON_SERVER_HOST: str
    JSON_SERVER_PORT: int
    JSON_SERVER_TIMEOUT: int = 5

    @property
    def JSON_SERVER_URL(self) -> str:
        return f"http://{self.JSON_SERVER_HOST}:{self.JSON_SERVER_PORT}"

    @property
    def JSON_SERVER_PHOTOS_URL(self) -> str:
        return urljoin(self.JSON_SERVER_URL, 'photos')

    @property
    def JSON_SERVER_USERS_URL(self) -> str:
        return urljoin(self.JSON_SERVER_URL, 'users')


    class Config:
        env_file = "config/.env"


SETTINGS = Settings()
