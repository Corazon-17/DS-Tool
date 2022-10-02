import streamlit as st  

from modules import utils  
from modules.feature import encoding, imputation, scaling, creation, dropping, change_dtype

try:
	dataset = st.session_state["dataset"]
	default_idx = st.session_state["default_dataset_idx"]

	data_opt = utils.dataset_opt(dataset.list_name(), default_idx)
	data = dataset.get_data(data_opt)

except KeyError:
	st.header("No Dataset Found")
	st.stop()

except Exception as e:
	st.warning(e)
	st.stop()

menus = ["Add/Modify", "Change Dtype", "Imputation",  "Encoding", "Scaling", "Drop Column"]
tabs = [tab for tab in st.tabs(menus)]

with tabs[0]:
	creation.creation(data, data_opt)

with tabs[1]:
	change_dtype.change_dtype(data, data_opt)

with tabs[2]:
	imputation.imputation(data, data_opt)

with tabs[3]:
	encoding.encoding(data, data_opt)

with tabs[4]:
	scaling.scaling(data, data_opt)

with tabs[5]:
	dropping.dropping(data, data_opt)