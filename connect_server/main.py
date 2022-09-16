import shlex
import subprocess

from fastapi import FastAPI

from connect_server.config import settings
from connect_server.model.task import WatchmenTask, AchievementPluginTaskStatus
from connect_server.streamlit.run import run_streamlit_with_pm2
from connect_server.utils.sdk import task_call_back

JUPYTER = "jupyter"

STREAMLIT = "streamlit"

app = FastAPI(
	title="watchmen connector server"
)

app_dict = {}


@app.on_event("shutdown")
def shutdown_event():
	for name in app_dict.keys():
		cmd = "pm2 stop {}.py".format(name)
		subprocess.run(shlex.split(cmd))


@app.post("/task/run")
def run_connector_server(task: WatchmenTask):
	if task.pluginType == STREAMLIT:
		port = run_streamlit_with_pm2(task, app_dict,settings.watchmen_token)
		task_call_back(settings.watchmen_token, task.achievementTaskId, AchievementPluginTaskStatus.SUCCESS,
		               settings.streamlit_host + ":{}".format(port))

	elif task.pluginType == JUPYTER:
		task_call_back(settings.watchmen_token, task.achievementTaskId, AchievementPluginTaskStatus.SUCCESS,
		               settings.jupyter_url + "/" + task.pluginCode)

	else:
		raise ValueError("task pluginType is not supported {}".format(task.pluginType))
