import streamlit as st  

from modules import utils

def delete_model(models):
	model_name = st.multiselect(
			"Select Models",
			models.list_name(),
			key="delete_model"
		)

	if st.button("Delete") and model_name:
		models.delete_model(model_name)

		st.success(f"{', '.join(model_name)} Deleted!")
		utils.rerun()