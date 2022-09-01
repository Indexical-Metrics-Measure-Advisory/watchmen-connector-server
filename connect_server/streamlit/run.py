import shlex
import subprocess

from connect_server.streamlit.strategy_loader import build_streamlit_app_path
from connect_server.utils.tools import get_free_port

streamlit_run_app = "run_app"

def run_streamlit_with_pm2(task, app_dict):
	app_location = build_streamlit_app_path(task.templateName)
	if task.templateName not in app_dict:
		port = get_free_port()
		cmd = "pm2 start {}.py -- {} {} {}".format(streamlit_run_app, port, task.achievementId, app_location)
		subprocess.run(shlex.split(cmd))
		app_dict[task.templateName] = port
	else:
		port = app_dict[task.templateName]
		cmd = "pm2 restart {}.py -- {} {} {}".format(streamlit_run_app, port, task.achievementId, app_location)
		subprocess.run(shlex.split(cmd))
	return port
