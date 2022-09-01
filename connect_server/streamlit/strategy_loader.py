from connect_server.config import settings


def build_streamlit_app_path(template_name):
	return settings.streamlit_folder+"/"+template_name