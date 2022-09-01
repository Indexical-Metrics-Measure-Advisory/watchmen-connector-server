from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class AchievementPluginTaskStatus(str, Enum):
	SUBMITTED = 'submitted',
	SENT = 'sent',
	SUCCESS = 'success',
	FAILED = 'failed'


class WatchmenTask(BaseModel):
	achievementTaskId: str = None
	achievementId: str = None
	pluginType: str = None
	params: List[str] = None
	pluginCode:str = None


class TaskResult(BaseModel):
	taskId: str = None
	status: AchievementPluginTaskStatus = None
	url: Optional[str] = None
