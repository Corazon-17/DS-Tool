import streamlit as st  
import pandas as pd
import pickle

from modules import utils

try:
	dataset = st.session_state["dataset"]
	pipe = st.session_state["pipeline"]

except KeyError:
	st.header("No Pipeline Found")
	st.stop()

except Exception as e:
	st.warning(e)
	st.stop()

# menus = ["List Pipeline", "Apply Pipeline", "Download", "Upload"]
menus = ["Pipeline Step List", "Apply Pipeline"]
tabs = [tab for tab in st.tabs(menus)]

with tabs[0]:
	pipe_df = pd.DataFrame({
			"Process Name": [proc for proc in pipe.pipelines]
		}, index=[f"Step {i+1}" for i in range(len(pipe.pipelines))])

	st.table(pipe_df)

	if st.button("Clear Pipeline"):
		pipe.clear()
		utils.rerun()

with tabs[1]:
	data_opt = st.selectbox(
			"Select Dataset",
			dataset.list_name(),
			key="pipeline_data_opt"
		)

	if st.button("Apply"):
		data = dataset.get_data(data_opt)
		new_value = pipe.transform(data)

		utils.update_value(data_opt, new_value)
		st.success("Success")

# with tabs[2]:
# 	col1, col2 = st.columns([8,2])
# 	filename = col1.text_input("Filename", "pipeline")
# 	file_format = col2.selectbox("Format", [".pkl"])
	
# 	saved_pipeline = pickle.dumps(pipe)
# 	btn = st.download_button(
# 			label="Download",
# 			data=saved_pipeline,
# 			file_name=filename+file_format
# 		)

# with tabs[3]:
# 	uploaded_file = st.file_uploader("Upload .pkl file")

# 	if uploaded_file is not None:
# 		loaded_pipelines = pickle.loads(uploaded_file.read())
# 		st.session_state["pipeline"] = loaded_pipelines