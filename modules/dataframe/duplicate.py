import streamlit as st  
import pandas as pd  

from modules import utils

def duplicate(data, data_opt):
	var = utils.get_variables(data)

	col1, col2, col3 = st.columns([6.5,1.7,1.8])
	col2.markdown("#")
	select_all = col2.checkbox("Select All", True, key="duplicate_select_all")
	default = var if select_all else None

	duplicate_var = col1.multiselect(
			"By",
			var,
			default,
			key="duplicate_var"
		)

	duplicate_keep = col3.selectbox(
			"Keep",
			["first", "last", "False"],
			key="duplicate_keep"
		)
	duplicate_keep = duplicate_keep if (duplicate_keep != "False") else False
	duplicate_var = duplicate_var if duplicate_var else None
	duplicate = data.duplicated(duplicate_var, keep=duplicate_keep)

	duplicate_count = duplicate.sum()
	st.write(f"There are {duplicate_count} duplicates in this dataset")

	if duplicate_count > 0:
		duplicate_data = data.loc[duplicate, duplicate_var]
		st.write(duplicate_data.sort_values(duplicate_var))

	if st.button("Drop Duplicates"):
		new_value = data.drop_duplicates(subset=duplicate_var, keep=duplicate_keep).reset_index(drop=True)
		utils.update_value(data_opt, new_value)
		utils.rerun()