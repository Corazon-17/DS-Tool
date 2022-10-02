import streamlit as st  
import pandas as pd
import time

from modules import utils
from io import StringIO
from pathlib import Path

def read_dataset(dataset):
	data = None
	option_list = ["Upload File", "Github URL", "Manual Input", "Sample Data"]
	option = st.radio(
			"Read Method",
			option_list,
			key="read_data_option",
			horizontal=True
		)

	col1, col2 = st.columns([7, 3])
	if option == option_list[0]:
		filepath_or_buffer = upload_file(col1)
	elif option == option_list[1]:
		filepath_or_buffer = github_url(col1)
	elif option == option_list[2]:
		filepath_or_buffer = manual_input(col1)
	elif option == option_list[3]:
		filepath_or_buffer = sample_data(col1)

	name = col2.text_input(
			"Dataset Name",  
			key=f"dataset_name"
		)

	show_sample = col2.checkbox("Show Sample", key=f"show_sample")

	if show_sample and filepath_or_buffer: # if show_sample is True and filepath_or_buffer is not None
		data = pd.read_csv(filepath_or_buffer)
		st.dataframe(data.head())

	if col1.button("Submit", key=f"read_submit"):
		is_valid = validate(name, dataset.list_name())

		if is_valid:
			if data is not None:
				dataset.add(name, data)
			else:
				data = pd.read_csv(filepath_or_buffer)
				dataset.add(name, data)

			st.success("Success")
			
			utils.rerun()
	

def upload_file(col1):
	filepath_or_buffer = col1.file_uploader(
			"Choose a file",  
			type=["csv"],
			key=f"upload_file"
		)

	return filepath_or_buffer

def github_url(col1):
	filepath_or_buffer = col1.text_input(
			"Github Raw Data URL", 
			key=f"github_url"
		)

	return filepath_or_buffer

def manual_input(col1):
	input_data = col1.text_area(
			"Enter data in csv format", 
			key=f"manual_input_data"
		)

	if input_data:
		filepath_or_buffer = StringIO(input_data)
		
		return filepath_or_buffer

def sample_data(col1):
	path = Path().absolute()
	
	list_sample = {
		"Iris Species": f"{path}/sample_data/Iris.csv",
		"Titanic Dataset": f"{path}/sample_data/titanic.csv"
	}

	sample = col1.selectbox(
			"Select Dataset",  
			list_sample.keys(),
			key=f"sample_data"
		)

	filepath_or_buffer = list_sample[sample]

	return filepath_or_buffer

def validate(name, used_names):
	if name.strip() == "": # check if name is empty string or only contains whitespace
		st.warning("Dataset name cannot be empty!")
		return False
	elif name in used_names: # check if name is already used
		st.warning(f"Name {name} already used! Enter another name.")
		return False

	return True
