import streamlit as st
import pandas as pd
import time

from modules import utils

def show_table(dataframe):
	# CSS to inject contained in a string
	hide_table_row_index = """
	            <style>
	            thead tr th:first-child {display:none}
	            tbody th {display:none}
	            </style>
	            """

	# Inject CSS with Markdown
	st.markdown(hide_table_row_index, unsafe_allow_html=True)

	# Display a static table
	st.table(dataframe)

def update_default_dataset(list_data, name):
	if len(list_data) > 1:
		default_idx = list_data.index(name)
		st.session_state["default_dataset_idx"] = default_idx

	else:
		st.session_state["default_dataset_idx"] = 0

def display(dataset, default_idx):
	list_data = dataset.list_name()

	if list_data: # if there's some data	
		# Set Default Dataset
		col1, _ = st.columns([4.5,5.5])
		default_data = col1.selectbox(
				"Default Dataset",
				list_data,
				default_idx,
				key="set_default_data"
			)

		update_default_dataset(list_data, default_data)

		# Show Table of Uploaded Dataset
		n_rows, n_cols = dataset.get_shape()
		table = pd.DataFrame({
				"Dataset Name": list_data,
				"Number of Rows": n_rows,
				"Number of Columns": n_cols
			}, index=None)

		show_table(table)

		# Delete Dataset
		col1, col2, col3 = st.columns([4.5,1.5,4])
		del_name = col1.selectbox(
				"Delete Dataset",
				list_data,
				key="delete_name"
			)

		col2.markdown("##")
		if col2.button("Confirm", key="del_confirm"):
			dataset.remove(del_name)

			list_data = dataset.list_name()
			if del_name == default_data and len(list_data) > 0:
				default_data = list_data[0]

			update_default_dataset(list_data, default_data)

			col3.markdown("#")
			col3.write(f"{del_name} deleted!")

			utils.rerun()

	else:
		st.header("No Dataset Found!")