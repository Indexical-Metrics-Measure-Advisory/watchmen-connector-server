import shlex
import subprocess

from fastapi import FastAPI

from model.task import WatchmenTask, AchievementPluginTaskStatus
from utils.sdk import task_call_back
from utils.tools import get_free_port

app = FastAPI(
	title="watchmen connector server"
)

app_dict = {}


@app.get("/")
def read_root():
	return {"Hello": "World"}

@app.on_event("shutdown")
def shutdown_event():
	for name in app_dict.keys():
		cmd = "pm2 stop {}.py".format(name)
		subprocess.run(shlex.split(cmd))


@app.post("/task/run")
def run_pm2(task: WatchmenTask):
	if task.pluginType =="streamlit":
		if task.templateName is None:
			task.templateName = "run_app"

		if task.templateName not in app_dict:
			port = get_free_port()
			cmd = "pm2 start {}.py -- {} {}".format(task.templateName, port, task.achievementId)
			subprocess.run(shlex.split(cmd))
			app_dict[task.templateName] = port
		else:
			port = app_dict[task.templateName]
			cmd = "pm2 restart {}.py -- {} {}".format(task.templateName, port, task.achievementId)
			subprocess.run(shlex.split(cmd))

		task_call_back("0Z6ag50cdIPamBIgf8KfoQ", task.achievementTaskId, AchievementPluginTaskStatus.SUCCESS,
		               "http://localhost:{}".format(port))
	elif task.pluginType=="jupyter":
		task_call_back("0Z6ag50cdIPamBIgf8KfoQ", task.achievementTaskId, AchievementPluginTaskStatus.SUCCESS,
		               "http://localhost:{}/lab/tree/customer.ipynb".format("8888"))
