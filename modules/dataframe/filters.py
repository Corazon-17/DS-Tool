import streamlit as st  
import numpy as np

from modules import utils

def filter_data(data, display_var):
	var = utils.get_variables(data)
	cat_var = utils.get_categorical(data)
	num_var = utils.get_numerical(data)
	null_var = utils.get_null(data)
	low_cardinality = utils.get_low_cardinality(data)
	num_operator = ["==", "<", ">", "<=", ">=", "!="]
	cat_operator = ["==", "!="]
	set_null = False

	col1, col2, col3, col4 = st.columns([3, 2, 3, 2])
	with col1:
		filter_var = col1.selectbox(
				"Column",
				var,
				key="filter_var"
			)
	
	with col2:
		if filter_var in num_var: # if variable is numerical
			filter_operator = st.selectbox(
					"Operator",
					num_operator,
					key="filter_cond"
				)

		else: # if variable is categorical
			filter_operator = st.selectbox(
					"Operator",
					cat_operator,
					key="filter_cond"
				)

	with col3:
		if filter_var in cat_var or filter_var in low_cardinality:
			# sorted(), np.sort(), list.sort() raise an error if array contains string and nan
			unique_val = sorted(data[filter_var].unique(), key=lambda val: (val is np.nan, val))

			filter_value = st.selectbox(
					"Value",
					unique_val,
					key="filter_value"
				)
		else:
			if filter_var in null_var: # if variable contains null value
				col4.markdown("#####")
				use_slider = col4.checkbox("Use Slider", key="filter_use_slider")
				set_null = col4.checkbox("Null", key="filter_null")
			
			else:	
				col4.markdown("#")
				use_slider = col4.checkbox("Use Slider", key="filter_use_slider")

			if set_null:
				filter_value = st.number_input(
						"Input value",
						value=np.nan,
						key="filter_null_value",
						disabled=True
					)
			
			else:
				if data[filter_var].dtype == int:
					min_val = int(data[filter_var].min())
					max_val = int(data[filter_var].max())
					
					filter_value = slider_or_input(use_slider, min_val, max_val)

				else:
					min_val = float(data[filter_var].min())
					max_val = float(data[filter_var].max())

					filter_value = slider_or_input(use_slider, min_val, max_val)
					

	filtered_data = filter_result(data, filter_var, filter_operator, filter_value)
	result = filtered_data[display_var]
	st.dataframe(result)

def slider_or_input(use_slider, min_val, max_val):
	if use_slider:
		filter_value = st.slider(
				"Value",
				min_val, # min value
				max_val, # max value
				min_val, # default value
				key="filter_value"
			)

	else:
		filter_value = st.number_input(
				"Value",
				min_val, # min value
				max_val, # max value
				min_val, # default value
				key="filter_value"
			)

	return filter_value

def filter_result(data, filter_var, filter_operator, filter_value):
	if filter_operator == "<":
		result = data.loc[data[filter_var] < filter_value]
	elif filter_operator == ">":
		result = data.loc[data[filter_var] > filter_value]
	elif filter_operator == "==":
		if type(filter_value) != str: # np.isna() cannot pass str as parameter
			if np.isnan(filter_value): # check if value is nan
				result = data.loc[data[filter_var].isna() == True]
			else:
				result = data.loc[data[filter_var] == filter_value]
		else:
			result = data.loc[data[filter_var] == filter_value]
	elif filter_operator == "<=":
		result = data.loc[data[filter_var] <= filter_value]
	elif filter_operator == ">=":
		result = data.loc[data[filter_var] >= filter_value]
	else:
		if type(filter_value) != str: # np.isna() cannot pass str as parameter
			if np.isnan(filter_value): # check if value is nan
				result = data.loc[data[filter_var].isna() == False]
			else:
				result = data.loc[data[filter_var] == filter_value]
		else:
			result = data.loc[data[filter_var] != filter_value]

	return result