from enum import Enum
from typing import Optional

from pydantic import BaseModel


class AchievementPluginTaskStatus(str, Enum):
	SUBMITTED = 'submitted',
	SENT = 'sent',
	SUCCESS = 'success',
	FAILED = 'failed'


class WatchmenTask(BaseModel):
	achievementTaskId: str = None
	achievementId: str = None
	templateName :str = None
	pluginType :str = None


	# status: AchievementPluginTaskStatus = None
	# url: str = None


class TaskResult(BaseModel):
	taskId: str = None
	status: AchievementPluginTaskStatus = None
	url: Optional[str] =None