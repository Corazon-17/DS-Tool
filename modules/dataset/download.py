import streamlit as st  

def download(dataset):
	list_data = dataset.list_name()

	if list_data:
		col1, col2,col3 = st.columns([6,3,1])
		data_opt = col1.selectbox(
				"Select Dataset",
				list_data,
				key="download_data"
			)

		data_name = col2.text_input(
				"Dataset Name",
				data_opt,
				key="download_name"
			)

		data_format = col3.text_input(
				"",
				".csv",
				disabled=True,
				key="download_format"
			)

		col1, col2, col3 = st.columns([2.3,2.5,5.2])
		if col1.checkbox("Display Data", key="download_display"):
			data = dataset.get_data(data_opt)
			st.dataframe(data)

		header = col2.checkbox("Include Header", True, key="data_header")
		index = col3.checkbox("Include Index", key="data_index")

		st.download_button(
				"Download",
				dataset.get_data(data_opt).to_csv(header=header, index=index),
				data_name+data_format,
				"text/scv",
				key="download_csv"
			)

	else:
		st.header("No Dataset Found!")