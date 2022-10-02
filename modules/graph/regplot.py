import streamlit as st 
import seaborn as sns
import matplotlib.pyplot as plt 

from modules import utils

def regplot(data):
	num_var = utils.get_numerical(data, add_hypen=True)

	col1, col2= st.columns(2)
	x = col1.selectbox(
			"X Variable",
			num_var, key="reg_x_var"
		)

	y = col2.selectbox(
			"Y Variable",
			num_var, key="reg_y_var"
		)	

	col1, col2, _ = st.columns([1.5,1.5,7])
	set_title = col1.checkbox("Title", key="reg_set_title")
	scatter = col2.checkbox("Scatter", True, key="reg_scatter")

	if x != "-" and y != "-":
		fig, ax = plt.subplots()

		if set_title:
			title = st.text_input(
					"Input title",
					f"Regression Plot of {x} and {y}",
					key="reg_title"
				)

			ax.set_title(title)

		ax = sns.regplot(data=data, x=x, y=y, scatter=scatter)
		st.pyplot(fig)