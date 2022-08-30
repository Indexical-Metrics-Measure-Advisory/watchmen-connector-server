import requests
from ml_sdk.ml.sdk.watchmen.sdk import build_headers

from connect_server.model.task import TaskResult

local_env_url = "http://localhost:8000"


def load_subject_by_id(token,subject_id):
	response = requests.get(local_env_url + "/indicator/subject", params={"subject_id":subject_id},
	                         headers=build_headers(token))
	return response.json()


def task_call_back(token,task_id , status,url):
	task = TaskResult(taskId=task_id, status=status ,url=url)

	response = requests.post(local_env_url + "/indicator/achievement/task/result", data=task.json(),
	                         headers=build_headers(token))
	# print( response.json())

