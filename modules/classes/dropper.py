class Dropper:
	def __init__(self, columns):
		self.columns = columns

	def fit(self, X):
		pass

	def transform(self, X):
		X_temp = X.copy()
		X_temp = X_temp.drop(self.columns, axis=1)

		return X_temp

	def fit_transform(self, X):
		X_temp = X.copy()
		
		self.fit(X_temp)
		X_temp = self.transform(X_temp)

		return X_temp