import pandas as pd

class Classification:
	def __init__(self):
		self.model = {}
		self.result = pd.DataFrame(columns=[
				"Model Name", "Train Data", "Test Data", 
				"Train Accuracy", "Train Precision", "Train Recall", "Train F1-Score",
				"Test Accuracy", "Test Precision", "Test Recall", "Test F1-Score"
			])
		self.target_var = []

	def add_model(self, model_name, model, train_name, test_name, target_var, result):
		self.model[model_name] = model
		if target_var not in self.target_var:
			self.target_var.append(target_var)

		model_info = [model_name, train_name, test_name]
		new_idx = len(self.result)
		self.result.loc[new_idx] = model_info + result

	def get_prediction(self, model_name, X):
		return self.model[model_name].predict(X)

	def list_name(self):
		if bool(self.model):
			return list(self.model.keys())

		return []

	def delete_model(self, model_name):
		for name in model_name:
			del self.model[name]

			drop_idx = self.result.index[self.result["Model Name"] == name][0]
			self.result = self.result.drop(drop_idx).reset_index(drop=True)