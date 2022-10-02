import streamlit as st  
import numpy as np

from modules import utils
from modules.classes import encoder

def encoding(data, data_opt):
	cat_var = utils.get_categorical(data)
	num_var = utils.get_numerical(data)
	low_cardinality = utils.get_low_cardinality(data, max_unique=5)

	col1, col2, col3 = st.columns([4,3.6,2.4])
	var = col1.selectbox(
			"Select column",
			set(cat_var+low_cardinality),
			key="encoding_var"
		)

	enc_method = ["Ordinal Encoding", "One-Hot Encoding", "Target Encoding"]
	method = col2.selectbox(
			"Select method",
			enc_method,
			key="encoding_method"
		)

	col3.markdown("#")
	add_pipeline = col3.checkbox("Add To Pipeline", True, key="encoding_add_pipeline")

	if method == "Ordinal Encoding":
		try:
			ordinal_encoding(data, data_opt, var, add_pipeline)	
		except:
			pass

	elif method == "One-Hot Encoding":
		onehot_encoding(data, data_opt, var, add_pipeline)

	elif method == "Target Encoding":
		target_encoding(data, data_opt, var, num_var, add_pipeline)

def ordinal_encoding(data, data_opt, var, add_pipeline):
	col1, col2, col3, _ = st.columns([2,2,2,4])
	from_zero = col1.checkbox("Start from 0")
	inc_nan = col2.checkbox("Include nan")
	asc_order = col3.checkbox("Sort Values")

	# include null or no
	unique_val = data[var].unique() if inc_nan else data[var].dropna().unique()
	
	# sort or no
	unique_val = sorted(unique_val, key=lambda val: (val is np.nan, val)) if asc_order else unique_val
	
	# encoding value start from 0 or 1
	enc_val = range(len(unique_val)) if from_zero else range(1, len(unique_val)+1)

	col1, col2 = st.columns(2)
	order = col1.multiselect(
			"Set value order",
			unique_val,
			key="ordinal_order"
		)

	ordinal_enc_dict = {val: new_val for val, new_val in zip(order, enc_val)}
	col2.json(ordinal_enc_dict)

	if col1.button("Submit", key="ordinal_submit"):
		if len(ordinal_enc_dict) == len(unique_val):
			enc = encoder.Encoder(strategy="ordinal", column=var, ordinal_dict=ordinal_enc_dict)
			new_value = enc.fit_transform(data)

			if add_pipeline:
				name = f"{var} ordinal encoding"
				utils.add_pipeline(name, enc)

			utils.update_value(data_opt, new_value)
			st.success("Success")

			utils.rerun()

		else:
			st.warning("Failed")

def onehot_encoding(data, data_opt, var, add_pipeline):
	col1, _ = st.columns([2,8])
	drop_first = col1.checkbox("Drop First")

	if st.button("Submit", "oh_submit"):
		enc = encoder.Encoder(strategy="onehot", column=var)
		new_value = enc.fit_transform(data)

		if add_pipeline:
			name = f"{var} one-hot encoding"
			utils.add_pipeline(name, enc)

		utils.update_value(data_opt, new_value)
		st.success("Success")

		utils.rerun()

def target_encoding(data, data_opt, var, num_var, add_pipeline):
	col1, _ = st.columns([4,6])
	target_var = col1.selectbox(
			"Select target",
			num_var,
			key="target_enc_var"
		)

	if st.button("Submit", "oh_submit"):
		enc = encoder.Encoder(strategy="target", column=var, target_var=target_var)
		new_value = enc.fit_transform(data)

		if add_pipeline:
			name = f"{var} target encoding by {target_var}"
			utils.add_pipeline(name, enc)

		utils.update_value(data_opt, new_value)
		st.success("Success")

		utils.rerun()