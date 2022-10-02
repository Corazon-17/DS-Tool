import streamlit as st  

from modules import utils
from modules.classes import dtype_changer

def change_dtype(data, data_opt):
	variables = utils.get_variables(data)
	orig_dtypes = utils.get_dtypes(data)
	var_with_dtype = {f"{var} ({dtype})": var for (var, dtype) in zip(variables, orig_dtypes)}
	cat_var = utils.get_categorical(data)

	col1, col2, _ = st.columns([3, 3, 4])
	n_iter = col1.number_input(
			"Number of Columns",
			1, len(variables), 1,
			key="change_dtype_n_rows"
		)

	col2.markdown("#")
	add_pipeline = col2.checkbox("Add To Pipeline", True, key="change_dtype_add_pipeline")

	change_dict = {}
	col1, col2, col3, col4 = st.columns([5,2,2,1])
	for i in range(int(n_iter)):
		var = col1.selectbox(
				f"Column {i+1}",
				var_with_dtype.keys(),
				key=f"change_dtype_var_{i}"
			)

		desired_dtype = col2.selectbox(
				"Desired Dtype",
				["int", "float", "complex", "str"],
				key=f"change_desired_dtype_{i}"
			)

		if desired_dtype in ["int", "float"]:
			desired_bits = col3.selectbox(
					"Desired Bit Length",
					["8", "16", "32", "64", "128", "256"],
					key=f"change_dtype_bit_{i}"
				)

		else:
			desired_bits = col3.selectbox(
					"Desired Bit Length",
					[""],
					key=f"change_dtype_bit_{i}",
					disabled=True
				)

		col4.markdown("###")	
		if change_check(data, var_with_dtype[var], desired_dtype+desired_bits):
			col4.success("", icon="✅")
		else:
			col4.error("", icon="❌")

		change_dict[var_with_dtype[var]] = desired_dtype + desired_bits
		

		# update unique value when selected to prevent same value in different group
		selected = list(change_dict.keys())
		var_with_dtype = {key: val for (key, val) in var_with_dtype.items() if val not in selected}

	status = [change_check(data, var, dtype) for (var, dtype) in change_dict.items()]

	if st.button("Submit", "dtype_change_submit"):
		if all(status): 
			chg = dtype_changer.DtypeChanger(change_dict)
			new_value = chg.fit_transform(data)

			if add_pipeline:
				name = f"Change {', '.join(change_dict.keys())} column dtype"
				utils.add_pipeline(name, chg)

			utils.update_value(data_opt, new_value)
			st.success("Success")

			utils.rerun()

		else:
			st.error("Conversion Failed!")


def change_check(data, var, dtype):
	try:
		data[var].astype(dtype)
		return True
	except:
		return False