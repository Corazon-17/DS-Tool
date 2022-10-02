import streamlit as st

from modules import utils
from modules.graph import barplot, pieplot, countplot, histogram, boxplot, violinplot, scatterplot, regplot, lineplot

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

menus = ["Bar Plot", "Pie Plot", "Count Plot", "Histogram", "Box Plot", "Violin Plot" , "Scatter Plot", "Reg Plot", "Line Plot"]
tabs = [tab for tab in st.tabs(menus)]

with tabs[0]:
	barplot.barplot(data)

with tabs[1]:
	pieplot.pieplot(data)

with tabs[2]:
	countplot.countplot(data)

with tabs[3]:
	histogram.histogram(data)

with tabs[4]:
	boxplot.boxplot(data)

with tabs[5]:
	violinplot.violinplot(data)

with tabs[6]:
	scatterplot.scatterplot(data)
	
with tabs[7]:
	regplot.regplot(data)

with tabs[8]:
	lineplot.lineplot(data)