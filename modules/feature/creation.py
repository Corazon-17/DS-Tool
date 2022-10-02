import streamlit as st 
import pandas as pd 
import numpy as np

from modules import utils  
from modules.classes import creator

def creation(data, data_opt):
	variables = utils.get_variables(data)

	col1, col2, col3, col4 = st.columns([1.6, 3, 2.4, 2.4])
	add_or_mod = col1.selectbox(
			"Options",
			["Add", "Modify"],
			key="add_or_modify"
		)

	if add_or_mod == "Add":
		var = col2.text_input(
				"New column name",
				key="add_column_name"
			)
	else:
		var = col2.selectbox(
				"Select column",
				variables,
				key="modify_column_name"
			)

	method = col3.selectbox(
			"Method",
			["Math Operation", "Extract Text", "Group Categorical", "Group Numerical"],
			key="creation_method"
		)

	col4.markdown("#")
	add_pipeline = col4.checkbox("Add To Pipeline", True, key="creation_add_pipeline")

	var = var.strip() # remove whitespace
	if method == "Math Operation":
		math_operation(data, data_opt, var, add_pipeline, add_or_mod)
	elif method == "Extract Text":
		extract_text(data, data_opt, var, add_pipeline, add_or_mod)
	elif method == "Group Categorical":
		group_categorical(data, data_opt, var, add_pipeline, add_or_mod)
	elif method == "Group Numerical":
		group_numerical(data, data_opt, var, add_pipeline, add_or_mod)

def math_operation(data, data_opt, var, add_pipeline, add_or_mod):
	col1, col2 = st.columns([7,3])
	operation = col1.text_area(
			"New Value Operation",
			key="new_value"
		)

	col1.caption(
			"Separate all expression with space (including parenthesis).<br>Example: Weight / ( Height ** 2 )", 
			unsafe_allow_html=True
		)

	col2.markdown("##")
	if col2.button("Show Sample", key="creation_show_sample") and operation:
		crt = creator.Creator("Math Operation", var, operation_string=operation)
		new_value = crt.fit_transform(data)
		st.dataframe(new_value.head())

	if st.button("Submit", key="math_submit"):
		if var:
			crt = creator.Creator("Math Operation", column=var, operation_string=operation)
			new_value = crt.fit_transform(data)

			if add_pipeline:
				name = f"{add_or_mod} column {var}"
				utils.add_pipeline(name, crt)

			utils.update_value(data_opt, new_value)
			st.success("Success")

			utils.rerun()
		
		else:
			st.warning("New column name cannot be empty!")


def extract_text(data, data_opt, var, add_pipeline, add_or_mod):
	cat_var = utils.get_categorical(data)

	col1, col2 = st.columns([7,3])
	regex = col1.text_area(
			"Regex pattern", 
			key="extract_regex",
			help=r"Example: ([A-Za-z]+)\\.",

		)

	extract_var = col2.selectbox(
			"Extract From:",
			cat_var,
			key="extract_var"
		)

	if col2.button("Show Sample", key="creation_show_sample") and regex:
		crt = creator.Creator("Extract String", column=var, extract_col=extract_var, regex_pattern=regex)
		new_value = crt.fit_transform(data)
		st.dataframe(new_value.head())
	
	if st.button("Submit", key="extract_submit"):
		if var:
			crt = creator.Creator("Extract String", column=var, extract_col=extract_var, regex_pattern=regex)
			new_value = crt.fit_transform(data)

			if add_pipeline:
				name = f"{add_or_mod} column {var}"
				utils.add_pipeline(name, crt)

			utils.update_value(data_opt, new_value)
			st.success("Success")

			utils.rerun()
			
		else:
			st.warning("New column name cannot be empty!")

