from modules import utils
import streamlit as st

class Creator:
	def __init__(self, method, column, extract_col=None, regex_pattern=None, operation_string=None, group_col=None, group_dict=None):
		"""
		Limitation:
			- Supported method: Math Operation, Extract String, Group Categorical, Group Numerical
		"""
		self.method = method  
		self.column = column
		self.extract_col = extract_col
		self.regex_pattern = regex_pattern  
		self.operation_string = operation_string
		self.group_col = group_col
		self.group_dict = group_dict

	def fit(self, X):
		if self.method == "Math Operation":
			columns = utils.get_variables(X)
			self.code = self.__build_code(columns)

	def transform(self, X):
		X_temp = X.copy()
		result = None
		result_dict = locals()

		if self.method == "Math Operation":
			exec(f"result = " + self.code, globals(), result_dict)
			result = result_dict["result"]

		elif self.method == "Extract String":
			result = X_temp[self.extract_col].str.extract(self.regex_pattern)

		elif self.method == "Group Categorical":
			result = [self.__group_func(val) for val in X_temp[self.group_col]]

		elif self.method == "Group Numerical":
			code = "result = X_temp.copy()\n"
			
			for key, val in self.group_dict.items():
				if val[0] in ["==", "!=", "<", ">", "<=", ">="]:
					operator = val[0]
					value = val[1]

					code += f"result.loc[result['{self.group_col}'] {operator} {value}, '{self.column}'] = {key}\n"
				else:
					min_val = val[0]
					max_val = val[1]

					code += f"result.loc[(result['{self.group_col}'] >= {min_val}) & (result['{self.group_col}'] <= {max_val}), '{self.column}'] = {key}\n"

			exec(code, globals(), result_dict)

			result = result_dict["result"][self.column].astype(int)

		X_temp[self.column] = result

		return X_temp

	def fit_transform(self, X):
		X_temp = X.copy()

		self.fit(X_temp)
		X_temp = self.transform(X_temp)

		return X_temp

	def __build_code(self, columns):
		string_list = self.operation_string.split(" ")
		code = ""

		for string in string_list:
			if string in columns:
				code += f"X[\"{string}\"]"

			elif string == "\"":
				code += f"\""

			else:
				code += string

		return code

	def __group_func(self, val):
		for key, values in self.group_dict.items():
			if val in values:
				return key
