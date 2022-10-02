from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

class Scaler:
	def __init__(self, method, columns):
		self.method = method
		self.columns = columns

	def fit(self, X):
		scaler_dict = {
			"Standard Scaler": StandardScaler(),
			"Min-Max Scaler": MinMaxScaler(),
			"Robust Scaler": RobustScaler()
		}

		self.scaler = scaler_dict[self.method]
		self.scaler.fit(X[self.columns])

	def transform(self, X):
		X_temp = X.copy()

		X_temp[self.columns] = self.scaler.transform(X_temp[self.columns])

		return X_temp  

	def fit_transform(self, X):
		X_temp = X.copy()

		self.fit(X_temp)
		X_temp = self.transform(X_temp)

		return X_temp
