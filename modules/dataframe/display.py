import streamlit as st  
import numpy as np

from modules import utils
from modules.dataframe import filters

def display(data):
	st.header("Display Dataset")

	var = utils.get_variables(data)
	idx_start, idx_end = 0, data.shape[0]

	display_opt = st.radio(
			"",
			["All", "Head", "Tail", "Custom"],
			index=1,
			key="display_opt",
			horizontal=True
		)

	if display_opt != "Custom":
		if display_opt == "Head":
			idx_end = 4
		elif display_opt == "Tail":
			idx_start = idx_end - 5

		st.dataframe(data.loc[idx_start:idx_end, var])

	else:
		custom(data)

def custom(data):
	var = utils.get_variables(data)
	idx_start, idx_end = 0, data.shape[0]

	col1, col2 = st.columns([8, 2])
	col2.markdown("####") # Add blank space so the checkbox can go down
	select_all = col2.checkbox("Select All", True, key="custom_select_all")
	is_filter = col2.checkbox("Filter Index", key="custom_filter")

	if select_all:
		var = col1.multiselect(
				"Select columns",
				var,
				var,
				key="var_table"
			)
	else:
		var = col1.multiselect(
				"Select columns",
				var,
				key="var_table"
			)

	col1, col2, col3 = st.columns([4,4,2])
	if is_filter:
		filters.filter_data(data, var)

	else:
		idx_start = col1.number_input(
				"Start Index",
				0, data.shape[0]-1, 0, # min, max, default
				format="%d",
				key="custom_idx_start"
			)

		idx_end = col2.number_input(
				"End Index",
				1, data.shape[0], 9, # min, max, default
				format="%d",
				key="custom_idx_end"
			)

		st.dataframe(data.loc[idx_start:idx_end, var])