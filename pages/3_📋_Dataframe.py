import streamlit as st

from modules import utils
from modules.dataframe import display, info, stats, correlation, duplicate, group

try:
	dataset = st.session_state["dataset"]
	default_idx = st.session_state["default_dataset_idx"]

	data_opt = utils.dataset_opt(dataset.list_name(), default_idx)
	data = dataset.get_data(data_opt)

except KeyError:
	st.header("No Dataset Found")
	st.stop()

except Exception as e:
	st.write(e)
	st.stop()

menus = ["Display", "Information", "Statistics", "Correlation", "Duplicate", "Group"]
tabs = st.tabs(menus)

with tabs[0]:
	display.display(data)

with tabs[1]:
	info.info(data)

with tabs[2]:
	stats.stats(data)

with tabs[3]:
	correlation.correlation(data)

with tabs[4]:
	duplicate.duplicate(data, data_opt)

with tabs[5]:
	# Bug: Return None when some columns dropped

	group.group(data)
