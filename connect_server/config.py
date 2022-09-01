from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Watchmen Connector Server"
    watchmen_host:str = None
    watchmen_token:str = None
    streamlit_enabled: bool = False
    streamlit_folder:str = "app_folder"
    streamlit_host:str = "http://localhost"
    jupyter_enabled: bool = False
    jupyter_url :Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()