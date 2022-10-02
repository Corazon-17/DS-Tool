import streamlit as st  

from modules import utils
from modules.classes import dropper

def dropping(data, data_opt):
	variables = utils.get_variables(data)
	cat_var = utils.get_categorical(data)
	null_var = utils.get_null(data)

	option_dict = {
			"All": variables,
			"Categorical": cat_var, 
			"With Null": null_var, 
			"Blank": []
		}

	option = st.radio(
			"Default Columns",
			option_dict.keys(),
			index=3,
			key="drop_default_options",
			horizontal=True
		)

	col1, col2 = st.columns([7.5, 2.5])
	drop_var = col1.multiselect(
			"Select Columns",
			variables,
			option_dict[option],
			key="drop_var"
		)

	col2.markdown("#")
	add_pipeline = col2.checkbox("Add To Pipeline", True, key="drop_add_pipeline")

	if st.button("Submit", key="drop_submit"):
		if drop_var:
			drp = dropper.Dropper(drop_var)
			new_value = drp.fit_transform(data)

			if add_pipeline:
				name = f"Drop {', '.join(drop_var)} column"
				utils.add_pipeline(name, drp)

			utils.update_value(data_opt, new_value)
			st.success("Success")

			utils.rerun()

		else:
			st.warning("Select columns to drop")