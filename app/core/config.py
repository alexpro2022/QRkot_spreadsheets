from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков'
    app_description: str = (
        'Наш Фонд собирает пожертвования на различные целевые проекты: '
        'на медицинское обслуживание нуждающихся хвостатых, на обустройство '
        'кошачьей колонии в подвале, на корм оставшимся без попечения '
        'кошкам — на любые цели, связанные с поддержкой кошачьей популяции.')
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret_key: str = 'SECRET'
    token_lifetime: int = 3600
    token_url: str = 'auth/jwt/login'
    auth_backend_name = 'jwt'
    password_length = 3
    admin_email: Optional[EmailStr] = None
    admin_password: Optional[str] = None
    # Переменные для Google API
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None
    SUPER_ONLY = '__Только для суперюзеров:__ '
    AUTH_ONLY = '__Только для авторизованных пользователей:__ '
    ALL_USERS = '__Для всех пользователей:__ '

    class Config:
        env_file = '.env'


settings = Settings()
