from ml_sdk.ml.sdk.index import WatchmenClient
from ml_sdk.ml.sdk.watchmen.sdk import load_indicator_by_id

from utils.sdk import load_subject_by_id


class WatchmenStreamlitClient(object):
	def __init__(self, watchmen_client: WatchmenClient):
		self.watchmen_client = watchmen_client
		self.current_achievement = None
		self.indicators_dict = {}

	def init(self,achievement_id):
		self.current_achievement = self.__get_achievement(achievement_id)
		indicator_list = self.current_achievement["indicators"]
		self.__load_indicators_dict(indicator_list)

	def __get_achievement(self,achievement_id):
		return self.watchmen_client.load_achievement(achievement_id)

	def __load_indicators_dict(self, indicator_list):
		for indicator_data in indicator_list:
			indicator_id = indicator_data["indicatorId"]
			if indicator_id != "-1":
				indicator = load_indicator_by_id(self.watchmen_client.token, indicator_data["indicatorId"])
				self.indicators_dict[indicator["name"].upper()] = {"indicator": indicator, "node": indicator_data}

	def load_achievement_by_id(self, achievement_id):
		return self.wetchmen_client.load_achievement(achievement_id)

	def load_metric_value(self, indicator_id, aggregate_arithmetic, filters=None):
		result = self.watchmen_client.load_indicator_value(indicator_id, aggregate_arithmetic, filters)
		return result["current"]

	def __merge_date_conditions(self, criterias, filters, subject):
		results = []
		columns = subject["dataset"]["columns"]
		if len(filters) == 0:
			return filters
		for filter in filters:
			if filter["factor"] == "year":
				for criteria in criterias:
					if criteria["value"] == "year":
						result = criteria.copy()
						result["value"] = str(filter["value"])
						results.append(result)
			elif filter["factor"] == "month":
				for criteria in criterias:
					if criteria["value"] == "month":
						result = criteria.copy()
						result["value"] = str(filter["value"])
						results.append(result)
			else:
				for column in columns:
					if column["alias"] == filter["factor"]:
						results.append({
							"factorId": column["columnId"],
							"operator": filter["operator"],
							"value": filter["value"]
						})
		return results

	def merge_column_conditions(self, criterias, filters):

		pass

	def load_dataset(self, name):
		return self.watchmen_client.load_dataset(name)

	def load_indicator_value_by_name(self, indicator_name, aggregate_arithmetic, filter=[]):
		if isinstance(indicator_name, str):
			up_name = indicator_name.upper()
			if up_name in self.indicators_dict:
				indicator = self.indicators_dict[up_name]
				criterias = indicator["node"]["criteria"]
				subject_id = indicator["indicator"]["topicOrSubjectId"]
				subject = load_subject_by_id(self.watchmen_client.token, subject_id)
				filters = self.__merge_date_conditions(criterias, filter, subject)
				return self.load_metric_value(indicator["indicator"]["indicatorId"], aggregate_arithmetic,
				                              filters)

			else:
				raise Exception("indicator_name can not find in achievement indicator list ")
		else:
			raise Exception("indicator_name is not a text ")

	def get_dataset_columns(self, indicator_id):

		pass
