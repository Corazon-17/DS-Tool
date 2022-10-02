import streamlit as st 
import seaborn as sns
import matplotlib.pyplot as plt 

from modules import utils

def histogram(data):
	num_var = utils.get_numerical(data, add_hypen=True)
	low_cardinality = utils.get_low_cardinality(data, add_hypen=True)
	bins = "auto"

	col1, col2, col3, col4 = st.columns([2.7, 2.7, 2.7, 1.9])
	var = col1.selectbox(
			"Variable",
			num_var,  
			key="hist_var"
		)

	hue = col2.selectbox(
			"Hue",
			low_cardinality,   
			key="hist_hue"
		)


	stat = col3.selectbox(
			"Aggregate Statistic",
			["count", "frequency", "probability", "percent", "density"],
			key="hist_stat"
		)

	orient = col4.selectbox(
			"Orientation",
			["Vertical", "Horizontal"],
			key="hist_orient"
		)

	col1, col2, col3, col4, _ = st.columns([1.5, 1.8, 1.5, 1.5, 3.7])
	set_title = col1.checkbox("Title", value=False, key="hist_set_title")
	auto_bin = col2.checkbox("Auto Bin", value=True, key="hist_bin")
	kde = col3.checkbox("KDE", key="hist_kde")	
	legend = col4.checkbox("Legend", value=True, key="hist_legend")

	if var != "-":
		fig, ax = plt.subplots()

		hue = None if (hue == "-") else hue

		if not auto_bin:
			bins = st.slider(
					"Bins",
					1, data[var].nunique(), 10
				)

		if set_title:
			title = st.text_input(
					"Input title",
					f"{var} Histogram",
					key="hist_title"
				)

			ax.set_title(title)

		if var != "-":
			if orient == "Vertical":
				ax = sns.histplot(data=data, x=var, bins=bins, hue=hue, kde=kde, legend=legend, stat=stat)	
			else:
				ax = sns.histplot(data=data, y=var, bins=bins, hue=hue, kde=kde, legend=legend, stat=stat)	
			st.pyplot(fig)