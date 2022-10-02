class Pipeline:
	def __init__(self):
		self.pipelines = {}

	def add(self, name, class_obj):
		self.pipelines[name] = class_obj

	def fit(self, X):
		pass

	def transform(self, X):
		X_temp = X.copy()

		for class_obj in self.pipelines.values():
			temp = class_obj.transform(X_temp)
			X_temp = temp

		return X_temp

	def clear(self):
		self.pipelines = {}