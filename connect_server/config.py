from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Watchmen Connector Server"
    watchmen_host:str = None
    watchmen_token:str = None
    streamlit_enabled: bool = False
    streamlit_folder:str = None
    streamlit_host:str = None
    jupyter_enabled: bool = False
    jupyter_url :Optional[str] = None

settings = Settings()