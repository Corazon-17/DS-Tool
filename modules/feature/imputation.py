import streamlit as st  

from modules import utils
from modules.classes import imputer

def imputation(data, data_opt):
	num_var = utils.get_numerical(data)
	null_var = utils.get_null(data)
	low_cardinality = utils.get_low_cardinality(data, add_hypen=True)

	col1, col2 = st. columns([7.5, 2.5])
	if null_var != []:
		var = col1.selectbox(
				"Select columns",
				null_var,
				key="null_var"
			)
		col2.markdown("#")
		add_pipeline = col2.checkbox("Add To Pipeline", True, key="impute_add_pipeline")

		if var in num_var:
			strat, fill_group, constant = impute_num(data, var, low_cardinality)
		else:
			strat, fill_group, constant = impute_cat(data, var, low_cardinality)

		if st.button("Submit", key="impute_submit"):
			fill_group = None if (fill_group == "-") else fill_group
			imp = imputer.Imputer(strategy=strat, columns=[var], fill_value=constant, group_col=fill_group)
			new_value = imp.fit_transform(data)

			if add_pipeline:
				name = f"{var} imputation"
				utils.add_pipeline(name, imp)

			utils.update_value(data_opt, new_value)
			st.success("Success")

			utils.rerun()

	else:
		st.header("No column has missing values")

def impute_num(data, var, low_cardinality):
	fill_group, constant = None, None

	strat = st.selectbox(
			"Strategy",
			# ["mean", "median", "ffill", "bfill", "constant"],
			["mean", "median", "constant"],
			key="impute_strat"
		)

	if strat in ["mean", "median"]:
		fill_group = st.selectbox(
				"Group By",
				low_cardinality,
				key="impute_group_by"
			)

	else:
		max_val = abs(data[var]).max()
		default = 0 if (data[var].dtype == int) else 0.0
		constant = st.number_input(
				"Value",
				-max_val, max_val, default,
				key="new_null_value"
			)

	return strat, fill_group, constant

def impute_cat(data, var, low_cardinality):
	fill_group, constant = None, None

	strat = st.selectbox(
			"Strategy",
			# ["mode", "ffill", "bfill", "value"],
			["mode", "value"],
			key="impute_strat"
		)

	if strat == "mode":
		mode = data[var].mode()
		col1, col2 = st.columns(2)
		mode_strat = col1.selectbox(
				"Options",
				["Select Mode", "Group Mode"],
				key="mode_strat"
			)

		if mode_strat == "Select Mode":
			strat = "constant" # set strat to constant because we will choose the mode value
							   # so, we will treat this strat as constant
			constant = col2.selectbox( # mode can have multiple values
					"Mode value",
					mode,
					key="null_mode"
				)

		else:
			fill_group = col2.selectbox(
				"Group By",
				low_cardinality,
				key="impute_group_by"
			)

	else:
		constant = st.text_input("Value")

	return strat, fill_group, constant