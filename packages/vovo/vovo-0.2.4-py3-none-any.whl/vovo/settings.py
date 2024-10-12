import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Literal


def get_env_file(env: Optional[str] = None) -> str:
    """
    获取环境的 .env 文件路径。
    如果未指定环境参数，则尝试从系统环境变量 APP_ENV 中获取环境名。
    如果未找到 APP_ENV，则返回默认的 `.env` 文件。
    """

    env = env or os.getenv('APP_ENV')

    if env is None:
        # 如果没有传递任何环境，并且系统环境变量 `APP_ENV` 也未设置，则使用默认的 `.env` 文件
        return ".env"

    # 如果明确指定了环境，加载对应的 `.env.{env}` 文件
    return f".env.{env}"


# 在程序启动时只加载一次 .env 文件
@lru_cache()
def load_env_file():
    load_dotenv(get_env_file())


class VovoBaseSettings(BaseSettings):
    # 应用的配置项

    PROJECT_NAME: str
    DOMAIN: str = 'http://localhost:8080'
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    VERSION: str = '1.0.0'
    DEBUG: bool = False

    SENTRY_URI: str | None = None
    CORS_ORIGINS: str = "*"

    # 使用 ConfigDict 替代 class-based Config
    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding='utf-8',
        extra="allow"  # 允许 .env 文件中存在未定义的字段
    )

    def __init__(self, env: Optional[str] = None, **kwargs):
        # 确保每次实例化时，.env 文件已经加载
        load_env_file()
        super().__init__(**kwargs)


@lru_cache()
def get_global_settings() -> VovoBaseSettings:
    """
       This function returns a cached instance of the VovoBaseSettings object.

       Caching is used to prevent re-reading the environment every time the API settings are used in an endpoint.

       If you want to change an environment variable and reset the cache (e.g., during testing), this can be done
       using the `lru_cache` instance method `get_api_settings.cache_clear()`.
    """

    return VovoBaseSettings()


global_settings = get_global_settings()