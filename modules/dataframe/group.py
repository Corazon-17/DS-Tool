import streamlit as st 

from modules import utils

def group(data):
	columns = utils.get_variables(data)

	col1, col2 = st.columns(2)
	group_var = col1.multiselect(
			"By",
			columns,
			key="group_var"
		)

	agg_func = col2.selectbox(
			"Aggregate Function",
			["count", "sum", "min", "max", "mean", "median", "std", "var"],
			key="filter_agg_func"
		)

	if group_var:
		st.dataframe(data.groupby(by=group_var, as_index=False).agg(agg_func))