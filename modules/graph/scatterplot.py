import streamlit as st 
import seaborn as sns
import matplotlib.pyplot as plt 

from modules import utils

def scatterplot(data):
	num_var = utils.get_numerical(data, add_hypen=True)
	low_cardinality = utils.get_low_cardinality(data, add_hypen=True)

	col1, col2, col3 = st.columns([4,4,2])
	x = col1.selectbox(
			"X Variable",
			num_var,   
			key="scatter_x_var"
		)

	y = col2.selectbox(
			"Y Variable",
			num_var,   
			key="scatter_y_var"
		)

	hue = col3.selectbox(
			"Hue",
			low_cardinality,   
			key="scatter_hue"
		)

	col1, _ = st.columns([1.5, 8.5])
	set_title = col1.checkbox("Title", key="scatter_set_title")

	if x != "-" and y != "-":
		fig, ax = plt.subplots()

		if set_title:
			title = st.text_input(
					"Input title",
					f"Scatterplot for {x} and {y}",
					key="scatter_title"
				)

			ax.set_title(title)

		hue = None if (hue == "-") else hue

		ax = sns.scatterplot(data=data, x=x, y=y, hue=hue)
		st.pyplot(fig)