import streamlit as st  

from modules import utils

def stats(data):
	st.header("Descriptive Statictics")

	col1, col2, _ = st.columns([1.7,1.7,6.6])
	show_all = col1.checkbox("Show All", key="stats_show_all", value=True)
	transpose = col2.checkbox("Transpose", key="stats_transpose")

	if show_all:
		if transpose:
			st.write(data.describe().T)
		else:
			st.write(data.describe())

	else:
		num_var = utils.get_numerical(data)
		columns = st.multiselect(
				"Select columns",
				num_var,
				key="col_stats"
			)
		if columns: # if columns not empty
			if transpose:
				st.write(data[columns].describe().T)
			else:
				st.write(data[columns].describe())