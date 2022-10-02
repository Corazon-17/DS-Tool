

class DtypeChanger:
	def __init__(self, change_dict):
		self.change_dict = change_dict

	def fit(self, X):
		pass

	def transform(self, X):
		X_temp = X.copy()

		for col, dtype in self.change_dict.items():
			X_temp[col] = X_temp[col].astype(dtype)

		return X_temp
		
	def fit_transform(self, X):
		X_temp = X.copy()

		self.fit(X_temp)
		X_temp = self.transform(X_temp)

		return X_temp