def group_categorical(data, data_opt, var, add_pipeline, add_or_mod):
	columns = utils.get_variables(data)
	group_dict = {}

	col1, col2, col3, col4 = st.columns([1.7, 4, 2, 2.3])
	n_groups = col1.number_input(
			"N Group",
			1, 100, 3, 1,
			format="%d",
			key="n_groups"
		)

	group_var = col2.selectbox(
			"Group Column",
			columns,
			key="group_cat_var"
		)

	col3.markdown("#")
	sort_values = col3.checkbox("Sort Values", True, key="group_sort_values")

	col4.markdown("#")
	show_group = col4.checkbox("Show Group", key="group_show_group")

	unique_val = data[group_var].unique()
	if sort_values:
		unique_val = sorted(unique_val, key=lambda val: (val is np.nan, val))

	n_iter = 1 if (n_groups < 2) else int(n_groups-1)

	col1, col2 = st.columns([2.5,7.5])
	for i in range(n_iter):
		group_name = col1.text_input("Group Name", key=f"group_name_{i}")
		group_members = col2.multiselect("Group Members", unique_val, key=f"group_members_{i}")
		group_dict[group_name] = group_members

		# update unique value when selected to prevent same value in different group
		selected = [item for sublist in list(group_dict.values()) for item in sublist]
		unique_val = [val for val in unique_val if val not in selected]

	if n_groups > 1:
		col1, col2, col3 = st.columns([2.5,6.3,1.2])
		col3.markdown("#")
		if col3.checkbox("Other", key="group_other"):
			group_name = col1.text_input("Group Name", key="group_name_end")
			group_members = col2.multiselect("Group Members", unique_val, key=f"group_members_end", disabled=True)

			group_member_vals = sum(group_dict.values(), []) # Gather all group member values in 1D list
			group_members = [val for val in unique_val if val not in group_member_vals]
			group_dict[group_name] = group_members

		else:
			group_name = col1.text_input("Group Name", key="group_name_end")
			group_members = col2.multiselect("Group Members", unique_val, key=f"group_members_end")
			group_dict[group_name] = group_members

	col1, col2 = st.columns([2.5,7.5])
	if show_group:
		col2.write(group_dict)

	if col1.button("Submit", key="group_submit"):
		if var:
			crt = creator.Creator("Group Categorical", column=var, group_col=group_var, group_dict=group_dict)
			new_value = crt.fit_transform(data)
			
			if add_pipeline:
				name = f"{add_or_mod} column {var}"
				utils.add_pipeline(name, crt)

			utils.update_value(data_opt, new_value)
			st.success("Success")

			utils.rerun()

		else:
			st.warning("New column name cannot be empty!")

def group_numerical(data, data_opt, var, add_pipeline, add_or_mod):
	num_var = utils.get_numerical(data)

	col1, col2, col3 = st.columns(3)
	n_groups = col1.number_input(
			"N Groups",
			1, 100, 2,
			key="n_bins"
		)

	group_var = col2.selectbox(
			"Bin Column",
			num_var,
			key="group_num_var"
		)

	col3.markdown("#")
	show_group = col3.checkbox("Show Bin Dict")

	group_dict = {}
	min_val, max_val = data[group_var].min(), data[group_var].max()
	for i in range(int(n_groups)):
		col1, col2, col3, col4 = st.columns([2.6,2.6,2.2,2.6])

		group_val = col4.number_input(
				f"Bin Value",
				i, 100, i,
				key=f"bin_value_{i}"
			)

		col3.markdown("#")
		use_operator = col3.checkbox("Use Operator", key=f"bin_use_operator_{i}")

		if use_operator:
			val1 = col1.selectbox(
					"Operator",
					["==", "!=", "<", ">", "<=", ">="],
					key=f"bin_operator_{i}"
				)

			val2 = col2.number_input(
					"Value",
					min_val, max_val, max_val,
					key=f"max_value_{i}"
				)

		else:
			val1 = col1.number_input(
				"Min Value",
				min_val, max_val, min_val,
				key=f"min_value_{i}"
			)

			val2 = col2.number_input(
					"Max Value",
					min_val, max_val, max_val,
					key=f"max_value_{i}"
				)

		group_dict[group_val] = (val1, val2)

	if st.button("Submit"):
		if var:
			crt = creator.Creator("Group Numerical", column=var, group_col=group_var, group_dict=group_dict)
			new_value = crt.fit_transform(data)
			
			if add_pipeline:
				name = f"{add_or_mod} column {var}"
				utils.add_pipeline(name, crt)

			utils.update_value(data_opt, new_value)
			st.success("Success")

			utils.rerun()

		else:
			st.warning("New column name cannot be empty!")

	if show_group :
		st.json(group_dict)