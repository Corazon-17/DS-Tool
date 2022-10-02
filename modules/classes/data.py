

class Dataset:
	def __init__(self):
		self.data = {}

	def add(self, name, data):
		self.data[name] = data

	def remove(self, name):
		del self.data[name]

	def get_data(self, name):
		return self.data[name]

	def list_name(self):
		if bool(self.data): # if data isn't empty
			return list(self.data.keys())
		
		else:
			return []

	def get_shape(self):
		if bool(self.data):
			data_shape = [data.shape for data in self.data.values()]
			n_rows = [shape[0] for shape in data_shape]
			n_cols = [shape[1] for shape in data_shape]

			return n_rows, n_cols
		
		else:
			return [], []