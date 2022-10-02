import streamlit as st  

from modules import utils
from modules.dataset import read
from sklearn.model_selection import train_test_split

def split_dataset(dataset):
	list_data = dataset.list_name()

	if list_data:
		col1, col2, col3 = st.columns(3)
		data_opt = col1.selectbox(
				"Dataset",
				list_data,
				key="dataset_split_options"
			)

		train_name = col2.text_input(
				"Train Data Name",  
				f"{data_opt}_train",
				key="train_data_name"
			)

		test_name = col3.text_input(
				"Test Data Name",  
				f"{data_opt}_test",
				key="test_data_name"
			)

		data = dataset.get_data(data_opt)
		variables = utils.get_variables(data, add_hypen=True)

		col1, col2, col3, col4 = st.columns([2,4,2,2])
		test_size = col1.number_input(
				"Test Size",
				0.1, 1.0, 0.2,
				key="split_test_size"
			)

		stratify = col2.selectbox(
				"Stratify",
				variables,
				key="split_stratify"
			)

		random_state = col3.number_input(
				"Random State",
				0, 1000, 0,
				key="split_random_state"
			)

		col4.markdown("#")
		shuffle = col4.checkbox("Shuffle", True, key="split_shuffle")

		if st.button("Submit", key="split_submit_button"):
			is_valid = [read.validate(name, list_data) for name in [train_name, test_name]]

			if all(is_valid):
				stratify = None if (stratify == "-") else stratify
				df_train, df_test = train_test_split(data, test_size=test_size, random_state=random_state, shuffle=shuffle, stratify=stratify)
				
				df_train.reset_index(drop=True, inplace=True)
				df_test.reset_index(drop=True, inplace=True)

				dataset.add(train_name, df_train)
				dataset.add(test_name, df_test)

				st.success("Success")
				utils.rerun()

	else:
		st.header("No Dataset Found!")