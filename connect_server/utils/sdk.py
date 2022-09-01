import requests

from connect_server.config import settings
from connect_server.model.task import TaskResult
from connect_server.utils.tools import build_headers


def load_subject_by_id(token,subject_id):
	response = requests.get(settings.watchmen_host + "/indicator/subject", params={"subject_id":subject_id},
	                         headers=build_headers(token))
	return response.json()


def task_call_back(token,task_id , status,url):
	task = TaskResult(taskId=task_id, status=status ,url=url)
	url = settings.watchmen_host + "/indicator/achievement/task/result"
	print(url)
	response = requests.post(url, data=task.json(),
	                         headers=build_headers(token))
	print(response.status_code)


