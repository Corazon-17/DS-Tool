import streamlit as st  

from modules import utils
from modules.classes import scaler

def scaling(data, data_opt):
	variables = utils.get_variables(data)
	num_var = utils.get_numerical(data)
	cat_var = utils.get_categorical(data)

	default_dict = {
			"Blank": [],
			"All": variables,
			"Numerical": num_var,
			"Categorical": cat_var,
		}

	col1, col2, col3 = st.columns([4,4,2.5])
	col_options = col1.selectbox(
			"Options",
			["Select Columns", "Select All Except"],
			key="col_options"
		)

	method = col2.selectbox(
			"Method",
			["Standard Scaler", "Min-Max Scaler", "Robust Scaler"],
			key="scaling_method"
		)

	col3.markdown("#")
	add_pipeline = col3.checkbox("Add To Pipeline", True, key="scaling_add_pipeline")

	default = st.radio(
			"Default Value",
			default_dict.keys(),
			key="scaling_default_col",
			horizontal=True
		)

	columns = st.multiselect(
			col_options, 
			variables,
			default_dict[default]
		)

	if st.button("Submit", key="scaling_submit"):
		if col_options == "Select All Except":
			columns = [var for var in variables if var not in columns]

		sc = scaler.Scaler(method, columns)
		new_value = sc.fit_transform(data)

		if add_pipeline:
			name = f"Feature scaling using {method}"
			utils.add_pipeline(name, sc)

		utils.update_value(data_opt, new_value)
		st.success("Success")

		utils.rerun()