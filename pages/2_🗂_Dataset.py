import streamlit as st 
import pandas as pd

from modules.classes import data
from modules.dataset import read, display, split, download

try:
	dataset = st.session_state["dataset"]
	default_idx = st.session_state["default_dataset_idx"]

except:
	st.session_state["dataset"] = data.Dataset()
	dataset = st.session_state["dataset"]

	st.session_state["default_dataset_idx"] = 0
	default_idx = st.session_state["default_dataset_idx"]
	
menus = ["Dataset List", "Read Dataset", "Split Dataset", "Download Dataset"]
tabs = st.tabs(menus)

with tabs[0]:
	display.display(dataset, default_idx)

with tabs[1]:
	read.read_dataset(dataset)

with tabs[2]:
	split.split_dataset(dataset)

with tabs[3]:
	download.download(dataset)
