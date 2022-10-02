import streamlit as st 
import seaborn as sns
import matplotlib.pyplot as plt 

from modules import utils

def lineplot(data):
	num_var = utils.get_numerical(data, add_hypen=True)
	low_cardinality = utils.get_low_cardinality(data, add_hypen=True)

	col1, col2, col3, col4 = st.columns(4)
	x = col1.selectbox(
			"X Variable",
			num_var,  
			key="line_x_var"
		)

	y = col2.selectbox(
			"Y Variable",
			num_var,   
			key="line_y_var"
		)


	hue = col3.selectbox(
			"Hue",
			low_cardinality,
			key="line_hue"
		)

	style = col4.selectbox(
			"Style",
			low_cardinality,
			key="line_style"
		)

	col1, col2, _ = st.columns([1.5, 1.5, 7])
	set_title = col1.checkbox("Title", value=False, key="line_set_title")
	legend = col2.checkbox("Legend", value=True, key="line_legend")
	
	if x != "-" and y != "-":
		fig, ax = plt.subplots()

		hue = None if (hue == "-") else hue
		style = None if (style == "-") else style

		if set_title:
			title = st.text_input(
					"Input title",
					f"Lineplot of {y} by {x}",
					key="line_title"
				)

			ax.set_title(title)

		ax = sns.lineplot(data=data, x=x, y=y, hue=hue, style=style, legend=legend)	
		st.pyplot(fig)